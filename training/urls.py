from django.urls import path

from training.views import TrainingTemplateView

app_name = 'training'

urlpatterns = [
    path('', TrainingTemplateView.as_view(), name='training-list')
]
