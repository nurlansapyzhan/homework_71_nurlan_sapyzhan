from rest_framework import serializers

from posts.models import Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'description', 'image', 'author', 'created_at']
        read_only_fields = ['id', 'created_at']


class PostCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'description', 'image', 'created_at']
        read_only_fields = ['id', 'created_at']