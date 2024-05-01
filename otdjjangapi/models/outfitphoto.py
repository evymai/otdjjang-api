from django.db import models


class OutfitPhoto(models.Model):
    outfit = models.ForeignKey("Outfit", on_delete=models.SET_NULL, null=True)
    worn_on = models.DateTimeField()
    image_url = models.URLField(null=True)
