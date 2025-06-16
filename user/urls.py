from django.urls import path
from .views import UserRegisterView, CustomAuthToken, UserListView, UserDetailView, LogoutView, ToggleFollowView

urlpatterns = [
    path("register/", UserRegisterView.as_view(), name="api-user-register"),
    path("login/", CustomAuthToken.as_view(), name="api-login"),
    path("logout/", LogoutView.as_view(), name="api-logout"),
    path("user/", UserListView.as_view(), name="api-user-list"),
    path("user/<int:pk>/", UserDetailView.as_view(), name="api-user-detail"),
    path("user/<int:pk>/toggle-follow/", ToggleFollowView.as_view(), name="api-user-toggle-follow"),
]