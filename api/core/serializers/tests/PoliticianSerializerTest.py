import pytest
from core.models import Profile, Politician
from core.serializers import PoliticianSerializer

def test_serialize_politician(db):
    # Create profile
    profile = Profile.objects.create(first_name = "Daven", last_name = "Thakkar", middle_initial = "C")
    # Create politician 
    politician = Politician.objects.create(profile = profile, politician_type = "Senate", politician_house = "I")

    politician_serialized = PoliticianSerializer(politician)
    serialized_data = politician_serialized.data
    
    assert serialized_data['politician_type'] == 'Senate'
    assert serialized_data['politician_house'] == 'I'
    assert serialized_data['profile']['first_name'] == 'Daven'
    assert serialized_data['profile']['last_name'] == 'Thakkar'
    assert serialized_data['profile']['middle_initial'] == 'C'


