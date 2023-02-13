from decimal import Decimal
from datetime import datetime

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem

from django.test import TestCase
from django.utils import timezone

class ShippingOrderTests(TestCase):
    def setUp(self) -> None:
        so1 = ShippingOrder.objects.create(name= 'so1', order_date = timezone.make_aware(datetime(2022, 1, 1), timezone.get_current_timezone()))
        item_cm_g = Item.objects.create(name= 'item_cm_g', length= 1, width= 2, height= 3, weight= 4)
        item_m_kg = Item.objects.create(name= 'item_m_kg', unitlength= 'm', unitweight= 'kg', length= 5, width= 6, height= 7, weight= 8)
        item_ft_lb = Item.objects.create(name= 'item_ft_lb', unitlength= 'ft', unitweight= 'lb', length= 7, width= 8, height= 9, weight= 10)

        so1.items.add(item_cm_g, through_defaults= {'quantity': 1})
        so1.items.add(item_m_kg, through_defaults= {'quantity': 2})
        so1.items.add(item_ft_lb, through_defaults= {'quantity': 3})
    
    def test_through(self):
        so1 = ShippingOrder.objects.get(name = 'so1')
        item_cm_g = Item.objects.get(name = 'item_cm_g')
        item_m_kg = Item.objects.get(name = 'item_m_kg')
        item_ft_lb = Item.objects.get(name = 'item_ft_lb')

        self.assertQuerysetEqual(so1.items.all().order_by('name'), Item.objects.all().order_by('name'))

        self.assertEqual(ShippingOrderItem.objects.get(shippingorder= so1, item= item_cm_g).quantity, 1)
        self.assertEqual(ShippingOrderItem.objects.get(shippingorder= so1, item= item_m_kg).quantity, 2)
        self.assertEqual(ShippingOrderItem.objects.get(shippingorder= so1, item= item_ft_lb).quantity, 3)
