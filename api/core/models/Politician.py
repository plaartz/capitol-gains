# pylint: disable=too-few-public-methods
from django.db import models
from .Profile import Profile

class Politician(models.Model):
    """
    Django model that represents a politician.
    """

    profile = models.ForeignKey(
        Profile,
        on_delete = models.RESTRICT
    )
    politician_type = models.CharField(max_length=20)
    politician_house = models.CharField(
        max_length = 1,
        choices = [
            ("R", "Republican"),
            ("D", "Democrat"),
            ("I", "Independent")
        ]
    )
