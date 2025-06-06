from django.urls import path
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from .views import LoginView, RegisterView, UserDetailTemplateView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="user-register"),
    path("user/<int:pk>/", UserDetailTemplateView.as_view(), name="user-detail"),
    path("Logout/", DjangoLogoutView.as_view(next_page="login"), name="logout"),
]