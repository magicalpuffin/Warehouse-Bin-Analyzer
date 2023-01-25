# File used to manage commands being run in shell
# Needs to be in materialsite directory to run correctly
# Needs to be run through py manage.py shell instead of just py

from binanalyze.models import Item, Bin, ShippingOrder

Item.objects.all()
itm1 = Item(name= 'item1', length= 1, width = 2, height = 3, weight= 0.5)
itm2 = Item(name= 'item2', length= 12, width = 31, height = 66)
itm3 = Item(name= 'item3')

# items must be saved before being able to be set in a many to many relation
itm1.save()
itm2.save()
itm3.save()

itm1 = Item.objects.get(pk = 2)
itm2 = Item.objects.get(pk = 3)


so1 = ShippingOrder.objects.first()

# adding to many to many relation
so1.items.add(itm1, itm2)
so1.items.all()

so1.items.remove(itm2)
so1.items.all()

# figuring out how to put this stuff into a dataframe will be pain
# or changing the format of the bin packing to use other data types
# i guess there is basic functionality...
# I want to make unit tests but there isn't anything to test yet...
# many to many is already built into django orm