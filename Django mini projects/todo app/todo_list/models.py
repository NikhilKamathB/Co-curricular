from django.db import models


# Create your models here.
# Create class -> make migarations -> push new migrations.
class TodoList(models.Model):

    item = models.CharField(max_length=200)
    completed = models.BooleanField(default=False)

    def __str__(self):
        return self.item
