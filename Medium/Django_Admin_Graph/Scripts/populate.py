import sys

sys.path += [".."]

import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Django_Admin_Graph.settings")

import django

django.setup()

from App_1.models import *
from sklearn import datasets

def fillBostonTable():
    boston = datasets.load_boston()
    print(f"Begining to save from sklearn dataset...")
    BostonHousePriceDataset.objects.bulk_create(
        [   
            BostonHousePriceDataset(
                crim = instance[0],
                zn = instance[1],
                indus = instance[2],
                chas = instance[3],
                nox = instance[4],
                rm = instance[5],
                age = instance[6],
                dis = instance[7],
                rad = instance[8],
                tax = instance[9],
                ptratio = instance[10],
                b = instance[11],
                lstat = instance[12],
                price = boston.target[ind]
          ) for ind, instance in enumerate(boston.data)
        ]
    )
    print(f"Bulk saving done...")

fillBostonTable()