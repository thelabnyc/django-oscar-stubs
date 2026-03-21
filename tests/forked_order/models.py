from oscar.apps.address.abstract_models import AbstractBillingAddress, AbstractShippingAddress
from oscar.apps.order.abstract_models import (
    AbstractCommunicationEvent,
    AbstractLine,
    AbstractLineAttribute,
    AbstractLinePrice,
    AbstractOrder,
    AbstractOrderDiscount,
    AbstractOrderLineDiscount,
    AbstractOrderNote,
    AbstractOrderStatusChange,
    AbstractPaymentEvent,
    AbstractPaymentEventType,
    AbstractShippingEvent,
    AbstractShippingEventType,
    AbstractSurcharge,
)


class Order(AbstractOrder):
    class Meta(AbstractOrder.Meta):
        app_label = "order"


class OrderNote(AbstractOrderNote):
    class Meta(AbstractOrderNote.Meta):
        app_label = "order"


class OrderStatusChange(AbstractOrderStatusChange):
    class Meta(AbstractOrderStatusChange.Meta):
        app_label = "order"


class CommunicationEvent(AbstractCommunicationEvent):
    class Meta(AbstractCommunicationEvent.Meta):
        app_label = "order"


class ShippingAddress(AbstractShippingAddress):
    class Meta(AbstractShippingAddress.Meta):
        app_label = "order"


class BillingAddress(AbstractBillingAddress):
    class Meta(AbstractBillingAddress.Meta):
        app_label = "order"


class Line(AbstractLine):
    class Meta(AbstractLine.Meta):
        app_label = "order"


class LinePrice(AbstractLinePrice):
    class Meta(AbstractLinePrice.Meta):
        app_label = "order"


class LineAttribute(AbstractLineAttribute):
    class Meta(AbstractLineAttribute.Meta):
        app_label = "order"


class ShippingEvent(AbstractShippingEvent):
    class Meta(AbstractShippingEvent.Meta):
        app_label = "order"


class ShippingEventType(AbstractShippingEventType):
    class Meta(AbstractShippingEventType.Meta):
        app_label = "order"


class PaymentEvent(AbstractPaymentEvent):
    class Meta(AbstractPaymentEvent.Meta):
        app_label = "order"


class PaymentEventType(AbstractPaymentEventType):
    class Meta(AbstractPaymentEventType.Meta):
        app_label = "order"


class OrderDiscount(AbstractOrderDiscount):
    class Meta(AbstractOrderDiscount.Meta):
        app_label = "order"


class OrderLineDiscount(AbstractOrderLineDiscount):
    class Meta(AbstractOrderLineDiscount.Meta):
        app_label = "order"


class Surcharge(AbstractSurcharge):
    class Meta(AbstractSurcharge.Meta):
        app_label = "order"
