from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

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
    def put(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        serializer = PostSerializer(post, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors)


class PostDeleteAPIView(APIView):
    def delete(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        post_pk = post.pk
        post.delete()
        serializer = PostSerializer(post)
        return Response({"issue_pk": post_pk})


class PostCreateAPIView(APIView):
    def post(self, request):
        posts = Post.objects.all()
        posts_count = posts.count()
        posts_count += 1
        serializer = PostCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(id=posts_count, author_id=request.auth.user_id)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)


