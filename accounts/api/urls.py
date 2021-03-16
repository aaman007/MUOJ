from django.urls import path, include

app_name = 'accounts-api'

urlpatterns = [
    path('v1/', include('accounts.api.v1.urls'))
]
