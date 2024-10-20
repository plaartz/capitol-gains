# pylint: disable=missing-class-docstring, too-few-public-methods
from rest_framework import serializers
from core.models import Profile

class ProfileSerializer(serializers.ModelSerializer):
    full_name = serializers.ReadOnlyField()

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'middle_initial', 'full_name')
