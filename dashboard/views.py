from django.contrib.auth.mixins import PermissionRequiredMixin, UserPassesTestMixin
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.contrib.auth import get_user_model
from django.views.generic import (
    ListView,
    CreateView,
    UpdateView,
    TemplateView
)
from rest_framework import status

from contest.forms import ContestForm
from contest.models import Contest
from problemset.models import Problem
from dashboard.mixins import ContestActionMixin


User = get_user_model()


class DashboardView(TemplateView):
    template_name = 'dashboard/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_tab': 'active'
        })
        return context


# Problem_set Related Dashboard Views
class MyProblemListView(PermissionRequiredMixin, ListView):
    model = Problem
    template_name = 'dashboard/problem_list.html'
    context_object_name = 'problems'
    permission_required = []

    def get_queryset(self):
        return Problem.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'my_problems_tab': 'active'
        })
        return context


# Contest Related Dashboard Views
class MyContestListView(PermissionRequiredMixin, ListView):
    model = Contest
    template_name = 'dashboard/contest_list.html'
    context_object_name = 'contests'
    permission_required = []

    def get_queryset(self):
        return Contest.objects.filter(author=self.request.user).order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'my_contests_tab': 'active'
        })
        return context


class ContestCreateView(PermissionRequiredMixin, CreateView):
    model = Contest
    form_class = ContestForm
    template_name = 'dashboard/contest_form.html'
    permission_required = []
    success_url = reverse_lazy('dashboard:my-contests')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'card_header': 'New Contest',
            'operation': 'Create'
        })
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ContestUpdateView(UserPassesTestMixin, UpdateView):
    model = Contest
    form_class = ContestForm
    template_name = 'dashboard/contest_form.html'
    success_url = reverse_lazy('dashboard:my-contests')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest_update_tab': 'active',
            'card_header': 'Update Contest Info',
            'contest': self.get_object(),
            'operation': 'Update'
        })
        return context

    def test_func(self):
        return self.get_object().author == self.request.user


class ContestProblemListView(UserPassesTestMixin, ListView):
    model = Problem
    template_name = 'dashboard/contest_problems.html'
    context_object_name = 'problems'

    def get_object(self):
        return get_object_or_404(Contest, pk=self.kwargs.get('pk'))

    def get_queryset(self):
        return Problem.objects.filter_preserved_by_ids(self.get_object().problem_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        contest = self.get_object()
        problem_ids, problem_scores = contest.problem_ids, contest.problem_scores
        scores_obj = {problem_id: problem_scores[index] for index, problem_id in enumerate(problem_ids)}

        context.update({
            'contest_problems_tab': 'active',
            'contest': contest,
            'scores_obj': scores_obj,
            'problems': context.get('problems', [])
        })
        return context

    def test_func(self):
        return self.get_object().author == self.request.user


class AddContestProblemAjaxView(ContestActionMixin):

    def post(self, request, *args, **kwargs):
        try:
            problem_id = int(request.POST.get('problem_id'))
            problem_score = int(request.POST.get('problem_score'))
            is_update = True if request.POST.get('is_update') == 'true' else False

            contest = self.get_object()
            problem = Problem.objects.get(id=problem_id)
            problem_ids = contest.problem_ids
            problem_scores = contest.problem_scores

            if not is_update:
                if problem_id in problem_ids:
                    return JsonResponse({
                        'error_message': 'Problem already added'
                    }, status=status.HTTP_400_BAD_REQUEST)

                problem_ids.append(problem_id)
                problem_scores.append(problem_score)

            else:
                index = problem_ids.index(problem_id)
                problem_scores[index] = problem_score

            Contest.objects.filter(id=contest.id).update(
                problem_ids=problem_ids,
                problem_scores=problem_scores
            )
        except (Problem.DoesNotExist, Exception):
            return JsonResponse({
                'error_message': 'Invalid Problem Id or Score'
            }, status=status.HTTP_400_BAD_REQUEST)

        contest = self.get_object()
        problem_ids, problem_scores = contest.problem_ids, contest.problem_scores
        scores_obj = {problem_id: problem_scores[index] for index, problem_id in enumerate(problem_ids)}
        return self.render_to_response({
            'scores_obj': scores_obj,
            'problems': Problem.objects.filter_preserved_by_ids(problem_ids)
        })


class RemoveContestProblemAjaxView(ContestActionMixin):

    def post(self, request, *args, **kwargs):
        try:
            problem_id = int(self.request.POST.get('problem_id'))

            contest = self.get_object()
            problem_ids = contest.problem_ids
            problem_scores = contest.problem_scores

            index = problem_ids.index(problem_id)
            problem_ids.pop(index)
            problem_scores.pop(index)

            Contest.objects.filter(id=contest.id).update(
                problem_ids=problem_ids,
                problem_scores=problem_scores
            )
        except (Contest.DoesNotExist, Exception):
            return JsonResponse({
                'error_message': 'Something went wrong'
            }, status=status.HTTP_400_BAD_REQUEST)

        scores_obj = {problem_id: problem_scores[index] for index, problem_id in enumerate(problem_ids)}
        return self.render_to_response({
            'scores_obj': scores_obj,
            'problems': Problem.objects.filter_preserved_by_ids(problem_ids)
        })


class ContestAuthorListView(UserPassesTestMixin, ListView):
    model = User
    template_name = 'dashboard/contest_authors.html'
    context_object_name = 'authors'

    def get_object(self):
        return Contest.objects.get(id=self.kwargs.get('pk'))

    def get_queryset(self):
        return User.objects.filter(id__in=[self.get_object().author_id])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest_authors_tab': 'active',
            'contest': self.get_object()
        })
        return context

    def test_func(self):
        return self.get_object().author == self.request.user


class ContestStatisticsView(UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/contest_statistics.html'

    def get_object(self):
        return get_object_or_404(Contest, pk=self.kwargs.get('pk'))

    def test_func(self):
        return self.get_object().author == self.request.user

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'contest': self.get_object(),
            'contest_statistics_tab': 'active'
        })
        return context
