from django.views.generic import TemplateView
from django.template.response import TemplateResponse

from blog.models import Blog


class TrainingTemplateView(TemplateView):
    template_name = 'training/training_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'training_nav': 'active'
        })
        return context


class TrainingDetailView(TemplateView):
    template_name = 'training/training_details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data()
        context.update({
            'training_nav': 'active',
            'blog': Blog.objects.get(pk=kwargs.get('pk'))
        })
        return context

    def post(self, *args, **kwargs):

        context = self.get_context_data(**kwargs)
        context.update({
            'code': self.request.POST.get('code'),
            'input': self.request.POST.get('input'),
            'output': self.request.POST.get('code') + self.request.POST.get('input')
        })
        return TemplateResponse(self.request, self.template_name, context)

