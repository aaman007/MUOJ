from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import (
    DetailView,
    CreateView,
    UpdateView, DeleteView,
)
from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import ListView, TemplateView
from django.contrib.auth import get_user_model
from rest_framework.reverse import reverse

from contest.forms import (
    SubmissionForm,
    ClarificationCreateForm,
    ClarificationReplyForm, AnnouncementForm
)
from contest.models import Contest, Announcement
from problemset.models import Problem, Submission,Clarification
from django.utils import timezone

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
        return Problem.objects.filter_preserved_by_ids_with_count(
            self.get_contest().problem_ids,
            self.kwargs.get('contest_id')
        )

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


class ClarificationCreateView(UserPassesTestMixin, CreateView):
    model = Clarification
    form_class = ClarificationCreateForm

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def test_func(self):
        contest = self.get_contest()
        return contest.state == 'Running' and self.request.user in contest.contestants.all()

    def get_success_url(self):
        return reverse('contest:contest-problems', kwargs={'contest_id': self.kwargs.get('contest_id')})

    def form_valid(self, form):
        form.instance.contest = get_object_or_404(Contest, id=self.kwargs.get('contest_id'))
        form.instance.user = self.request.user
        return super().form_valid(form)


class ClarificationReplyView(UpdateView):
    model = Clarification
    form_class = ClarificationReplyForm

    def get_success_url(self):
        return reverse('contest:contest-problems', kwargs={'contest_id': self.kwargs.get('contest_id')})


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
        return reverse('contest:contest-my-submissions', kwargs={'contest_id': self.kwargs.get('contest_id')})

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
        return self.request.user.is_authenticated and self.get_contest().state != 'Upcoming'

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


class ContestAnnouncementsListView(UserPassesTestMixin, ListView):
    model = Announcement
    template_name = 'contest/contest_announcements.html'
    context_object_name = 'announcements'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def test_func(self):
        if self.get_contest().state == 'Finished':
            return True
        return self.request.user in self.get_contest().contestants.all() and self.get_contest().state != 'Upcoming'

    def get_queryset(self):
        return Announcement.objects.filter(contest=self.get_contest()).order_by('-created_at')

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context.update({
            'contest': self.get_contest(),
            'contest_nav': 'active',
            'contest_announcements_tab': 'active',
            'announcement_form': AnnouncementForm()
        })
        return context


class ContestAnnouncementCreateView(UserPassesTestMixin, CreateView):
    model = Announcement
    form_class = AnnouncementForm

    def get_success_url(self):
        return reverse('contest:contest-announcements', kwargs={'contest_id': self.kwargs.get('contest_id')})

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def test_func(self):
        return self.get_contest().author == self.request.user

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.contest = self.get_contest()
        return super().form_valid(form)


class ContestAnnouncementTemplateView(UserPassesTestMixin, TemplateView):
    model = Announcement
    template_name = 'contest/contest_announcements.html'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def test_func(self):
        return self.get_contest().author == self.request.user

    def post(self, request, *args, **kwargs):
        try:
            announcement_id = request.POST.get('announcement_id')
            title = request.POST.get('title')
            content = request.POST.get('content')

            Announcement.objects.filter(id=announcement_id).update(
                title=title,
                content=content
            )

        except (ValueError, Exception):
            messages.add_message(request, messages.ERROR, 'Invalid fields')

        return redirect(
            reverse(
                'contest:contest-announcements',
                kwargs={'contest_id': self.kwargs.get('contest_id')}
            )
        )


class ContestAnnouncementDeleteView(UserPassesTestMixin, SuccessMessageMixin, DeleteView):
    model = Announcement
    success_message = 'Announcement deleted successfully'

    def get_success_url(self):
        return reverse('contest:contest-announcements', kwargs={'contest_id': self.kwargs.get('contest_id')})

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def test_func(self):
        return self.get_contest().author == self.request.user

    def get(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


class ContestRegistrationTemplateView(UserPassesTestMixin, TemplateView):
    template_name = 'contest/contest_registration.html'

    def get_contest(self):
        return get_object_or_404(Contest, id=self.kwargs.get('contest_id'))

    def test_func(self):
        return self.request.user.is_authenticated and self.request.user and self.get_contest().state == 'Upcoming'

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


class ContestDetailView(DetailView):
    template_name = 'contest/contest_detail.html'
    model = Contest
    context_object_name = 'contest'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_time = timezone.now()
        contest_time = context['contest'].start_time
        context['finished'] = context['contest'].start_time + context['contest'].duration

        if current_time > contest_time:
            context['started'] = True
        else:
            context['started'] = False

        if context['finished'] < current_time:
            context['finished'] = True
        else:
            context['finished'] = False

        return context