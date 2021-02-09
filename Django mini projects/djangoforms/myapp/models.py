from django.db import models


# Create your models here.
class Snippet(models.Model):
    name_model = models.CharField(max_length=100)
    body_model = models.TextField()

    def __str__(self):
        return self.name_model
