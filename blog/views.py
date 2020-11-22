from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    DetailView
)

from blog.forms import BlogForm
from blog.models import Blog


class BlogListView(ListView):
    model = Blog
    paginate_by = 5
    context_object_name = 'blogs'
    ordering = ['-created_at']
    template_name = 'blog/blog_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active'
        })
        return context


class BlogCreateView(LoginRequiredMixin, CreateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'card_header': 'New Blog',
            'operation': 'Create'
        })
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class BlogUpdateView(UserPassesTestMixin, UpdateView):
    model = Blog
    template_name = 'blog/blog_form.html'
    context_object_name = 'blog'
    form_class = BlogForm
    success_url = reverse_lazy('blog:blog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'card_header': 'Update Blog',
            'operation': 'Update'
        })
        return context

    def test_func(self):
        return self.request.user == self.get_object().user


class BlogDeleteView(UserPassesTestMixin, DeleteView):
    model = Blog
    template_name = 'blog/blog_delete.html'
    success_url = reverse_lazy('blog:blog-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active'
        })
        return context

    def test_func(self):
        return self.request.user == self.get_object().user


class BlogDetailView(DetailView):
    model = Blog
    template_name = 'blog/blog_details.html'
    context_object_name = 'blog'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active'
        })
        return context
