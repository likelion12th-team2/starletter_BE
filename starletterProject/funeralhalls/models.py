from django.db import models
from multiselectfield import MultiSelectField


class FuneralHall(models.Model):
    original_id = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    location = models.CharField(max_length=100)
    contact = models.CharField(max_length=30, blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    TAG_CHOICES = (
        ('장례', '장례'), # funeral
        ('화장', '화장'), # cremation
        ('건조', '건조'), # drying
        ('봉안', '봉안') # enshrined
    )
    tag = MultiSelectField(choices=TAG_CHOICES)
    # https://pypi.org/project/django-multiselectfield/

    image = models.ImageField(null=True, upload_to='funeralhalls/')

    def __str__(self):
        return self.name