# File used to manage commands being run in shell
# Needs to be in materialsite directory to run correctly
# Needs to be run through py manage.py shell instead of just py

import pandas as pd
from binanalyze.models import Item, Bin, ShippingOrder
from binanalyze.binpackfunctions import pack_SO

# uuhhhhhh the model 'Bin' would conflict with 'Bin' from p3dbp

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