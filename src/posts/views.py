from django.shortcuts import render

from django.views.generic import (
    ListView,  # Para listar los blogs
    DetailView,  # Para mostrar detalle del blogs
    CreateView,  # Para crear un blogs
    DeleteView,  # Para eliminar un Blog
    UpdateView,  # Para actualizar los blogs
)

from posts.models import Post, PostView, Like, Comment
from .forms import PostForm


class PostListView(ListView):
    model = Post
    template_name = "posts/post_list.html"

    def get_context_data(self, **kwargs):
        """Metodo para pasar el contexto"""
        context = super().get_context_data(**kwargs)
        context.update({"view": "listar"})
        return context


class PostDetailView(DetailView):
    model = Post
    template_name = "posts/post_detail.html"

    def get_context_data(self, **kwargs):
        """Metodo para pasar el contexto"""
        context = super().get_context_data(**kwargs)
        context.update({"view": "detalle"})
        return context


class PostCreateView(CreateView):
    form_class = PostForm
    model = Post
    # fields = "__all__"
    # exclude = ("publish_date", "last_updated")
    template_name = "posts/post_create.html"

    def get_context_data(self, **kwargs):
        """Metodo para pasar el contexto"""
        context = super().get_context_data(**kwargs)
        context.update({"view": "crear"})
        return context

    success_url = "/"


class PostUpdateView(UpdateView):
    form_class = PostForm
    model = Post
    # fields = "__all__"
    # exclude = ("publish_date", "last_updated")
    template_name = "posts/post_update.html"

    def get_context_data(self, **kwargs):
        """Metodo para pasar el contexto"""
        context = super().get_context_data(**kwargs)
        context.update({"view": "actualizar"})
        return context

    success_url = "/"


class PostDeleteView(DeleteView):
    model = Post
    template_name = "posts/post_delete.html"
    success_url = "/"

    def get_context_data(self, **kwargs):
        """Metodo para pasar el contexto"""
        context = super().get_context_data(**kwargs)
        context.update({"view": "borrar"})
        return context
