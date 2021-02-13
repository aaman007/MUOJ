from django.urls import path

from contest.api.base.views import ApplyRatingGenericAPIView

app_name = 'contest-api-base'

urlpatterns = [
    path('apply-rating/', ApplyRatingGenericAPIView.as_view(), name='apply-rating')
]
