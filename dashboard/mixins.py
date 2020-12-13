from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic import TemplateView

from contest.models import Contest


class ContestActionMixin(UserPassesTestMixin, TemplateView):
    template_name = 'dashboard/snippets/render_problems.html'

    def get_object(self):
        return Contest.objects.get(id=self.request.POST.get('contest_id'))

    def test_func(self):
        return self.get_object().author == self.request.user
