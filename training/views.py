from django.views.generic import TemplateView


class TrainingTemplateView(TemplateView):
    template_name = 'training/training_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context.update({
            'training_nav': 'active'
        })
        return context

