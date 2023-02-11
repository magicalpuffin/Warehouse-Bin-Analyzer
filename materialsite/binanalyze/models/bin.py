from .mixinmodels.dimensionalmixin import DimensionalMixin
from .mixinmodels.weightmixin import WeightMixin

from django.db import models
from django.urls import reverse

class Bin(DimensionalMixin, WeightMixin):
    name = models.CharField(max_length=32, unique= True)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('binanalyze:bin-detail', kwargs= {'pk': self.pk})