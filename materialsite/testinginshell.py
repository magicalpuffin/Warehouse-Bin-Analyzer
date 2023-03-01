# File used to manage commands being run in shell
# Needs to be in materialsite directory to run correctly

# How to access:
    # Opena a terminal in the docker container running the django app
    # Activate the django interactive console
# Example:
    # docker exec - it <container name> /bin/bash
    # python manage.py shell

import pandas as pd
from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem
from binanalyze.utils.py3dbp_wrapper import pack_SO
from django.utils import timezone

# 2023-02-6 Testing new database model
item1 = Item(name= 'Item1', unitlength = 'in', unitweight = 'lb', length= 1, width= 2, height= 3, weight = 4)
item2 = Item(name= 'Item2', unitlength = 'ft', unitweight = 'lb', length= 1, width= 0.5, height= 2, weight = 7)
item3 = Item(name= 'Item3', length= 5, width= 2.2222, height= 4.6623, weight = 25.125)
bin1 = Bin(name= 'Bin', length= 5, width= 10, height= 4, weight = 25)
so1 = ShippingOrder(name= 'SO1', order_date = timezone.now())

item1.get_dims()
item1.get_dims(True)
item1.get_volume()
item1.get_volume(True)
item1.get_weight()
item1.get_weight(True)

so1 = ShippingOrder.objects.get(name = 'SO1')
so1.items.add(item1, through_defaults= {'quantity': 2})
so1.items.add(item2, through_defaults= {'quantity': 3})
so1.items.all()

# 2023-02-20 Tesitng query and binpacking
Item.objects.all()
Bin.objects.all()
ShippingOrder.objects.all()
ShippingOrderItem.objects.all()

item1 = Item.objects.get(name= 'Item1')
so1 = ShippingOrder.objects.get(name = 'Shipping Order 1')

recordlist = []
for shippingorderitem in ShippingOrderItem.objects.all():
    rowdict = {
        'shippingorder_name':shippingorderitem.shippingorder.name,
        'quantity': shippingorderitem.quantity,
        'item_length': shippingorderitem.item.get_length(True),
        'item_width': shippingorderitem.item.get_width(True),
        'item_height': shippingorderitem.item.get_height(True),
        'item_weight': shippingorderitem.item.get_weight(True),
    }
    recordlist.append(rowdict)

binlist = []
for bin in Bin.objects.all():
    rowdict = {
        'bin_name':bin.name,
        'bin_length': bin.get_length(True),
        'bin_width': bin.get_width(True),
        'bin_height': bin.get_height(True),
        'bin_weight': bin.get_weight(True),
    }
    binlist.append(rowdict)

bin_df = pd.DataFrame.from_records(binlist)

so_df = pd.DataFrame.from_records(recordlist)
so_df = so_df.set_index('shippingorder_name')

result_df = so_df.groupby(level= 0).apply(pack_SO, bin_df=bin_df)

# Selects Shipping order, items and quantity
ShippingOrderItem.objects.filter(shippingorder = so1)
pd.DataFrame.from_records(ShippingOrderItem.objects.filter(shippingorder = so1).values('shippingorder__name', 'quantity', 'item__name', 'item__length', 'item__width', 'item__height', 'item__weight'))

# This was checking if bin packing works, the model has changed now and is outdated
soobjs = ShippingOrder.objects.all()
so_df = pd.DataFrame.from_records(soobjs.values('name', 'items__name', 'items__length', 'items__width', 'items__height', 'items__weight'))
so_df.columns = ['Shipment_Number', 'Item Number', 'Length', 'Width', 'Height', 'Weight']
so_df.loc[:, 'Quantity'] = 1
so_df = so_df.set_index('Shipment_Number')
so_df

binobjs = Bin.objects.all()
bin_df = pd.DataFrame.from_records(binobjs.values('name', 'length', 'width', 'height', 'weight'))
bin_df.columns = ['Bin Name', 'Length', 'Width', 'Height', 'Weight']
bin_df

result_df = so_df.groupby(level= 0).apply(pack_SO, bin_df=bin_df)