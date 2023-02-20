from decimal import Decimal

from django.db import models

class WeightMixin(models.Model):
    class UnitWeight(models.TextChoices):
        POUND = 'lb'
        GRAM = 'g'
        KILOGRAM = 'kg'
        
    weightconversion = {
        UnitWeight.POUND : Decimal('0.4535'),
        UnitWeight.GRAM : Decimal('0.001'),
        UnitWeight.KILOGRAM : Decimal('1'),
    }

    unitweight = models.CharField(max_length= 2, choices= UnitWeight.choices, default= UnitWeight.GRAM)
    weight = models.DecimalField(max_digits=8, decimal_places=4, default=0)

    class Meta:
        abstract = True

    def get_weight(self, in_kg=False):
        if in_kg==False:
            return self.weight
        
        return self.weight * self.weightconversion[self.unitweight]