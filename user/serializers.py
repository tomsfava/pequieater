from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={'input_type': 'password'}, write_only=True)
    password2 = serializers.CharField(style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password2', 'bio']

    def validate(self, data):
        super().validate(data)
        password = data.get('password')
        password2 = data.get('password2')

        if password and password2 and password != password2:
            raise serializers.ValidationError({'password2': 'As senhas devem ser idênticas'})

        if 'password' in data:
            data.pop('password2')

        return data

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
            bio=validated_data.get('bio', '')
        )
        return user

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']

class UserPublicSerializer(serializers.ModelSerializer):
    followers_count = serializers.SerializerMethodField(read_only=True)
    following_count = serializers.SerializerMethodField(read_only=True)
    is_following = serializers.SerializerMethodField(read_only=True)
    following = SimpleUserSerializer(many=True, read_only=True)
    followers = SimpleUserSerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'bio', 'followers_count', 'following_count', 'is_following', 'following', 'followers']
        read_only_fields = ['id', 'username', 'followers_count', 'following_count', 'is_following', 'following', 'followers']

    def get_followers_count(self, obj):
        return obj.followers.count()

    def get_following_count(self, obj):
        return obj.following.count()

    def get_is_following(self, obj):
        request = self.context.get("request", None)
        if request and request.user.is_authenticated:
            return obj.followers.filter(id=request.user.id).exists()
        return False