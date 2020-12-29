import self
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
)
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.contrib.auth import get_user_model
from contest.forms import (
    SubmissionForm,
    ClarificationCreateForm,
    ClarificationReplyForm
)
from contest.models import Contest
from problemset.models import Problem, Submission,Clarification


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
            'form_class': ClarificationCreateForm(contest_id=self.kwargs.get('contest_id')),
            'form_reply': ClarificationReplyForm(),
            'clarifications': Clarification.objects.filter(contest=self.kwargs.get('contest_id')),
            'contest_problems_tab': 'active',
        })
        return context


class ClarificationCreateView(CreateView):
    model = Clarification
    form_class = ClarificationCreateForm

    def get_success_url(self):
        return reverse_lazy('contest:contest-problems', kwargs={'contest_id': self.kwargs.get('contest_id')})

    def form_valid(self, form):
        form.instance.contest = get_object_or_404(Contest, id=self.kwargs.get('contest_id'))
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClarificationReplyView(UpdateView):
    model = Clarification
    form_class = ClarificationReplyForm

    def get_success_url(self):
        return reverse_lazy('contest:contest-problems', kwargs={'contest_id': self.kwargs.get('contest_id')})


class ContestProblemDetails(DetailView):
    model = Problem
    template_name = 'contest/contest_problem_details.html'
    context_object_name = 'problem'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active',
            'contest': self.get_contest(),
            'submission_form': SubmissionForm(),
            'testcases': self.get_object().testcases.filter(is_sample=True)
        })
        return context


class ContestSubmissionCreateView(CreateView):
    model = Submission
    form_class = SubmissionForm

    def get_success_url(self):
        return reverse_lazy('contest:contest-my-submissions', kwargs={'contest_id': self.kwargs.get('contest_id')})

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.contest = get_object_or_404(Contest, pk=self.kwargs.get('contest_id'))
        form.instance.problem = get_object_or_404(Problem, pk=self.kwargs.get('problem_id'))
        return super().form_valid(form)


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

