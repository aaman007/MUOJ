from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from django.contrib.auth import get_user_model

from contest.models import Contest
from problemset.models import Problem, Submission


User = get_user_model()


class RunningContestListView(ListView):
    model = Contest
    context_object_name = 'contests'
    template_name = 'contest/running_contest_list.html'

    def get_queryset(self):
        return Contest.objects.running_contests()

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
        return Contest.objects.upcoming_contests()

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


class ContestProblemListView(ListView):
    model = Problem
    template_name = 'contest/contest_problems.html'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest': self.get_contest(),
            'contest_nav': 'active',
            'contest_problems_tab': 'active'
        })
        return context


class ContestMySubmissionListView(ListView):
    model = Submission
    template_name = 'contest/contest_my_submissions.html'
    context_object_name = 'submissions'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

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


class ContestStandingsListView(ListView):
    model = User
    template_name = 'contest/contest_standings.html'
    context_object_name = 'users'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest': self.get_contest(),
            'contest_nav': 'active',
            'contest_standings_tab': 'active'
        })
        return context
