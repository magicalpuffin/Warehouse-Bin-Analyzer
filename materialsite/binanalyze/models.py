from django.db import models
from django.urls import reverse
# Create your models here.

# Dimensions and weight, default?
# length, width, height
# Item name?
# Units
# Foreign key
class Item(models.Model):
    name = models.CharField(max_length=16, unique= True)
    length = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    height = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return reverse('binanalyze:item-detail', kwargs= {'pk': self.pk})
    
# Dimensions and weight
# Name
class Bin(models.Model):
    name = models.CharField(max_length=16, unique= True)
    length = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    width = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    height = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    weight = models.DecimalField(max_digits=6, decimal_places=2, default=0)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('binanalyze:bin-detail', kwargs= {'pk': self.pk})

# Models all SO, SO contain items which should be shipped together
# many to many, one shipment can have many items, one item can have many SO
# Total volume?
class ShippingOrder(models.Model):
    name = models.CharField(max_length=16, unique= True)
    order_date = models.DateTimeField()
    items = models.ManyToManyField(Item)

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('binanalyze:so-detail', kwargs= {'pk': self.pk})


