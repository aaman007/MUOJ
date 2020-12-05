from django.urls import reverse_lazy
from django.views.generic import (
    ListView,
    CreateView
)

from contest.forms import ContestForm
from contest.models import Contest


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


class ContestCreateView(CreateView):
    model = Contest
    form_class = ContestForm
    success_url = reverse_lazy('contest:upcoming-contest-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest_nav': 'active',
            'card_header': 'New Contest',
            'operation': 'Create'
        })
        return context

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
