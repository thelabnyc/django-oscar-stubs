from django.contrib import admin
from oscar.apps.order.abstract_models import PaymentEventQuantity as PaymentEventQuantity
from oscar.apps.order.models import (
    BillingAddress as BillingAddress,
)
from oscar.apps.order.models import (
    CommunicationEvent as CommunicationEvent,
)
from oscar.apps.order.models import (
    Line as Line,
)
from oscar.apps.order.models import (
    LineAttribute as LineAttribute,
)
from oscar.apps.order.models import (
    LinePrice as LinePrice,
)
from oscar.apps.order.models import (
    Order as Order,
)
from oscar.apps.order.models import (
    OrderDiscount as OrderDiscount,
)
from oscar.apps.order.models import (
    OrderNote as OrderNote,
)
from oscar.apps.order.models import (
    OrderStatusChange as OrderStatusChange,
)
from oscar.apps.order.models import (
    PaymentEvent as PaymentEvent,
)
from oscar.apps.order.models import (
    PaymentEventType as PaymentEventType,
)
from oscar.apps.order.models import (
    ShippingAddress as ShippingAddress,
)
from oscar.apps.order.models import (
    ShippingEvent as ShippingEvent,
)
from oscar.apps.order.models import (
    ShippingEventType as ShippingEventType,
)
from oscar.apps.order.models import (
    Surcharge as Surcharge,
)

class LineInline(admin.TabularInline): ...
class OrderAdmin(admin.ModelAdmin): ...
class LineAdmin(admin.ModelAdmin): ...
class LinePriceAdmin(admin.ModelAdmin): ...
class ShippingEventTypeAdmin(admin.ModelAdmin): ...
class PaymentEventQuantityInline(admin.TabularInline): ...
class PaymentEventAdmin(admin.ModelAdmin): ...
class PaymentEventTypeAdmin(admin.ModelAdmin): ...
class OrderDiscountAdmin(admin.ModelAdmin): ...
class SurchargeAdmin(admin.ModelAdmin): ...
