from django.urls import path

from .views import LoginView, RegisterView, UserDetailTemplateView

urlpatterns = [
    path("", LoginView.as_view(), name="login"),
    path("register/", RegisterView.as_view(), name="user-register"),
    path("user/<int:pk>/", UserDetailTemplateView.as_view(), name="user-detail"),
]