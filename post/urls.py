from django.urls import path
from .views import PostListCreateAPIView, PostDestroyAPIView

urlpatterns = [
    path("", PostListCreateAPIView.as_view(), name="post-list-create"),
    path("<int:pk>/", PostDestroyAPIView.as_view(), name="post-delete"),
]