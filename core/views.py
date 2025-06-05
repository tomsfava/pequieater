from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from user.forms import UserRegisterForm

class LoginView(DjangoLoginView):
    template_name = "login.html"

class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)