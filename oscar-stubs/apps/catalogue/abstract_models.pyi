from typing import Any, ClassVar

from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models.expressions import Combinable
from django.db.models.lookups import StartsWith
from django.utils.functional import cached_property
from oscar.apps.catalogue.product_attributes import ProductAttributesContainer
from oscar.apps.partner.abstract_models import AbstractStockRecord
from oscar.models.fields import AutoSlugField, NullCharField
from oscar.models.fields.slugfield import SlugField
from treebeard.mp_tree import MP_Node

class ReverseStartsWith(StartsWith):
    def process_rhs(self, qn: Any, connection: Any) -> Any: ...
    def process_lhs(self, compiler: Any, connection: Any, lhs: Any = ...) -> Any: ...

class AbstractProductClass(models.Model):
    name: models.CharField
    slug: AutoSlugField
    requires_shipping: models.BooleanField
    track_stock: models.BooleanField
    options: models.ManyToManyField[AbstractOption, AbstractOption]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

    @property
    def has_attributes(self) -> bool: ...

class AbstractCategory(MP_Node):
    COMPARISON_FIELDS: ClassVar[tuple[str, ...]]

    name: models.CharField
    code: NullCharField
    description: models.TextField
    long_description: models.TextField
    meta_title: models.CharField
    meta_description: models.TextField
    image: models.ImageField
    slug: SlugField
    exclude_from_menu: models.BooleanField
    is_public: models.BooleanField
    ancestors_are_public: models.BooleanField

    _slug_separator: ClassVar[str]
    _full_name_separator: ClassVar[str]

    objects: ClassVar[models.Manager[AbstractCategory]]  # type: ignore[assignment]

    @property
    def full_name(self) -> str: ...
    def get_full_slug(self, parent_slug: str | None = ...) -> str: ...
    @property
    def full_slug(self) -> str: ...
    def generate_slug(self) -> str: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def set_ancestors_are_public(self) -> None: ...
    def get_public_children(self) -> models.QuerySet[AbstractCategory]: ...
    @classmethod
    def fix_tree(cls, fix_paths: bool = ..., **kwargs: Any) -> None: ...  # type: ignore[override]
    def get_meta_title(self) -> str: ...
    def get_meta_description(self) -> str: ...
    def get_ancestors_and_self(self) -> list[AbstractCategory]: ...
    def get_descendants_and_self(self) -> models.QuerySet[AbstractCategory]: ...
    def get_url_cache_key(self) -> str: ...
    def _get_absolute_url(self, parent_slug: str | None = ...) -> str: ...
    def get_absolute_url(self) -> str: ...

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

    def has_children(self) -> bool: ...
    def get_num_children(self) -> int: ...

class AbstractProductCategory(models.Model):
    product: models.ForeignKey[AbstractProduct | Combinable, AbstractProduct]
    product_id: int
    category: models.ForeignKey[AbstractCategory | Combinable, AbstractCategory]
    category_id: int

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        unique_together: tuple[str, str]
        verbose_name: str
        verbose_name_plural: str

class AbstractProduct(models.Model):
    STANDALONE: ClassVar[str]
    PARENT: ClassVar[str]
    CHILD: ClassVar[str]
    STRUCTURE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    structure: models.CharField
    is_public: models.BooleanField
    upc: NullCharField
    parent: models.ForeignKey[AbstractProduct | None | Combinable, AbstractProduct | None]
    parent_id: int | None
    title: models.CharField
    slug: SlugField
    description: models.TextField
    meta_title: models.CharField
    meta_description: models.TextField
    priority: models.SmallIntegerField
    product_class: models.ForeignKey[AbstractProductClass | None | Combinable, AbstractProductClass | None]
    product_class_id: int | None
    attributes: models.ManyToManyField[AbstractProductAttribute, AbstractProductAttribute]
    product_options: models.ManyToManyField[AbstractOption, AbstractOption]
    recommended_products: models.ManyToManyField[AbstractProduct, AbstractProduct]
    rating: models.FloatField
    date_created: models.DateTimeField
    date_updated: models.DateTimeField
    categories: models.ManyToManyField[AbstractCategory, AbstractCategory]
    is_discountable: models.BooleanField
    code: models.CharField

    # Reverse relations
    children: models.Manager[AbstractProduct]
    stockrecords: models.Manager[AbstractStockRecord]

    attr: ProductAttributesContainer

    objects: ClassVar[models.Manager[AbstractProduct]]

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
    def get_absolute_url(self) -> str: ...
    def clean(self) -> None: ...
    def _clean_standalone(self) -> None: ...
    def _clean_child(self) -> None: ...
    def _clean_parent(self) -> None: ...
    def save(self, *args: Any, **kwargs: Any) -> None: ...
    def refresh_from_db(self, *args: Any, **kwargs: Any) -> None: ...
    @property
    def is_standalone(self) -> bool: ...
    @property
    def is_parent(self) -> bool: ...
    @property
    def is_child(self) -> bool: ...
    def can_be_parent(self, give_reason: bool = ...) -> bool | tuple[bool, str | None]: ...
    @property
    def options(self) -> models.QuerySet[AbstractOption]: ...
    @cached_property
    def has_options(self) -> bool: ...
    @property
    def is_shipping_required(self) -> bool: ...
    @property
    def has_stockrecords(self) -> bool: ...
    @property
    def num_stockrecords(self) -> int: ...
    @property
    def attribute_summary(self) -> str: ...
    def get_title(self) -> str: ...
    def get_meta_title(self) -> str: ...
    def get_meta_description(self) -> str: ...
    def get_product_class(self) -> AbstractProductClass | None: ...
    def get_public_children(self) -> models.QuerySet[AbstractProduct] | list[AbstractProduct]: ...
    def get_is_discountable(self) -> bool: ...
    def get_categories(self) -> models.QuerySet[AbstractCategory] | list[AbstractCategory]: ...
    def get_attribute_values(
        self,
    ) -> models.QuerySet[AbstractProductAttributeValue] | list[AbstractProductAttributeValue]: ...
    def get_missing_image(self) -> MissingProductImage: ...
    def get_all_images(self) -> models.QuerySet[AbstractProductImage]: ...
    def primary_image(self) -> AbstractProductImage | object: ...
    def update_rating(self) -> None: ...
    def calculate_rating(self) -> float | None: ...
    def has_review_by(self, user: User) -> bool: ...
    def is_review_permitted(self, user: User) -> bool: ...
    @cached_property
    def num_approved_reviews(self) -> int: ...
    @property
    def sorted_recommended_products(self) -> list[AbstractProduct]: ...
    def get_structure_display(self) -> str: ...

class AbstractProductRecommendation(models.Model):
    primary: models.ForeignKey[AbstractProduct | Combinable, AbstractProduct]
    primary_id: int
    recommendation: models.ForeignKey[AbstractProduct | Combinable, AbstractProduct]
    recommendation_id: int
    ranking: models.PositiveSmallIntegerField

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        unique_together: tuple[str, str]
        verbose_name: str
        verbose_name_plural: str

class AbstractProductAttribute(models.Model):
    product_class: models.ForeignKey[AbstractProductClass | None | Combinable, AbstractProductClass | None]
    product_class_id: int | None
    name: models.CharField
    code: models.SlugField

    TEXT: ClassVar[str]
    INTEGER: ClassVar[str]
    BOOLEAN: ClassVar[str]
    FLOAT: ClassVar[str]
    RICHTEXT: ClassVar[str]
    DATE: ClassVar[str]
    DATETIME: ClassVar[str]
    OPTION: ClassVar[str]
    MULTI_OPTION: ClassVar[str]
    ENTITY: ClassVar[str]
    FILE: ClassVar[str]
    IMAGE: ClassVar[str]
    TYPE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    type: models.CharField
    option_group: models.ForeignKey[
        AbstractAttributeOptionGroup | None | Combinable, AbstractAttributeOptionGroup | None
    ]
    option_group_id: int | None
    required: models.BooleanField

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str
        unique_together: tuple[str, str]

    @property
    def is_option(self) -> bool: ...
    @property
    def is_multi_option(self) -> bool: ...
    @property
    def is_file(self) -> bool: ...
    @property
    def is_entity(self) -> bool: ...
    def clean(self) -> None: ...
    def _get_value_obj(self, product: AbstractProduct, value: Any) -> Any: ...
    def _bind_value_file(self, value_obj: Any, value: Any) -> Any: ...
    def _bind_value_multi_option(self, value_obj: Any, value: Any) -> Any: ...
    def _bind_value(self, value_obj: Any, value: Any) -> Any: ...
    def bind_value(self, value_obj: Any, value: Any) -> Any: ...
    def save_value(self, product: AbstractProduct, value: Any) -> Any: ...
    def validate_value(self, value: Any) -> None: ...
    def _validate_text(self, value: Any) -> None: ...
    _validate_richtext: Any
    def _validate_float(self, value: Any) -> None: ...
    def _validate_integer(self, value: Any) -> None: ...
    def _validate_date(self, value: Any) -> None: ...
    def _validate_datetime(self, value: Any) -> None: ...
    def _validate_boolean(self, value: Any) -> None: ...
    def _validate_entity(self, value: Any) -> None: ...
    def _validate_multi_option(self, value: Any) -> None: ...
    def _validate_option(self, value: Any, valid_values: Any = ...) -> None: ...
    def _validate_file(self, value: Any) -> None: ...
    _validate_image: Any
    def get_type_display(self) -> str: ...

class AbstractProductAttributeValue(models.Model):
    attribute: models.ForeignKey[AbstractProductAttribute | Combinable, AbstractProductAttribute]
    attribute_id: int
    product: models.ForeignKey[AbstractProduct | Combinable, AbstractProduct]
    product_id: int
    value_text: models.TextField
    value_integer: models.IntegerField
    value_boolean: models.BooleanField
    value_float: models.FloatField
    value_richtext: models.TextField
    value_date: models.DateField
    value_datetime: models.DateTimeField
    value_multi_option: models.ManyToManyField[AbstractAttributeOption, AbstractAttributeOption]
    value_option: models.ForeignKey[AbstractAttributeOption | None | Combinable, AbstractAttributeOption | None]
    value_option_id: int | None
    value_file: models.FileField
    value_image: models.ImageField
    value_entity: GenericForeignKey
    entity_content_type: models.ForeignKey[ContentType | None | Combinable, ContentType | None]
    entity_content_type_id: int | None
    entity_object_id: models.PositiveIntegerField
    _dirty: bool

    @cached_property
    def type(self) -> str: ...
    @property
    def value_field_name(self) -> str: ...
    def _get_value(self) -> Any: ...
    def _set_value(self, new_value: Any) -> None: ...
    value: Any
    @property
    def is_dirty(self) -> bool: ...

    class Meta:
        abstract: bool
        app_label: str
        unique_together: tuple[str, str]
        verbose_name: str
        verbose_name_plural: str

    def summary(self) -> str: ...
    @property
    def value_as_text(self) -> Any: ...
    @property
    def _multi_option_as_text(self) -> str: ...
    @property
    def _option_as_text(self) -> str: ...
    @property
    def _richtext_as_text(self) -> str: ...
    @property
    def _entity_as_text(self) -> str: ...
    @property
    def _boolean_as_text(self) -> str: ...
    @property
    def value_as_html(self) -> Any: ...
    @property
    def _richtext_as_html(self) -> str: ...

class AbstractAttributeOptionGroup(models.Model):
    name: models.CharField
    code: NullCharField

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str

    @property
    def option_summary(self) -> str: ...

class AbstractAttributeOption(models.Model):
    group: models.ForeignKey[AbstractAttributeOptionGroup | Combinable, AbstractAttributeOptionGroup]
    group_id: int
    option: models.CharField
    code: NullCharField

    class Meta:
        abstract: bool
        app_label: str
        unique_together: tuple[str, str]
        verbose_name: str
        verbose_name_plural: str

class AbstractOption(models.Model):
    TEXT: ClassVar[str]
    INTEGER: ClassVar[str]
    FLOAT: ClassVar[str]
    BOOLEAN: ClassVar[str]
    DATE: ClassVar[str]
    SELECT: ClassVar[str]
    RADIO: ClassVar[str]
    MULTI_SELECT: ClassVar[str]
    CHECKBOX: ClassVar[str]
    TYPE_CHOICES: ClassVar[tuple[tuple[str, str], ...]]

    empty_label: ClassVar[str]
    empty_radio_label: ClassVar[str]

    name: models.CharField
    code: AutoSlugField
    type: models.CharField
    required: models.BooleanField
    option_group: models.ForeignKey[
        AbstractAttributeOptionGroup | None | Combinable, AbstractAttributeOptionGroup | None
    ]
    option_group_id: int | None
    help_text: models.CharField
    order: models.IntegerField

    @property
    def is_option(self) -> bool: ...
    @property
    def is_multi_option(self) -> bool: ...
    @property
    def is_select(self) -> bool: ...
    @property
    def is_radio(self) -> bool: ...
    def add_empty_choice(self, choices: list[tuple[Any, str]]) -> list[tuple[Any, str]]: ...
    def get_choices(self) -> list[tuple[Any, str]]: ...
    def clean(self) -> None: ...
    def get_type_display(self) -> str: ...

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

class MissingProductImage:
    name: str
    def __init__(self, name: str | None = ...) -> None: ...
    def symlink_missing_image(self, media_file_path: str) -> None: ...

class AbstractProductImage(models.Model):
    product: models.ForeignKey[AbstractProduct | Combinable, AbstractProduct]
    product_id: int
    code: NullCharField
    original: models.ImageField
    caption: models.CharField
    display_order: models.PositiveIntegerField
    date_created: models.DateTimeField

    class Meta:
        abstract: bool
        app_label: str
        ordering: list[str]
        verbose_name: str
        verbose_name_plural: str

    def is_primary(self) -> bool: ...
    def delete(self, *args: Any, **kwargs: Any) -> tuple[int, dict[str, int]]: ...

class AbstractProductCategoryHierarchy(models.Model):
    id: models.CharField  # type: ignore[assignment]
    product_id: models.IntegerField
    category_id: models.IntegerField

    class Meta:
        abstract: bool
        app_label: str
        verbose_name: str
        verbose_name_plural: str
        db_table: str
        managed: bool
