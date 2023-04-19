from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from api.permissions import IsAuthor
from api.serializers import PostSerializer, PostCreateSerializer
from posts.models import Post


class PostListView(APIView):
    def get(self, request, *args, **kwargs):
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)


class PostDetailApiView(APIView):
    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post)
        return Response(serializer.data)


class PostUpdateApiView(APIView):
    permission_classes = [IsAuthor]

    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class PostDeleteAPIView(APIView):
    permission_classes = [IsAuthor]

    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post_pk = post.pk
        post.delete()
        serializer = PostSerializer(post)
        return Response({"issue_pk": post_pk})


class PostCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        posts = Post.objects.all()
        id_list = []
        for post in posts:
            id_list.append(post.id)
        id_list.sort()
        last_id = id_list[-1]
        last_id += 1
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id=last_id, author_id=request.auth.user_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


class LikeAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        user = request.user
        if user in post.user_likes.all():
            post.user_likes.remove(user)
            post.save()
            return Response({"like_info": "unliked"})
        else:
            post.user_likes.add(user)
            post.save()
            return Response({"like_info": "liked"})
