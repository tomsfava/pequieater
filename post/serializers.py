from rest_framework import serializers
from .models import Post
from user.serializers import SimpleUserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at']
        read_only_fields = ['id', 'author', 'created_at']