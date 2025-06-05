from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as _

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'bio']

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = User(**validated_data)
        user.set_password(password)
        user.save()
        return user

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserPublicSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField()
    following_count = serializers.SerializerMethodField()
    is_following = serializers.SerializerMethodField()
    following = SimpleUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'bio', 'followers_count', 'following_count', 'is_following', 'following']

    def get_followers_count(self, obj):
        return obj.followers.count()
    def get_following_count(self, obj):
        return obj.following.count()
    def get_is_following(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated():
            return obj.followers.filter(id=request.user.id).exists()
        return False