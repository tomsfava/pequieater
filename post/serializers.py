from rest_framework import serializers
from .models import Post
from user.serializers import SimpleUserSerializer

class PostSerializer(serializers.ModelSerializer):
    author = SimpleUserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format="%Y-%m-%d %H:%M:%S", read_only=True)
    likes_count = serializers.SerializerMethodField()
    liked_by_user = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'author', 'content', 'created_at', 'likes_count', 'liked_by_user']
        read_only_fields = ['id', 'author', 'created_at', 'likes_count', 'liked_by_user']

    def get_likes_count(self, obj):
        return obj.likes.count()

    def get_liked_by_user(self, obj):
        user = self.context['request'].user
        if user.is_authenticated:
            return obj.likes.filter(id=user.id).exists()
        return False