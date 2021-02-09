from django.db import models


# Create your models here.
class Stock(models.Model):
    quote = models.CharField(max_length=10)

    def __str__(self):
        return self.quote
