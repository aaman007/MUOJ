from django.views.generic import ListView
from django.http import JsonResponse
from blog.models import Blog
from contest.models import Contest
from accounts.models import Profile
from django.contrib import messages


class HomeView(ListView):
    model = Blog
    paginate_by = 5
    context_object_name = 'blogs'
    ordering = ['-created_at']
    template_name = 'core/home.html'

    def get_queryset(self):
        return Blog.objects.filter(preference=True)

    def post(self, request, *args, **kwargs):
        try:
            if 'term' in request.Get:
                qs = Profile.objects.filter(user__username_istartswith=request.Get.get('term'))
                users = list()
                for user in qs:
                    users.append(user.username)
                return JsonResponse(users, safe=False)
        except (ValueError, Exception):
            messages.add_message(request, messages.ERROR, 'No User')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'home_nav': 'active',
            'upcoming_contest': Contest.objects.upcoming_contests(self.request.user.username)
        })
        return context
