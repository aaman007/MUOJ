from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.contrib.auth import get_user_model

from contest.models import Contest
from problemset.models import Problem, Submission


User = get_user_model()


class RunningContestListView(ListView):
    model = Contest
    context_object_name = 'contests'
    template_name = 'contest/running_contest_list.html'

    def get_queryset(self):
        return Contest.objects.running_contests(self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest_running_tab': 'active',
            'contest_nav': 'active'
        })
        return context


class UpcomingContestListView(ListView):
    model = Contest
    context_object_name = 'contests'
    template_name = 'contest/upcoming_contest_list.html'

    def get_queryset(self):
        return Contest.objects.upcoming_contests(self.request.user.username)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest_upcoming_tab': 'active',
            'contest_nav': 'active'
        })
        return context


class PastContestListView(ListView):
    model = Contest
    context_object_name = 'contests'
    template_name = 'contest/past_contest_list.html'

    def get_queryset(self):
        return Contest.objects.past_contests()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest_past_tab': 'active',
            'contest_nav': 'active'
        })
        return context


class ContestProblemListView(UserPassesTestMixin, ListView):
    model = Problem
    template_name = 'contest/contest_problems.html'
    context_object_name = 'problems'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def test_func(self):
        contest = self.get_contest()
        state = contest.state
        return state == 'Finished' or (state == 'Running' and self.request.user in contest.contestants.all())

    def get_queryset(self):
        return Problem.objects.filter_preserved_by_ids(self.get_contest().problem_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest': self.get_contest(),
            'contest_nav': 'active',
            'contest_problems_tab': 'active'
        })
        return context


class ContestMySubmissionListView(UserPassesTestMixin, ListView):
    model = Submission
    template_name = 'contest/contest_my_submissions.html'
    context_object_name = 'submissions'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def test_func(self):
        return self.get_contest().state != 'Upcoming'

    def get_queryset(self):
        return Submission.objects.filter(contest=self.get_contest(), user=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest': self.get_contest(),
            'contest_nav': 'active',
            'contest_my_submissions_tab': 'active'
        })
        return context


class ContestStandingsListView(UserPassesTestMixin, TemplateView):
    template_name = 'contest/contest_standings.html'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def test_func(self):
        return self.get_contest().state != 'Upcoming'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest': self.get_contest(),
            'contest_nav': 'active',
            'contest_standings_tab': 'active'
        })
        return context


class ContestRegistrationTemplateView(LoginRequiredMixin, TemplateView):
    template_name = 'contest/contest_registration.html'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'contest': self.get_contest(),
            'contest_nav': 'active',
        })
        return context

    def post(self, *args, **kwargs):
        self.get_contest().contestants.add(self.request.user)
        messages.add_message(self.request, messages.SUCCESS, 'Registration Successful!')
        return redirect('contest:running-contest-list')
