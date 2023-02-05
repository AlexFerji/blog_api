from rest_framework import serializers
from .models import BlogPost, BlogComent


class PostReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения поста """
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'body', 'files', 'created_at', 'updated_at', 'total_likes']


class PostWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для создание поста"""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = BlogPost
        fields = ['author', 'title', 'body', 'files', 'created_at', 'updated_at', 'total_likes']


class CommentReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтение коментария"""
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = BlogComent
        fields = ['id', 'author', 'post', 'body', 'file', 'created_at', 'updated_at', 'total_likes']


class CommentWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи коментария"""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BlogComent
        fields = ['author', 'post', 'body', 'file', 'created_at', 'updated_at', 'total_likes']

