import django_tables2 as tables
from django_tables2.utils import A

from binanalyze.models import Item, Bin, ShippingOrder, ShippingOrderItem

class ItemTable(tables.Table):
    # LinkColumn is passed pk into the link using A (accessor)
    # TemplateColumn renders template on each row. record is an automatically passed context
    name = tables.LinkColumn('binanalyze:item-detail', text=lambda item:item.name, args=[A('pk')])
    delete = tables.TemplateColumn(template_name= 'binanalyze/item/partials/in-table-delete.html')

    class Meta:
        model = Item
        fields = ['unitlength', 'length', 'width', 'height', 'unitweight', 'weight']
        sequence = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight', 'delete']

# Bins should be almost identical to items
class BinTable(tables.Table):
    # LinkColumn is passed pk into the link using A (accessor)
    # TemplateColumn renders template on each row. record is an automatically passed context
    name = tables.LinkColumn('binanalyze:bin-detail', text=lambda bin:bin.name, args=[A('pk')])
    delete = tables.TemplateColumn(template_name= 'binanalyze/bin/partials/in-table-delete.html')

    class Meta:
        model = Bin
        fields = ['unitlength', 'length', 'width', 'height', 'unitweight', 'weight']
        sequence = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight', 'delete']

class ShippingOrderTable(tables.Table):
    name = tables.LinkColumn('binanalyze:shippingorder-detail', text=lambda shippingorder:shippingorder.name, args=[A('pk')])
    delete = tables.TemplateColumn(template_name= 'binanalyze/shippingorder/partials/in-table-delete.html')
    
    class Meta:
        model = ShippingOrder
        fields = ['order_date']
        sequence = ['name', 'order_date', 'delete']

# Consider having items link to the item detail
class ShippingOrderItemTable(tables.Table):
    delete = tables.TemplateColumn(template_name= 'binanalyze/shippingorder/partials/in-table-item-delete.html')

    class Meta:
        model = ShippingOrderItem
        fields = ['shippingorder', 'item', 'quantity']
        sequence = ['shippingorder', 'item', 'quantity', 'delete']


class PackResultTable(tables.Table):
    shippingorder_name = tables.Column()
    pack_status = tables.Column()
    bin_name = tables.Column()
    volume_difference = tables.Column()
    weight_difference = tables.Column()
    volume_utilization = tables.Column()
    weight_utilization = tables.Column()
