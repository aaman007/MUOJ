from django.urls import path

from dashboard.views import (
    DashboardView,
    MyContestListView,
    ContestCreateView,
    ContestUpdateView,
    ContestDeleteView,
    ContestProblemListView,
    ContestAuthorListView,
    ContestStatisticsView,
    AddContestProblemAjaxView,
    RemoveContestProblemAjaxView,
    UserProblemSettingListView
)

app_name = 'dashboard'

urlpatterns = [
    path('', DashboardView.as_view(), name='dashboard'),

    # Problemset
    path('problemsetting/', UserProblemSettingListView.as_view(), name='user-problems-list'),

    # Contest
    path('contests/', MyContestListView.as_view(), name='my-contests'),
    path('contests/new/', ContestCreateView.as_view(), name='contest-create'),
    path('contests/<int:pk>/update/', ContestUpdateView.as_view(), name='contest-update'),
    path('contests/<int:pk>/delete/', ContestDeleteView.as_view(), name='contest-delete'),
    path('contests/<int:pk>/problems/', ContestProblemListView.as_view(), name='contest-problems'),
    path('contests/<int:pk>/authors/', ContestAuthorListView.as_view(), name='contest-authors'),
    path('contests/<int:pk>/statistics/', ContestStatisticsView.as_view(), name='contest-statistics'),

    # Ajax Views
    path('ajax/add-contest-problem/', AddContestProblemAjaxView.as_view(), name='ajax-add-contest-problem'),
    path('ajax/remove-contest-problem/', RemoveContestProblemAjaxView.as_view(), name='ajax-remove-contest-problem'),
]
