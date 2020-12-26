from django.urls import path

from contest.views import (
    RunningContestListView,
    UpcomingContestListView,
    PastContestListView,
    ContestProblemListView,
    ContestMySubmissionListView,
    ContestStandingsListView,
    ContestRegistrationTemplateView
)

app_name = 'contest'

urlpatterns = [
    path('running/', RunningContestListView.as_view(), name='running-contest-list'),
    path('upcoming/', UpcomingContestListView.as_view(), name='upcoming-contest-list'),
    path('past-contests/', PastContestListView.as_view(), name='past-contest-list'),

    path('<int:contest_id>/problems/', ContestProblemListView.as_view(), name='contest-problems'),
    path('<int:contest_id>/my-submissions/', ContestMySubmissionListView.as_view(), name='contest-my-submissions'),
    path('<int:contest_id>/standings/', ContestStandingsListView.as_view(), name='contest-standings'),
    path('<int:contest_id>/register/', ContestRegistrationTemplateView.as_view(), name='contest-registration'),
]
