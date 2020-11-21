from django.urls import path

from problemset.views import (
    ProblemListView
)

app_name = 'problemset'

urlpatterns = [
    path('', ProblemListView.as_view(), name='problem-list'),
]
