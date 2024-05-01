from django.db import models


class UserArticle(models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    article = models.ForeignKey("Article", on_delete=models.CASCADE)
    size = models.ForeignKey("Size", on_delete=models.SET_NULL)
    
 