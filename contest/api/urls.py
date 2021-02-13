from django.urls import path, include

app_name = 'contest-api'

urlpatterns = [
    path('', include('contest.api.base.urls')),
    path('v1/', include('contest.api.v1.urls'))
]
