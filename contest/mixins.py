from django.contrib import messages
from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse

from contest.models import Contest


class BaseContestFetch:
    def __init__(self):
        self.contest = None

    def get_contest(self):
        if self.contest:
            return self.contest
        kwargs = getattr(self, 'kwargs', {})
        self.contest = get_object_or_404(Contest, id=kwargs.get('contest_id'))
        return self.contest


class ContestantPassesTestMixin(BaseContestFetch, UserPassesTestMixin):
    def handle_no_permission(self):
        messages.add_message(self.request, messages.ERROR, 'Only registered users can view this')
        return redirect(reverse('contest:contest-standings', kwargs={'contest_id': self.kwargs.get('contest_id')}))

    def test_func(self):
        request = getattr(self, 'request')
        contest = self.get_contest()
        state = contest.state
        if request.user == contest.author:
            return True
        return state == 'Finished' or (state == 'Running' and request.user in contest.contestants.all())


class ModeratorPassesTestMixin(BaseContestFetch, UserPassesTestMixin):
    def test_func(self):
        request = getattr(self, 'request')
        return request.user == self.get_contest().author


class ContestAllowOrRedirectMixin(BaseContestFetch):
    def get(self, request, *args, **kwargs):
        if self.get_contest().state == 'Upcoming':
            messages.add_message(request, messages.ERROR, 'Contest has not started yet')
            return redirect(request.META.get('HTTP_REFERER', '/'))
        return getattr(super(), 'get')(request, *args, **kwargs)


class ContestRegisterOrRedirectMixin(BaseContestFetch):
    def get(self, request, *args, **kwargs):
        contest = self.get_contest()

        if not request.user.is_authenticated:
            return redirect(reverse('login'))

        elif contest.state != 'Upcoming':
            messages.add_message(request, messages.ERROR, 'You can only register for upcoming contests')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        elif request.user in contest.contestants.all():
            messages.add_message(request, messages.ERROR, 'You have already registered for this contest')
            return redirect(request.META.get('HTTP_REFERER', '/'))

        return getattr(super(), 'get')(request, *args, **kwargs)
