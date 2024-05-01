from django.db import models


class OutfitArticle(models.Model):
    outfit = models.ForeignKey("Outfit", on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    
 