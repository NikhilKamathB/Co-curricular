from django.db import models


class BostonHousePriceDataset(models.Model):

    CHAS = (
        (0, "Otherwise"),
        (1, "Tract bounds river")
    )

    class Meta:
        verbose_name = "Boston House Price Dataset"
        verbose_name_plural = "Boston House Price Dataset"

    crim = models.FloatField(null=True, blank=True, help_text="Per capital crime rate by town")
    zn = models.FloatField(null=True, blank=True, help_text="Proportion of residential land zoned for lots over 25,000 sq.ft")
    indus = models.FloatField(null=True, blank=True, help_text="Proportion of non-retail business acres per town")
    chas = models.IntegerField(choices=CHAS, null=True, blank=True, help_text="Charles River dummy variable")
    nox = models.FloatField(null=True, blank=True, help_text="Nitric oxides concentration (parts per 10 million)")
    rm = models.FloatField(null=True, blank=True, help_text="Average number of rooms per dwelling")
    age = models.FloatField(null=True, blank=True, help_text="Proportion of owner-occupied units built prior to 1940")
    dis = models.FloatField(null=True, blank=True, help_text="Weighted distances to five Boston employment centers")
    rad = models.IntegerField(null=True, blank=True, help_text="Index of accessibility to radial highways")
    tax = models.FloatField(null=True, blank=True, help_text="Full-value property-tax rate per 10,000 USD")
    ptratio = models.FloatField(null=True, blank=True, help_text="Pupil-teacher ratio by town")
    b = models.FloatField(null=True, blank=True, help_text="1000(Bk — 0.63)² where Bk is the proportion of blacks by town")
    lstat = models.FloatField(null=True, blank=True, help_text="Lower status of the population")
    price = models.FloatField(null=True, blank=True, help_text="Price")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"House instance {self.id}"