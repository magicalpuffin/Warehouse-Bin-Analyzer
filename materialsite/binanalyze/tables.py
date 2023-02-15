import django_tables2 as tables
from django_tables2.utils import A

from binanalyze.models import Item

class ItemTable(tables.Table):
    name = tables.LinkColumn('binanalyze:item-detail', text=lambda item:item.name, args=[A('id')])
    
    class Meta:
        model = Item
        template_name = "django_tables2/bootstrap.html"
        fields = ['unitlength', 'length', 'width', 'height', 'weight']
        sequence = ['name', 'unitlength', 'length', 'width', 'height', 'weight']