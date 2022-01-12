from django.shortcuts import render, get_object_or_404, redirect

from django.views.generic import (
    ListView,  # Para listar los blogs
    DetailView,  # Para mostrar detalle del blogs
    CreateView,  # Para crear un blogs
    DeleteView,  # Para eliminar un Blog
    UpdateView,  # Para actualizar los blogs
)

from posts.models import Post, PostView, Like, Comment
from .forms import PostForm, CommentForm


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
    
    def post(self, *args, **kwargs):
        form = CommentForm(self.request.POST)
        if form.is_valid():
            post = self.get_object()
            comment = form.instance
            comment.user = self.request.user
            comment.post = post
            comment.save()
            return redirect("detail", slug=post.slug)

    def get_context_data(self, **kwargs):
        """Metodo para pasar el contexto"""
        context = super().get_context_data(**kwargs)
        context.update({"view": "detalle", 'form': CommentForm})
        return context
    
    def get_object(self, **kwargs):
        object = super().get_object(**kwargs)
        # Solo usuarios autenticados cuentan para contar como post visto
        if self.request.user.is_authenticated:
            PostView.objects.get_or_create(user=self.request.user, post=object)
        return object

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


def like(request, slug):
    post = get_object_or_404(Post, slug=slug)
    like_qs = Like.objects.filter(user=request.user, post=post)
    if like_qs.exists():
        like_qs[0].delete()
        return redirect('detail', slug=slug)
    Like.objects.create(user=request.user, post=post)
    return redirect('detail', slug=slug)    