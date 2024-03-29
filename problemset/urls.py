from django.urls import path

from problemset.views import (
    ProblemListView,
    ProblemDetailView,
    SubmissionListView,
    SubmissionCreateView,
    SubmissionDetailView,
    StandingsListView,
    ProblemCreateView,
    ProblemUpdateView,
    TestCaseCreateView,
    TestCaseListView,
    TestCaseDeleteView,
)

app_name = 'problemset'

urlpatterns = [
    # Problems
    path('problems/', ProblemListView.as_view(), name='problem-list'),
    path('problems/<int:pk>/', ProblemDetailView.as_view(), name='problem-details'),
    path('problems/new/', ProblemCreateView.as_view(), name='add-problem'),
    path('problems/<int:pk>/problem-update/', ProblemUpdateView.as_view(), name='problem-update'),
    path('problems/<int:pk>/test-cases', TestCaseListView.as_view(), name='testcase-list'),
    path('problems/<int:pk>/add-test-case', TestCaseCreateView.as_view(), name='add-testcase'),
    path('problems/<int:problem_id>/test-cases/<int:pk>/delete', TestCaseDeleteView.as_view(), name='delete-testcase'),

    # Submissions
    path('submissions/', SubmissionListView.as_view(), name='submission-list'),
    path('submissions/<int:pk>/', SubmissionDetailView.as_view(), name='submission-details'),
    path('problems/<int:problem_id>/submit/', SubmissionCreateView.as_view(), name='submission-create'),

    # Standings
    path('standings/', StandingsListView.as_view(), name='standings')


]
