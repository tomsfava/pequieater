from django.views.generic import FormView, TemplateView
from django.contrib.auth.views import LoginView as DjangoLoginView
from django.urls import reverse_lazy
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.http import HttpResponse, HttpResponseForbidden
from user.forms import UserRegisterForm, UserUpdateForm

User = get_user_model()

class LoginView(DjangoLoginView):
    template_name = "login.html"

    def get_success_url(self):
        return reverse_lazy("user-detail", kwargs={"pk": self.request.user.pk})

class RegisterView(FormView):
    template_name = "register.html"
    form_class = UserRegisterForm
    success_url = reverse_lazy("login")

    def form_valid(self, form):
        form.save()
        return super().form_valid(form)

class UserDetailTemplateView(LoginRequiredMixin, TemplateView):
    template_name = "user_detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        profile_user = get_object_or_404(User, pk=self.kwargs["pk"])
        current_user = self.request.user
        is_own_profile = profile_user == current_user
        following = profile_user.following.all()

        context.update({
            "profile_user": profile_user,
            "is_own_profile": is_own_profile,
            "following": following,
        })
        return context

    def get(self, request, *args, **kwargs):
        profile_user = get_object_or_404(User, pk=self.kwargs["pk"])
        current_user = request.user
        is_own_profile = profile_user == current_user

        edit_mode = request.GET.get("edit") == "true"

        if edit_mode:
            if not is_own_profile:
                return HttpResponseForbidden("Você não pode editar este perfil.")
            form = UserUpdateForm(instance=current_user)
            html = render_to_string("partials/_user_update_form.html", {"form": form}, request=request)
            return HttpResponse(html)

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        profile_user = get_object_or_404(User, pk=self.kwargs["pk"])
        current_user = request.user

        if profile_user != current_user:
            return HttpResponseForbidden("Você não pode editar este perfil.")

        form = UserUpdateForm(request.POST, instance=current_user)

        if form.is_valid():
            form.save()
            return redirect("user-detail", pk=current_user.pk)

        context = self.get_context_data()
        context["form"] = form
        return self.render_to_response(context)
