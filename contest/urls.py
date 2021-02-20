from django.urls import path

from contest.views import (
    RunningContestListView,
    UpcomingContestListView,
    PastContestListView,
    ContestProblemListView,
    ContestMySubmissionListView,
    ContestStandingsListView,
    ContestProblemDetails,
    ClarificationCreateView,
    ContestRegistrationTemplateView,
    ContestSubmissionCreateView,
    ContestAnnouncementsListView,
    ContestAnnouncementCreateView,
    ContestAnnouncementTemplateView,
    ContestAnnouncementDeleteView,
    ClarificationReplyView,
    ContestDetailView
)

app_name = 'contest'

urlpatterns = [
    path('running/', RunningContestListView.as_view(), name='running-contest-list'),
    path('upcoming/', UpcomingContestListView.as_view(), name='upcoming-contest-list'),
    path('past-contests/', PastContestListView.as_view(), name='past-contest-list'),
    path('<int:pk>/', ContestDetailView.as_view(), name='contest-details'),
    path('<int:contest_id>/problems/', ContestProblemListView.as_view(), name='contest-problems'),
    path('<int:contest_id>/problems/<int:pk>', ContestProblemDetails.as_view(), name='contest-problem-details'),
    path('<int:contest_id>/problems/<int:problem_id>/submit/', ContestSubmissionCreateView.as_view(),
         name='contest-submission'),
    path('<int:contest_id>/my-submissions/', ContestMySubmissionListView.as_view(), name='contest-my-submissions'),
    path('<int:contest_id>/register/', ContestRegistrationTemplateView.as_view(), name='contest-registration'),
    path('<int:contest_id>/standings/', ContestStandingsListView.as_view(), name='contest-standings'),
    path('<int:contest_id>/announcements/', ContestAnnouncementsListView.as_view(), name='contest-announcements'),
    path('<int:contest_id>/announcements/new/', ContestAnnouncementCreateView.as_view(), name='announcement-create'),
    path('<int:contest_id>/announcements/update/', ContestAnnouncementTemplateView.as_view(),
         name='announcement-update'),
    path('<int:contest_id>/announcements/<int:pk>/delete/', ContestAnnouncementDeleteView.as_view(),
         name='announcement-delete'),

    path('<int:contest_id>/problems/ask-question/', ClarificationCreateView.as_view(), name='ask-question'),
    path('<int:contest_id>/problems/clarification/<int:pk>/reply/', ClarificationReplyView.as_view(),
         name='reply-question')
]
