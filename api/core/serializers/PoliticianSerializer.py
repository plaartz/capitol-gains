# pylint: disable=missing-class-docstring, too-few-public-methods
from rest_framework import serializers
from core.models import Politician
from .ProfileSerializer import ProfileSerializer

class PoliticianSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()

    class Meta:
        model = Politician
        fields = ('politician_type', 'politician_house', 'profile')
