from decimal import Decimal

from binanalyze.models import Item

from django.test import TestCase

class ItemTests(TestCase):
    def setUp(self) -> None:
        Item.objects.create(name= 'item_cm_g', length= 1, width= 2, height= 3, weight= 4)
        # Item.objects.create(name= 'item_m_kg', unitlength= 'm', unitweight= 'kg', length= 5, width= 6, height= 7, weight= 8)
        # Item.objects.create(name= 'item_ft_lb', unitlength= 'ft', unitweight= 'lb', length= 7, width= 8, height= 9, weight= 10)
    
    def test_get(self):
        item_cm_g = Item.objects.get(name = 'item_cm_g')
        # item_m_kg = Item.objects.get(name = 'item_m_kg')
        # item_ft_lb = Item.objects.get(name = 'item_ft_lb')

        self.assertEqual(item_cm_g.get_length(), Decimal('1'))
        self.assertEqual(item_cm_g.get_width(), Decimal('2'))
        self.assertEqual(item_cm_g.get_height(), Decimal('3'))
        self.assertEqual(item_cm_g.get_length(in_meter= True), Decimal('0.01'))
        self.assertEqual(item_cm_g.get_width(in_meter= True), Decimal('0.02'))
        self.assertEqual(item_cm_g.get_height(in_meter= True), Decimal('0.03'))

        self.assertEqual(item_cm_g.get_dims(), [1, 2, 3])
        self.assertEqual(item_cm_g.get_dims(in_meter= True), [Decimal(x) for x in ['0.01', '0.02', '0.03']])

        self.assertEqual(item_cm_g.get_volume(), 6)
        self.assertEqual(item_cm_g.get_volume(in_meter= True), Decimal('0.000006'))

        self.assertEqual(item_cm_g.get_weight(), 4)
        self.assertEqual(item_cm_g.get_weight(in_kg= True), Decimal('0.004'))