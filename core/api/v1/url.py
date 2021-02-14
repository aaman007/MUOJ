from django.urls import path

from core.api.v1.views import GetRemoteConfigAPIView, GetApplicationConfigAPIView

app_name = 'core-api-v1'

urlpatterns = [
    path('remote-config/', GetRemoteConfigAPIView.as_view(), name='remote-config'),
    path('application-config/', GetApplicationConfigAPIView.as_view(), name='application-config')
]
