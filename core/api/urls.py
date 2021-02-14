from django.urls import path, include

app_name = 'core-api'

urlpatterns = [
    path('', include('core.api.base.urls')),
    path('v1/', include('core.api.v1.url'))
]
