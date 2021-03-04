from django.contrib.auth.mixins import UserPassesTestMixin, LoginRequiredMixin
from django.urls import reverse_lazy
from contest.models import Contest
from django.views.generic import (
    ListView,
    DeleteView,
    CreateView,
    UpdateView,
    DetailView,
    TemplateView
)

from blog.forms import BlogForm,NewCommentForm
from blog.models import Blog, Comments


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


class HomeView(ListView):
    model = Blog
    paginate_by = 5
    context_object_name = 'blogs'
    ordering = ['-created_at']
    template_name = 'base.html'

    def get_queryset(self):
        return Blog.objects.filter(preference=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'home_nav': 'active',
            'upcoming_contest': Contest.objects.upcoming_contests(self.request.user.username)
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
        comments_connected = Comments.objects.filter(post_connected=self.get_object()).order_by('-date_posted')
        context.update({
            'blog_nav': 'active',
            'comments': comments_connected,
            'form': NewCommentForm(instance=self.request.user),
        })
        return context

    def post(self, request, *args, **kwargs):
        new_comment = Comments(Comment=request.POST.get('Comment'),
                            author=self.request.user,
                            post_connected=self.get_object(), )
        new_comment.save()
        return self.get(self, request, *args, **kwargs)
