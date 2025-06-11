from django.urls import path
from .views import PostListView, PostCreateView, PostDeleteView

urlpatterns = [
    path("", PostListView.as_view(), name="post-list"),
    path("create/", PostCreateView.as_view(), name="post-create"),
    path("<int:pk>/delete/", PostDeleteView.as_view(), name="post-delete"),
]