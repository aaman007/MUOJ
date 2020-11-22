from django.urls import path

from problemset.views import (
    ProblemListView,
    SubmissionListView,
    StandingsListView
)

app_name = 'problemset'

urlpatterns = [
    path('problems/', ProblemListView.as_view(), name='problem-list'),
    path('submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('standings/', StandingsListView.as_view(), name='standings')
]
