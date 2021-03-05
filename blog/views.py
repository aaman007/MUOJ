from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    DetailView,
    FormView
)

from blog.forms import BlogForm,NewCommentForm
from blog.models import Blog, Comment


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
        comments_connected = Comment.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        context.update({
            'blog_nav': 'active',
            'comments': comments_connected,
            'form': NewCommentForm(instance=self.request.user),
        })
        return context


class CreateCommentFormView(LoginRequiredMixin, FormView):
    form_class = NewCommentForm
    template_name = 'blog/blog_details.html'

    def get_success_url(self):
        return reverse('blog:blog-details', kwargs={'pk': self.kwargs.get('pk')})

    def get_blog(self):
        return get_object_or_404(Blog, id=self.kwargs.get('pk'))

    def form_valid(self, form):
        form.instance.post_connected = self.get_blog()
        form.instance.author = self.request.user
        form.save()
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Comment cannot be empty')
        return redirect(self.get_success_url())
