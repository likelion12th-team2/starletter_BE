from django.db import models

class Market(models.Model):
    original_id = models.PositiveIntegerField()
    name = models.CharField(max_length=50)
    discount = models.IntegerField(null=True)
    before_discount = models.IntegerField(null=True)
    price = models.IntegerField(default=0)
    image = models.URLField(blank=True, null=True)
    link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.name