from rest_framework import serializers

from django.utils.translation import gettext_lazy as _


class ApplyRatingSerializer(serializers.Serializer):
    contest_id = serializers.IntegerField(label=_('Contest Id'))

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
