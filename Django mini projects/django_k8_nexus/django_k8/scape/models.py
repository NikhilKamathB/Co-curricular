from django.db import models


class ScapeModel(models.Model):

    class Meta:
        verbose_name_plural = "Scaple Model"
    
    name = models.CharField(max_length=100)
    file_data = models.FileField(upload_to='django_k8/scape/')