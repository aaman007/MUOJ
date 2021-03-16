from rest_framework import status
from rest_framework.generics import GenericAPIView

from django.contrib.auth import get_user_model
from rest_framework.response import Response

User = get_user_model()


class AutoCompleteGenericAPIView(GenericAPIView):
    def get(self, request, *args, **kwargs):
        username = request.GET.get('term', '')
        users_qs = User.objects.filter(username__icontains=username)[:10]

        if not users_qs.exists():
            return Response({'detail': 'No users found with this username'}, status=status.HTTP_400_BAD_REQUEST)

        results = []
        for user in users_qs:
            results.append({
                'id': user.id,
                'label': user.username,
                'value': user.username
            })
        return Response(results, status=status.HTTP_200_OK)