from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView
)

from problemset.models import Problem, Submission


User = get_user_model()


class ProblemListView(ListView):
    model = Problem
    template_name = 'problemset/problem_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active',
            'problemset_problems_tab': 'active'
        })
        return context


class SubmissionListView(ListView):
    model = Submission
    template_name = 'problemset/submission_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active',
            'problemset_submissions_tab': 'active'
        })
        return context


class StandingsListView(ListView):
    model = Submission
    template_name = 'problemset/standings.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active',
            'problemset_standings_tab': 'active'
        })
        return context
