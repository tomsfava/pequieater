from django.urls import path
from .views import PostListCreateAPIView, PostDestroyAPIView, ToggleLikeAPIView

urlpatterns = [
    path("", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDestroyAPIView.as_view(), name="post-delete"),
    path("<int:pk>/like/", ToggleLikeAPIView.as_view(), name="post-like-toggle"),
]