from django.urls import path

from accounts.api.v1.views import AutoCompleteGenericAPIView

app_name = 'accounts-api-v1'

urlpatterns = [
    path('autocomplete/', AutoCompleteGenericAPIView.as_view(), name='autocomplete')
]
