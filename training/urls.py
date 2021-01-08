from django.urls import path

from training.views import TutorialListView, TutorialDetailView

app_name = 'training'

urlpatterns = [
    path('', TutorialListView.as_view(), name='tutorial-list'),
    path('<int:pk>/', TutorialDetailView.as_view(), name='tutorial-details')
]
