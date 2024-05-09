from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    name = models.CharField(max_length=155)
    brand = models.ForeignKey("Brand", on_delete=models.CASCADE)
    type = models.ForeignKey("Type", on_delete=models.CASCADE)
    image = models.ImageField(upload_to='article_imgs/')
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
