from django.views.generic import ListView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.template.loader import render_to_string

from .models import Post
from .forms import PostForm

class PostListView(LoginRequiredMixin, ListView):
    model = Post
    template_name = "post_list.html"
    context_object_name = "posts"
    ordering = ["-created_at"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = PostForm()
        return context

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostForm
    template_name = "partials/_post_form.html"

    def form_valid(self, form):
        post = form.save(commit=False)
        post.author = self.request.user
        post.save()
        html = render_to_string("partials/_post.html", {"form": form})
        return HttpResponse(html)

    def form_invalid(self, form):
        html = render_to_string("partials/_post_form.html",{"form": form})
        return HttpResponse(html, status=400)
