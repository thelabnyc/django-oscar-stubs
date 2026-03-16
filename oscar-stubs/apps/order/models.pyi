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

class Order(AbstractOrder): ...
class OrderNote(AbstractOrderNote): ...
class OrderStatusChange(AbstractOrderStatusChange): ...
class CommunicationEvent(AbstractCommunicationEvent): ...
class ShippingAddress(AbstractShippingAddress): ...
class BillingAddress(AbstractBillingAddress): ...
class Line(AbstractLine): ...
class LinePrice(AbstractLinePrice): ...
class LineAttribute(AbstractLineAttribute): ...
class ShippingEvent(AbstractShippingEvent): ...
class ShippingEventType(AbstractShippingEventType): ...
class PaymentEvent(AbstractPaymentEvent): ...
class PaymentEventType(AbstractPaymentEventType): ...
class OrderDiscount(AbstractOrderDiscount): ...
class OrderLineDiscount(AbstractOrderLineDiscount): ...
class Surcharge(AbstractSurcharge): ...
