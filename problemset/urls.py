from django.urls import path

from problemset.views import (
    ProblemListView,
    ProblemDetailView,
    SubmissionListView,
    SubmissionCreateView,
    StandingsListView
)

app_name = 'problemset'

urlpatterns = [
    # Problems
    path('problems/', ProblemListView.as_view(), name='problem-list'),
    path('problems/<int:pk>/', ProblemDetailView.as_view(), name='problem-details'),

    # Submissions
    path('submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('problems/<int:problem_id>/submit/', SubmissionCreateView.as_view(), name='submission-create'),

    # Standings
    path('standings/', StandingsListView.as_view(), name='standings')
]
