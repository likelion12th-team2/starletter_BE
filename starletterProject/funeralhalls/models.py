from django.db import models
from multiselectfield import MultiSelectField


class FuneralHall(models.Model):
    original_id = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=30)
    link = models.URLField()

    TAG_CHOICES = (
        ('FU', '장례'), # funeral
        ('CR', '화장'), # cremation
        ('DR', '건조'), # drying
        ('EN', '봉안') # enshrined
    )
    tag = MultiSelectField(choices=TAG_CHOICES)
    # https://pypi.org/project/django-multiselectfield/

    def __str__(self):
        return self.name