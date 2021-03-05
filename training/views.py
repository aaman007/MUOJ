from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView

from problemset.models import Problem
from training.models import Tutorial


class TutorialListView(LoginRequiredMixin, ListView):
    model = Tutorial
    template_name = 'training/tutorial_list.html'
    context_object_name = 'tutorials'

    def get_queryset(self):
        return Tutorial.objects.order_by('level')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'training_nav': 'active'
        })
        return context


class TutorialDetailView(UserPassesTestMixin, DetailView):
    model = Tutorial
    template_name = 'training/tutorial_details.html'
    context_object_name = 'tutorial'

    def test_func(self):
        user = self.request.user
        return user.is_authenticated and user.profile.levels_completed >= self.get_object().level

    def get_problems(self):
        return Problem.objects.filter(id__in=self.get_object().problem_ids)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'training_nav': 'active',
            'problems': self.get_problems()
        })
        return context

