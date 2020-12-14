from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
)
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.models import Profile
from problemset.models import Submission
from accounts.forms import UserRegisterForm
from blog.models import Blog
from contest.models import Contest
from problemset.models import Problem


User = get_user_model()


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}!')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})


class UserListView(ListView):
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'

    def get_queryset(self):
        return Profile.objects.all().order_by('-rating')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'users_nav': 'active'
        })
        return context


class UserSubmissionListView(ListView):
    model = Submission
    template_name = 'accounts/user_submission_list.html'
    context_object_name = 'user_submissions'
    paginate_by = 10

    def get_queryset(self):
        return Submission.objects.filter(user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_submissions_tab': 'active'
        })
        return context


class UserProfileView(DetailView):
    model = User
    template_name = 'accounts/user_profile.html'
    context_object_name = 'user'
    paginate_by = 10

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_profile_tab': 'active'
        })
        return context


class UserBlogListView(ListView):
    model = Blog
    paginate_by = 5
    context_object_name = 'user_blogs'
    ordering = ['-created_at']
    template_name = 'accounts/user_blogs_list.html'

    def get_queryset(self):
        return Blog.objects.filter(user = self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'blog_nav': 'active',
            'dashboard_blogs_tab': 'active'
        })
        return context


class UserContestListView(ListView):
    model = Contest
    paginate_by = 10
    context_object_name = 'user_contest'
    template_name = 'accounts/user_contest_list.html'
    ordering = ['-created_at']

    def get_queryset(self):
        return Contest.objects.past_contests()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_contest_tab': 'active'
        })
        return context


class UserProblemSettingListView(ListView):
    model = Problem
    context_object_name = 'user_problems'
    template_name = 'accounts/user_problems_list.html'
    author = Problem.author

    def get_queryset(self):
        return Problem.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_problemsetting_tab': 'active'
        })
        return context
