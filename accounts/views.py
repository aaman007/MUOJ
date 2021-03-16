from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import (
    ListView,
    DetailView,
)
from django.contrib.auth import get_user_model
from django.contrib import messages
from accounts.models import Profile
from problemset.models import Submission
from accounts.forms import UserRegisterForm,UserUpdateForm,ProfileUpdateForm
from blog.models import Blog
from contest.models import Contest


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
    paginate_by = 20
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

    def get_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        return Submission.objects.filter(user=self.get_user()).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_submissions_tab': 'active',
            'v_user': get_object_or_404(User, username=self.kwargs.get('username'))
        })
        return context


class UserProfileView(DetailView):
    model = User
    template_name = 'accounts/user_profile.html'
    context_object_name = 'v_user'

    def get_object(self, queryset=None):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        history = self.get_object().profile.rating_history
        rated_contests = [idx for idx in range(len(history)+1)]
        ratings = [0]
        ratings.extend([contest.get('new_rating') for contest in history])
        context.update({
            'dashboard_profile_tab': 'active',
            "rated_contests": rated_contests,
            "ratings": ratings
        })
        return context


class UserBlogListView(ListView):
    model = Blog
    paginate_by = 5
    context_object_name = 'user_blogs'
    ordering = ['-created_at']
    template_name = 'accounts/user_blogs_list.html'

    def get_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        return Blog.objects.filter(user=self.get_user())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_blogs_tab': 'active',
            'v_user': get_object_or_404(User, username=self.kwargs.get('username'))
        })
        return context


class UserContestListView(ListView):
    model = Contest
    context_object_name = 'user_contests'
    template_name = 'accounts/user_contest_list.html'

    def get_user(self):
        return get_object_or_404(User, username=self.kwargs.get('username'))

    def get_queryset(self):
        return Contest.objects.user_participation(self.get_user())

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_contest_tab': 'active',
            'v_user': get_object_or_404(User, username=self.kwargs.get('username'))
        })
        return context


@login_required
def profile_update_view(request, username):
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('accounts:update-profile', username)

    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)

    context = {
        'u_form': u_form,
        'p_form': p_form
    }

    context.update({
        'dashboard_settings_tab': 'active',
        'v_user': get_object_or_404(User, username=username)
    })

    return render(request, 'accounts/user_settings.html', context)
