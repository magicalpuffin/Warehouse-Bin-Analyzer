from .item import Item

from django.db import models
from django.urls import reverse

class ShippingOrder(models.Model):
    name = models.CharField(max_length=32, unique= True)
    order_date = models.DateTimeField()
    items = models.ManyToManyField(Item, through= 'ShippingOrderItem')

    def __str__(self) -> str:
        return self.name
    
    def get_absolute_url(self):
        return reverse('binanalyze:shippingorder-detail', kwargs= {'pk': self.pk})

# Extra fields for ManyToManyField to track quantity of each item
class ShippingOrderItem(models.Model):
    shippingorder = models.ForeignKey(ShippingOrder, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default= 1)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields= ['shippingorder', 'item'], name= 'unique shippingorder item')
        ]
