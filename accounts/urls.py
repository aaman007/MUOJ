from django.urls import path
from accounts.views import (
    UserListView,
    UserProfileView,
    UserSubmissionListView,
    UserBlogListView,
    UserContestListView,
    UserProblemSettingListView,
    ProblemCreateView,
    ProblemUpdateView,
    TestCaseCreateView
)

app_name = 'accounts'

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('user-submission-list/', UserSubmissionListView.as_view(), name='user-submission-list'),
    path('user-blog-list/', UserBlogListView.as_view(), name='user-blog-list'),
    path('user-contest-list/', UserContestListView.as_view(), name='user-contest-list'),
    path('user-problems-list/', UserProblemSettingListView.as_view(), name='user-problems-list'),
    path('add-problem/', ProblemCreateView.as_view(), name='add-problem'),
    path('problems/<int:pk>/problem-update/', ProblemUpdateView.as_view(), name='problem-update'),
    path('add-testcase/', TestCaseCreateView.as_view(), name='add-testcase'),
    path('<str:username>', UserProfileView.as_view(), name='user-profile')
]
