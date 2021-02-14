from rest_framework import serializers

from core.models import Constant


class ConstantSerializer(serializers.ModelSerializer):
    class Meta:
        model = Constant
        exclude = ['id', 'remote']
