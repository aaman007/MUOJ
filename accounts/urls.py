from django.urls import path
from accounts.views import (UserListView,
                            UserSubmissionListView,
                            UserBlogListView,
                            UserContestListView,)



app_name = 'accounts'

urlpatterns = [
    path('', UserListView.as_view(), name='user-list'),
    path('user-submission-list/', UserSubmissionListView.as_view(), name='user-submission-list'),
    path('user-blog-list/', UserBlogListView.as_view(), name='user-blog-list'),
    path('user-contest-list/', UserContestListView.as_view(), name='user-contest-list')
]
