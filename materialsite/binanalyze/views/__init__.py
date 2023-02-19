# This seems messy, not sure if splitting it up to multiple files would be worth it

from .analyze_views import AnalyzeView

from .bin_views import BinDetailView, BinUpdateView, BinCreateView, BinDeleteView

from .index_view import IndexView

from .item_views import table_item_create, table_item_delete
from .item_views import ItemListView, ItemDetailView, ItemUpdateView, ItemCreateView, ItemDeleteView

from .shippingorder_views import table_shippingorder_create, table_shippingorder_delete, table_shippingorderitem_create, table_shippingorderitem_delete
from .shippingorder_views import ShippingOrderListView, ShippingOrderUpdateView, ShippingOrderCreateView, ShippingOrderDetailView, ShippingOrderDeleteView