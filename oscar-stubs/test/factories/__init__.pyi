from decimal import Decimal
from typing import Any

from oscar.apps.basket.abstract_models import AbstractBasket
from oscar.apps.catalogue.abstract_models import AbstractProduct, AbstractProductImage
from oscar.apps.offer.abstract_models import AbstractConditionalOffer
from oscar.apps.order.abstract_models import AbstractOrder
from oscar.apps.partner.abstract_models import AbstractStockRecord
from oscar.apps.partner.strategy import PurchaseInfo
from oscar.apps.shipping.abstract_models import AbstractWeightBand, AbstractWeightBased
from oscar.apps.voucher.abstract_models import AbstractVoucher
from oscar.test.factories.address import CountryFactory as CountryFactory
from oscar.test.factories.address import UserAddressFactory as UserAddressFactory
from oscar.test.factories.basket import BasketFactory as BasketFactory
from oscar.test.factories.basket import (
    BasketLineAttributeFactory as BasketLineAttributeFactory,
)
from oscar.test.factories.catalogue import (
    AttributeOptionFactory as AttributeOptionFactory,
)
from oscar.test.factories.catalogue import (
    AttributeOptionGroupFactory as AttributeOptionGroupFactory,
)
from oscar.test.factories.catalogue import CategoryFactory as CategoryFactory
from oscar.test.factories.catalogue import OptionFactory as OptionFactory
from oscar.test.factories.catalogue import (
    ProductAttributeFactory as ProductAttributeFactory,
)
from oscar.test.factories.catalogue import (
    ProductAttributeValueFactory as ProductAttributeValueFactory,
)
from oscar.test.factories.catalogue import (
    ProductCategoryFactory as ProductCategoryFactory,
)
from oscar.test.factories.catalogue import ProductClassFactory as ProductClassFactory
from oscar.test.factories.catalogue import ProductFactory as ProductFactory
from oscar.test.factories.catalogue import ProductImageFactory as ProductImageFactory
from oscar.test.factories.catalogue import (
    ProductReviewFactory as ProductReviewFactory,
)
from oscar.test.factories.contrib import PermissionFactory as PermissionFactory
from oscar.test.factories.contrib import SiteFactory as SiteFactory
from oscar.test.factories.customer import (
    ProductAlertFactory as ProductAlertFactory,
)
from oscar.test.factories.customer import UserFactory as UserFactory
from oscar.test.factories.models import Band as Band
from oscar.test.factories.models import Member as Member
from oscar.test.factories.offer import BenefitFactory as BenefitFactory
from oscar.test.factories.offer import (
    ConditionalOfferFactory as ConditionalOfferFactory,
)
from oscar.test.factories.offer import ConditionFactory as ConditionFactory
from oscar.test.factories.offer import RangeFactory as RangeFactory
from oscar.test.factories.order import (
    BillingAddressFactory as BillingAddressFactory,
)
from oscar.test.factories.order import (
    OrderDiscountFactory as OrderDiscountFactory,
)
from oscar.test.factories.order import OrderFactory as OrderFactory
from oscar.test.factories.order import OrderLineFactory as OrderLineFactory
from oscar.test.factories.order import (
    ShippingAddressFactory as ShippingAddressFactory,
)
from oscar.test.factories.order import (
    ShippingEventFactory as ShippingEventFactory,
)
from oscar.test.factories.order import (
    ShippingEventTypeFactory as ShippingEventTypeFactory,
)
from oscar.test.factories.partner import PartnerFactory as PartnerFactory
from oscar.test.factories.partner import StockRecordFactory as StockRecordFactory
from oscar.test.factories.payment import SourceFactory as SourceFactory
from oscar.test.factories.payment import SourceTypeFactory as SourceTypeFactory
from oscar.test.factories.payment import TransactionFactory as TransactionFactory
from oscar.test.factories.voucher import VoucherFactory as VoucherFactory
from oscar.test.factories.voucher import VoucherSetFactory as VoucherSetFactory
from oscar.test.factories.wishlists import WishListFactory as WishListFactory

def create_stockrecord(
    product: Any = ...,
    price: Decimal | None = ...,
    partner_sku: str | None = ...,
    num_in_stock: int | None = ...,
    partner_name: str | None = ...,
    currency: str = ...,
    partner_users: list[Any] | None = ...,
) -> AbstractStockRecord: ...
def create_purchase_info(record: AbstractStockRecord) -> PurchaseInfo: ...
def create_product(
    upc: str | None = ...,
    title: str = ...,
    product_class: str = ...,
    partner_name: str | None = ...,
    partner_sku: str | None = ...,
    price: Decimal | None = ...,
    num_in_stock: int | None = ...,
    attributes: dict[str, Any] | None = ...,
    partner_users: list[Any] | None = ...,
    **kwargs: Any,
) -> AbstractProduct: ...
def create_product_image(
    product: Any = ...,
    original: Any = ...,
    caption: str = ...,
    display_order: int | None = ...,
) -> AbstractProductImage: ...
def create_basket(empty: bool = ...) -> AbstractBasket: ...
def create_order(
    number: str | None = ...,
    basket: AbstractBasket | None = ...,
    user: Any = ...,
    shipping_address: Any = ...,
    shipping_method: Any = ...,
    billing_address: Any = ...,
    total: Any = ...,
    **kwargs: Any,
) -> AbstractOrder: ...
def create_offer(
    name: str = ...,
    offer_type: str = ...,
    max_basket_applications: int | None = ...,
    product_range: Any = ...,
    condition: Any = ...,
    benefit: Any = ...,
    priority: int = ...,
    status: str | None = ...,
    start: Any = ...,
    end: Any = ...,
) -> AbstractConditionalOffer: ...
def create_voucher(**kwargs: Any) -> AbstractVoucher: ...
def create_shipping_weight_based(
    default_weight: Decimal = ...,
) -> AbstractWeightBased: ...
def create_shipping_weight_band(
    upper_limit: Decimal, charge: Decimal, weight_based: Any = ...
) -> AbstractWeightBand: ...
