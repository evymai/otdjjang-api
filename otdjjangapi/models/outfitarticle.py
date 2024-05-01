from django.db import models
from .outfit import Outfit
from .userarticle import UserArticle


class OutfitArticle(models.Model):
    outfit = models.ForeignKey("Outfit", on_delete=models.CASCADE)
    user_article = models.ForeignKey("UserArticle", on_delete=models.CASCADE)
