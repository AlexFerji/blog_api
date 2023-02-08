from rest_framework import serializers
from .models import BlogPost, BlogComent
from .mixins import LikedMixin
from blog import services as likes_services

class PostReadSerializer(serializers.ModelSerializer):
    """Сериализатор для чтения поста """
    author = serializers.CharField(source="author.username", read_only=True)

    class Meta:
        model = BlogPost
        fields = ['id', 'author', 'title', 'body', 'files', 'created_at', 'updated_at', 'total_likes']

    def get_is_fan(self, obj) -> bool:
        """Проверяет, лайкнул ли `request.user` твит (`obj`).
        """
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class PostWriteSerializer(LikedMixin,
serializers.ModelSerializer):
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


    def get_is_fan(self, obj) -> bool:
        """Проверяет, лайкнул ли `request.user` твит (`obj`).
        """
        user = self.context.get('request').user
        return likes_services.is_fan(obj, user)


class CommentWriteSerializer(serializers.ModelSerializer):
    """Сериализатор для записи коментария"""
    author = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = BlogComent
        fields = ['author', 'post', 'body', 'file', 'created_at', 'updated_at', 'total_likes']

