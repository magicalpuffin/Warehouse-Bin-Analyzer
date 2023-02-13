from .mixinmodels.dimensionalmixin import DimensionalMixin
from .mixinmodels.weightmixin import WeightMixin

from django.db import models
from django.urls import reverse

import pandas as pd

# Testing custom managers and query sets 
# class ItemQuerySet(models.QuerySet):
#     def to_df(self):
#         return pd.DataFrame.from_records(self.values('name', 'length', 'width', 'height', 'weight'))

# class ItemManager(models.Manager):
#     def get_queryset(self):
#         return ItemQuerySet(self.model, using= self._db)

class Item(DimensionalMixin, WeightMixin):
    name = models.CharField(max_length=32, unique= True)
    # objects = ItemManager()

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('binanalyze:item-detail', kwargs= {'pk': self.pk})