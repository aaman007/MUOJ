from django.views.generic import (
    ListView
)

from problemset.models import Problem


class ProblemListView(ListView):
    model = Problem
    template_name = 'problem/problem_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'problemset_nav': 'active'
        })
        return context
