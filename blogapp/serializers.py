from rest_framework import serializers
from .models import Author, Post


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'image', 'created_at', 'updated_at']


class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'avatar', 'email']


class AuthorSerializerWithPosts(serializers.ModelSerializer):
    posts = PostSerializer(many=True)

    class Meta:
        model = Author
        fields = ['id', 'name', 'avatar', 'email', 'posts']


class PostSerializerWithAuthor(serializers.ModelSerializer):
    author = AuthorSerializer(many=False)

    class Meta:
        model = Post
        fields = ['id', 'title', 'body', 'image', 'created_at', 'updated_at', 'author']
