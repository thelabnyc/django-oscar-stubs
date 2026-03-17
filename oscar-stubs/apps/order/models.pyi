from oscar.apps.address.abstract_models import (
    AbstractBillingAddress as AbstractBillingAddress,
)
from oscar.apps.address.abstract_models import (
    AbstractShippingAddress as AbstractShippingAddress,
)
from oscar.apps.order.abstract_models import (
    AbstractCommunicationEvent as AbstractCommunicationEvent,
)
from oscar.apps.order.abstract_models import (
    AbstractLine as AbstractLine,
)
from oscar.apps.order.abstract_models import (
    AbstractLineAttribute as AbstractLineAttribute,
)
from oscar.apps.order.abstract_models import (
    AbstractLinePrice as AbstractLinePrice,
)
from oscar.apps.order.abstract_models import (
    AbstractOrder as AbstractOrder,
)
from oscar.apps.order.abstract_models import (
    AbstractOrderDiscount as AbstractOrderDiscount,
)
from oscar.apps.order.abstract_models import (
    AbstractOrderLineDiscount as AbstractOrderLineDiscount,
)
from oscar.apps.order.abstract_models import (
    AbstractOrderNote as AbstractOrderNote,
)
from oscar.apps.order.abstract_models import (
    AbstractOrderStatusChange as AbstractOrderStatusChange,
)
from oscar.apps.order.abstract_models import (
    AbstractPaymentEvent as AbstractPaymentEvent,
)
from oscar.apps.order.abstract_models import (
    AbstractPaymentEventType as AbstractPaymentEventType,
)
from oscar.apps.order.abstract_models import (
    AbstractShippingEvent as AbstractShippingEvent,
)
from oscar.apps.order.abstract_models import (
    AbstractShippingEventType as AbstractShippingEventType,
)
from oscar.apps.order.abstract_models import (
    AbstractSurcharge as AbstractSurcharge,
)
from oscar.apps.order.abstract_models import (
    PaymentEventQuantity as PaymentEventQuantity,
)
from oscar.apps.order.abstract_models import (
    ShippingEventQuantity as ShippingEventQuantity,
)

class Order(AbstractOrder):
    id: int

class OrderNote(AbstractOrderNote):
    id: int

class OrderStatusChange(AbstractOrderStatusChange):
    id: int

class CommunicationEvent(AbstractCommunicationEvent):
    id: int

class ShippingAddress(AbstractShippingAddress):
    id: int

class BillingAddress(AbstractBillingAddress):
    id: int

class Line(AbstractLine):
    id: int

class LinePrice(AbstractLinePrice):
    id: int

class LineAttribute(AbstractLineAttribute):
    id: int

class ShippingEvent(AbstractShippingEvent):
    id: int

class ShippingEventType(AbstractShippingEventType):
    id: int

class PaymentEvent(AbstractPaymentEvent):
    id: int

class PaymentEventType(AbstractPaymentEventType):
    id: int

class OrderDiscount(AbstractOrderDiscount):
    id: int

class OrderLineDiscount(AbstractOrderLineDiscount):
    id: int

class Surcharge(AbstractSurcharge):
    id: int
