from django.urls import path

from core.views import HomeView

urlpatterns = [
    path('', HomeView.as_view(extra_context={'home': 'active'}), name='home')
]
