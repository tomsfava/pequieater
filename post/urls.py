from django.urls import path
from .views import PostListCreateAPIView, PostDestroyAPIView, ToggleLikeAPIView, CommentListCreateAPIView, CommentDestroyAPIView

urlpatterns = [
    path("", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDestroyAPIView.as_view(), name="post-delete"),
    path("<int:pk>/like/", ToggleLikeAPIView.as_view(), name="post-like-toggle"),
    path("<int:pk>/comments/", CommentListCreateAPIView.as_view(), name="post-comments"),
    path("comments/<int:pk>/", CommentDestroyAPIView.as_view(), name="comment-delete"),
]