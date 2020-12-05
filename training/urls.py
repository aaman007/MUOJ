from django.urls import path

from training.views import TrainingTemplateView, TrainingDetailView

app_name = 'training'

urlpatterns = [
    path('', TrainingTemplateView.as_view(), name='training-list'),
    path('<int:pk>/', TrainingDetailView.as_view(), name='training-details')
]
