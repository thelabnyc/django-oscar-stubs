from oscar.apps.catalogue.abstract_models import (
    AbstractAttributeOption as AbstractAttributeOption,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractAttributeOptionGroup as AbstractAttributeOptionGroup,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractCategory as AbstractCategory,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractOption as AbstractOption,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractProduct as AbstractProduct,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractProductAttribute as AbstractProductAttribute,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractProductAttributeValue as AbstractProductAttributeValue,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractProductCategory as AbstractProductCategory,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractProductCategoryHierarchy as AbstractProductCategoryHierarchy,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractProductClass as AbstractProductClass,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractProductImage as AbstractProductImage,
)
from oscar.apps.catalogue.abstract_models import (
    AbstractProductRecommendation as AbstractProductRecommendation,
)
from oscar.apps.catalogue.abstract_models import (
    MissingProductImage as MissingProductImage,
)
from oscar.apps.catalogue.abstract_models import (
    ReverseStartsWith as ReverseStartsWith,
)
from oscar.apps.catalogue.product_attributes import (
    ProductAttributesContainer as ProductAttributesContainer,
)

class ProductClass(AbstractProductClass): ...
class Category(AbstractCategory): ...
class ProductCategory(AbstractProductCategory): ...
class Product(AbstractProduct): ...
class ProductRecommendation(AbstractProductRecommendation): ...
class ProductAttribute(AbstractProductAttribute): ...
class ProductAttributeValue(AbstractProductAttributeValue): ...
class AttributeOptionGroup(AbstractAttributeOptionGroup): ...
class AttributeOption(AbstractAttributeOption): ...
class Option(AbstractOption): ...
class ProductImage(AbstractProductImage): ...
class ProductCategoryHierarchy(AbstractProductCategoryHierarchy): ...
