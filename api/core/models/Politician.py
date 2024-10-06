from django.db import models
from .Profile import Profile
# comment
class Politician(models.Model):
    """
    Django model that represents a politician.
    """
    POLITICIAN_TYPES = {
        "R": "Republican",
        "D": "Democrat",
        "I": "Independent"
    }

    profile = models.ForeignKey(
        Profile,
        on_delete = models.RESTRICT
    )
    politician_type = models.CharField(max_length=20)
    politician_house = models.CharField(max_length=1, choices=POLITICIAN_TYPES)
