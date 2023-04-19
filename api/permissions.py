from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission

from posts.models import Post


class IsAuthor(BasePermission):
    def has_permission(self, request, view):
        user = request.auth.user_id
        post = get_object_or_404(Post, pk=view.kwargs.get('pk'))
        if user == post.author.pk:
            return True
        else:
            return False
