from django.db import models


class OutfitArticle(models.Model):
    outfit = models.ForeignKey("Outfit", on_delete=models.CASCADE)
    user_article = models.ForeignKey("UserArticle", on_delete=models.CASCADE)
