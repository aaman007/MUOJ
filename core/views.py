from django.views.generic import ListView

from blog.models import Blog
from contest.models import Contest


class HomeView(ListView):
    model = Blog
    paginate_by = 5
    context_object_name = 'blogs'
    ordering = ['-created_at']
    template_name = 'core/home.html'

    def get_queryset(self):
        return Blog.objects.filter(preference=True)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'home_nav': 'active',
            'upcoming_contest': Contest.objects.upcoming_contests(self.request.user.username)
        })
        return context
