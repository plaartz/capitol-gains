# pylint: disable=too-few-public-methods
from django.db import models

class Profile(models.Model):
    """
    Django model that represents a user's profile.
    """
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    middle_initial = models.CharField(max_length=1, null=True)

    @property
    def full_name(self):
        " Returns the profile's full name. "
        #pylint: disable=line-too-long
        return f'{self.first_name}{ " " + self.middle_initial + ". " if self.middle_initial else " "}{self.last_name}'
