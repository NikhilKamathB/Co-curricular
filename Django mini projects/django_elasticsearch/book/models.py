from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):

    name = models.CharField(max_length=150)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Book(models.Model):

    name = models.CharField(max_length=150)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, related_name='book_author')
    tags = models.ManyToManyField(Tag, related_name='book_tag')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name