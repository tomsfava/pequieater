from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import get_object_or_404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import UserRegisterSerializer, UserPublicSerializer

User = get_user_model()

class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        token = Token.objects.get(key=response.data['token'])
        user = token.user
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
        })

class LogoutView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class UserRegisterView(APIView):
    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserPublicSerializer
    permission_classes = [permissions.IsAuthenticated]

    def path(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            return Response({"detail": "Not allowed to edit this profile"}, status=status.HTTP_403_FORBIDDEN)
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.pk != self.get_object().pk:
            return Response({"detail": "Not allowed to delete this profile"}, status=status.HTTP_403_FORBIDDEN)
        return self.destroy(request, *args, **kwargs)

class ToggleFollowView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        user_to_follow = get_object_or_404(User, pk=pk)
        current_user = request.user

        if user_to_follow == current_user:
            return Response({"detail": "You can't follow yourself"}, status=status.HTTP_400_BAD_REQUEST)

        if user_to_follow in current_user.following.all():
            current_user.following.remove(user_to_follow)
            action = "unfollowed"

        else:
            current_user.following.add(user_to_follow)
            action = "followed"

        return Response({
            "status": "success",
            "action": action,
            "target_user_id": user_to_follow.id,
            "target_username": user_to_follow.username,
        }, status=status.HTTP_200_OK)