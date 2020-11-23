from django.urls import path

from contest.views import (
    RunningContestListView,
    UpcomingContestListView,
    PastContestListView
)

app_name = 'contest'

urlpatterns = [
    path('running/', RunningContestListView.as_view(), name='running-contest-list'),
    path('upcoming/', UpcomingContestListView.as_view(), name='upcoming-contest-list'),
    path('past-contests/', PastContestListView.as_view(), name='past-contest-list'),
]
