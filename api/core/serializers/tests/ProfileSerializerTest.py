import pytest
from core.models import Profile
from core.serializers import ProfileSerializer

def test_serialize_profile(db):
    # Create profile
    profile = Profile.objects.create(first_name = "Daven", last_name = "Thakkar", middle_initial = "C")

    profile_serialized = ProfileSerializer(profile)
    serialized_data = profile_serialized.data

    assert serialized_data['first_name'] == 'Daven'
    assert serialized_data['last_name'] == 'Thakkar'
    assert serialized_data['middle_initial'] == 'C'
    assert serialized_data['full_name'] == 'Daven C. Thakkar'


