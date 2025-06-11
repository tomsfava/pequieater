from rest_framework import generics, permissions, status
from rest_framework.response import Response

from .models import Post
from .serializers import PostSerializer

class IsAuthorOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.author == request.user


class PostListCreateAPIView(generics.ListCreateAPIView):
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()

        filter_param = self.request.query_params.get('filter')
        author_id = self.request.query_params.get('author')

        if filter_param == 'following' and self.request.user.is_authenticated:
            followed_users = self.request.user.following.all()
            queryset = queryset.filter(author__in=followed_users)

        elif author_id:
            try:
                author_id = int(author_id)
                queryset = queryset.filter(author__id=author_id)
            except ValueError:
                pass
            except self.request.user.DoesNotExist:
                pass

        return queryset.order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

class PostDestroyAPIView(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def get_permissions(self):
        return [permissions.IsAuthenticated(), IsAuthorOrReadOnly()]

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)