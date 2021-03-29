from .models import *
from django.contrib import admin


class BostonHousePriceDatasetAdmin(admin.ModelAdmin):
    
    list_display = ["id", "crim", "zn", "indus", "chas", "nox", "rm", "age", "dis", "rad", "tax", "ptratio", "b", "lstat", "price"]


admin.site.register(BostonHousePriceDataset, BostonHousePriceDatasetAdmin)