import django_tables2 as tables
from django_tables2.utils import A

from binanalyze.models import Item, ShippingOrder, ShippingOrderItem

class ItemTable(tables.Table):
    # LinkColumn is passed pk into the link using A (accessor)
    # TemplateColumn renders template on each row. record is an automatically passed context
    name = tables.LinkColumn('binanalyze:item-detail', text=lambda item:item.name, args=[A('pk')])
    delete = tables.TemplateColumn(template_name= 'binanalyze/item/partials/in-table-delete.html')

    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ['unitlength', 'length', 'width', 'height', 'unitweight', 'weight']
        sequence = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight', 'delete']

# Bins should be almost identical to items
class BinTable(tables.Table):
    # LinkColumn is passed pk into the link using A (accessor)
    # TemplateColumn renders template on each row. record is an automatically passed context
    name = tables.LinkColumn('binanalyze:bin-detail', text=lambda bin:bin.name, args=[A('pk')])
    delete = tables.TemplateColumn(template_name= 'binanalyze/bin/partials/in-table-delete.html')

    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ['unitlength', 'length', 'width', 'height', 'unitweight', 'weight']
        sequence = ['name', 'unitlength', 'length', 'width', 'height', 'unitweight', 'weight', 'delete']

class ShippingOrderTable(tables.Table):
    name = tables.LinkColumn('binanalyze:shippingorder-detail', text=lambda shippingorder:shippingorder.name, args=[A('pk')])
    delete = tables.TemplateColumn(template_name= 'binanalyze/shippingorder/partials/in-table-delete.html')
    
    class Meta:
        model = ShippingOrder
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ['order_date']
        sequence = ['name', 'order_date', 'delete']

# Consider having items link to the item detail
class ShippingOrderItemTable(tables.Table):
    delete = tables.TemplateColumn(template_name= 'binanalyze/shippingorder/partials/in-table-item-delete.html')

    class Meta:
        model = ShippingOrderItem
        template_name = "django_tables2/bootstrap-responsive.html"
        fields = ['shippingorder', 'item', 'quantity']
        sequence = ['shippingorder', 'item', 'quantity', 'delete']
