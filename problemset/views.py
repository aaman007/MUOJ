from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.views.generic import (
    ListView
)

from problemset.models import Problem, Submission


User = get_user_model()


class ProblemListView(ListView):
    model = Problem
    context_object_name = 'problems'
    template_name = 'problemset/problem_list.html'

    def get_queryset(self):
        """
        Returns a queryset containing problems in descending order based on the number
        of people who solved each problem
        - It uses annotation and aggregation to calculate the problem solution count
        by number of unique users for each problem
        """

        return Problem.objects.annotate(
            solve_count=Count(
                'submissions__user',
                filter=Q(submissions__status='ac'),
                distinct=True
            )
        ).order_by('-solve_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active',
            'problemset_problems_tab': 'active'
        })
        return context


class SubmissionListView(ListView):
    model = Submission
    context_object_name = 'submissions'
    template_name = 'problemset/submission_list.html'

    def get_queryset(self):
        return Submission.objects.all().order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active',
            'problemset_submissions_tab': 'active'
        })
        return context


class StandingsListView(ListView):
    model = User
    context_object_name = 'users'
    template_name = 'problemset/standings.html'

    def get_queryset(self):
        """
        Returns a queryset containing users in descending order based on their
        problem solve count
        - It uses annotation and aggregation to calculate the unique problem solve count
        for each user
        """

        return User.objects.annotate(
            solve_count=Count(
                'submissions__problem',
                filter=Q(submissions__status='ac'),
                distinct=True
            )
        ).order_by('-solve_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active',
            'problemset_standings_tab': 'active'
        })
        return context
