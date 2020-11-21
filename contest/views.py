from django.views.generic import (
    ListView
)

from contest.models import Contest


class ContestListView(ListView):
    model = Contest
    template_name = 'contest/contest_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'contest_nav': 'active'
        })
        return context
