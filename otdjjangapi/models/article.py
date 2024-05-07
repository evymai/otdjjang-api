from django.db import models
from django.contrib.auth.models import User
from .brand import Brand
from .type import Type


class Article(models.Model):
    name = models.CharField(max_length=155)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    image_url = models.URLField(null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
