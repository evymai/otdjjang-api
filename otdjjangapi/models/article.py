from django.db import models


class Article(models.Model):
    name = models.CharField(max_length=155)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    image_url = models.URLField(null=True)
