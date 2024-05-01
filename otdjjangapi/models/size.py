from django.db import models


class Size(models.Model):
    size = models.CharField(max_length=10)
