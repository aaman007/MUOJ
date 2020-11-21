from django.urls import path

from contest.views import ContestListView

app_name = 'contest'

urlpatterns = [
    path('', ContestListView.as_view(), name='contest-list'),
]
