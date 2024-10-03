from django.db import models
from . import Profile

class Politician(models.Model):
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
