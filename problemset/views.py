from django.contrib.auth import get_user_model
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from problemset.forms import SubmissionForm
from problemset.models import Problem, Submission, TestCase
from problemset.forms import ProblemCreateForm,TestCreateForm


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

        current_user = self.request.user if self.request.user.is_authenticated else None
        return Problem.objects.exclude(is_protected=True).annotate(
            solve_count=Count(
                'submissions__user',
                filter=Q(submissions__status='AC'),
                distinct=True
            ),
            is_solved=Count(
                'submissions__user',
                filter=Q(submissions__status='AC', submissions__user=current_user)
            )
        ).order_by('-solve_count')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active',
            'problemset_problems_tab': 'active'
        })
        return context


class ProblemDetailView(DetailView):
    model = Problem
    template_name = 'problemset/problem_details.html'
    context_object_name = 'problem'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active',
            'submission_form': SubmissionForm(),
            'testcases': self.get_object().testcases.filter(is_sample=True)
        })
        return context


class SubmissionListView(ListView):
    model = Submission
    paginate_by = 10
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


class SubmissionCreateView(CreateView):
    model = Submission
    form_class = SubmissionForm

    def get_success_url(self):
        return reverse_lazy('problemset:submission-list')

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.problem = get_object_or_404(Problem, pk=self.kwargs.get('problem_id'))
        return super().form_valid(form)


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
                filter=Q(submissions__status='AC'),
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


class ProblemCreateView(CreateView):
    model = Problem
    template_name = 'problemset/problem_create_form.html'
    form_class = ProblemCreateForm

    def get_success_url(self):
        return reverse_lazy('dashboard:user-problems-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_ProblemStatement_tab': 'active',
            'operation': 'Create',
        })
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class ProblemUpdateView(UpdateView):
    model = Problem
    template_name = 'problemset/problem_create_form.html'
    form_class = ProblemCreateForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('dashboard:user-problems-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_ProblemStatement_tab': 'active',
            'key': 'update',
            'operation': 'Update'
        })
        return context

    def test_func(self):
        return self.request.user == self.get_object().user


class TestCaseListView(ListView):
    model = TestCase
    template_name = 'problemset/test_case_list.html'
    context_object_name = 'testcases'

    def get_queryset(self):
        return TestCase.objects.filter(problem_id=self.kwargs.get('pk'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_ProblemTests_tab': 'active',
            'form_class': TestCreateForm(),
            'problem': Problem.objects.get(id=self.kwargs.get('pk')),
        })
        return context


class TestCaseCreateView(CreateView):
    model = TestCase
    form_class = TestCreateForm

    def get_success_url(self):
        return reverse_lazy('problemset:testcase-list', kwargs={'pk': self.kwargs.get('pk')})

    def form_valid(self, form):
        form.instance.problem = get_object_or_404(Problem, id=self.kwargs.get('pk'))
        return super().form_valid(form)


class TestCaseDeleteView(DeleteView):
    model = TestCase
    template_name = 'problemset/testcase_delete.html'

    def get_success_url(self):
        return reverse_lazy('problemset:testcase-list', kwargs={'pk': self.kwargs.get('pk')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'dashboard_ProblemTests_tab': 'active',
        })
        return context

    def test_func(self):
        return self.request.user == self.get_object().user
