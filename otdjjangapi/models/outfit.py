from django.db import models
from django.contrib.auth.models import User


class Outfit(models.Model):
    name = models.CharField(max_length=155)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
