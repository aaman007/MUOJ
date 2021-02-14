from django.contrib.auth import get_user_model
from django.http import Http404
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response

from core.api.v1.serializers import ConstantSerializer
from core.models import Constant

User = get_user_model()


class GetRemoteConfigAPIView(GenericAPIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        key = request.query_params.get('key')
        constants = Constant.objects.filter(key__iexact=key, remote=True)

        if not constants.exists():
            raise Http404

        return Response({'value': constants.first().value}, status=status.HTTP_200_OK)


class GetApplicationConfigAPIView(GenericAPIView):
    authentication_classes = []

    def get(self, request, *args, **kwargs):
        constant_qs = Constant.objects.filter(remote=True)
        constant_serializer = ConstantSerializer(constant_qs, many=True)

        resp = {
            'constants': constant_serializer.data,
        }
        return Response(resp, status=status.HTTP_200_OK)
