from django.urls import path
from accounts.views import (
    UserListView,
    UserProfileView,
    UserSubmissionListView,
    UserBlogListView,
    UserContestListView,
    profile_update_view,
)

app_name = 'accounts'

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('<str:username>/user-submission-list/', UserSubmissionListView.as_view(), name='user-submission-list'),
    path('<str:username>/user-blog-list/', UserBlogListView.as_view(), name='user-blog-list'),
    path('<str:username>/user-contest-list/', UserContestListView.as_view(), name='user-contest-list'),
    path('<str:username>/update-profile/', profile_update_view, name='update-profile'),
    path('<str:username>/', UserProfileView.as_view(), name='user-profile'),
]
