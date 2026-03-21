# django-oscar-stubs

PEP 561 type stubs for [django-oscar](https://github.com/django-oscar/django-oscar).

Includes a custom mypy plugin that resolves the return types of oscar's dynamic class loading functions (`get_model`, `get_class`, `get_classes`) to the actual concrete types, including support for forked apps.

## Installation

```bash
pip install django-oscar-stubs
```

## Configuration

Add `mypy_oscar_plugin` to your mypy plugins, alongside `mypy_django_plugin.main` from [django-stubs](https://github.com/typeddjango/django-stubs):

```toml
# pyproject.toml
[tool.mypy]
plugins = [
    "mypy_django_plugin.main",
    "mypy_oscar_plugin",
]

[tool.django-stubs]
django_settings_module = "myproject.settings"
```

Or in INI format:

```ini
# mypy.ini
[mypy]
plugins =
    mypy_django_plugin.main,
    mypy_oscar_plugin

[mypy.plugins.django-stubs]
django_settings_module = myproject.settings
```

The oscar plugin reads `django_settings_module` from the django-stubs config section (or the `DJANGO_SETTINGS_MODULE` environment variable) to detect forked apps. Plugin ordering does not matter, but both plugins must be listed.

### Third-party oscar package support

If your project uses third-party packages that extend oscar (e.g., django-oscar-cch, django-oscar-bluelight), the plugin can remap types in those packages too. Configure the package prefixes so the plugin knows which packages to handle:

```toml
# pyproject.toml
[tool.django-oscar-stubs]
oscar_third_party_packages = [
    "oscarcch",
    "oscarbluelight",
    "oscarbundles",
    "oscarapicheckout",
    "cybersource",
]
oscar_local_packages = [
    "oscarpnp",
    "oscarcsr",
]
```

Or in INI format (comma-separated or newline-separated):

```ini
# mypy.ini
[mypy.plugins.django-oscar-stubs]
oscar_third_party_packages = oscarcch, oscarbluelight, oscarbundles, oscarapicheckout, cybersource
oscar_local_packages = oscarpnp, oscarcsr
```

Newline-separated values are also supported:

```ini
# mypy.ini
[mypy.plugins.django-oscar-stubs]
oscar_third_party_packages =
    oscarcch
    oscarbluelight
    oscarbundles
    oscarapicheckout
    cybersource
oscar_local_packages =
    oscarpnp
    oscarcsr
```

- **`oscar_third_party_packages`**: Installed packages that use oscar models via `get_model()`. The plugin normalizes their base class method signatures so that overrides in your project don't produce spurious `[override]` errors. It also remaps oscar types in their method signatures to forked equivalents when the corresponding app is forked.
- **`oscar_local_packages`**: Your own project packages (outside the main forked apps) that import oscar models. The plugin remaps oscar types on attribute access within these packages.

## What it does

### Type-safe dynamic loading

Oscar uses `get_model` and `get_class` to dynamically load models and classes at runtime. Without the plugin, these return untyped `type` objects. With the plugin, mypy resolves them to the actual types:

```python
from oscar.core.loading import get_model, get_class, get_classes

# Without plugin: type[Model]
# With plugin:    type[oscar.apps.catalogue.models.Product]
Product = get_model("catalogue", "Product")

# Without plugin: type
# With plugin:    type[oscar.apps.address.forms.UserAddressForm]
UserAddressForm = get_class("address.forms", "UserAddressForm")

# Without plugin: list[type]
# With plugin:    tuple[type[BasketLineForm], type[SavedLineForm]]
BasketLineForm, SavedLineForm = get_classes(
    "basket.forms", ["BasketLineForm", "SavedLineForm"]
)
```

Both expression-level calls (e.g., `model = get_model(...)`) and module-level assignments (e.g., `Product = get_model(...)`) are handled. Module-level assignments are treated as type aliases during semantic analysis, so the names can be used as type annotations.

When non-literal arguments are used (e.g., a variable instead of a string), the plugin falls back to `type[Model]` for `get_model`, `type` for `get_class`, and `list[type]` for `get_classes`.

### Forked app detection

Oscar's [app forking mechanism](https://django-oscar.readthedocs.io/en/latest/topics/customisation.html) allows projects to replace oscar's built-in apps with custom versions. The plugin detects forked apps by reading `INSTALLED_APPS` from the Django settings module and resolves to your forked types instead of oscar's defaults:

```python
# settings.py
INSTALLED_APPS = [
    ...
    "myproject.catalogue.apps.CatalogueConfig",  # forked from oscar
    "oscar.apps.basket.apps.BasketConfig",        # not forked
    ...
]
```

```python
# myproject/catalogue/models.py
from oscar.apps.catalogue.abstract_models import AbstractProduct

class Product(AbstractProduct):
    custom_field = models.CharField(max_length=100)
```

```python
# Resolves to type[myproject.catalogue.models.Product] (with custom_field!)
Product = get_model("catalogue", "Product")
Product.objects.filter(custom_field="foo")  # type-safe
```

Fork detection works by parsing the settings file's AST. It handles:
- Direct `AppConfig` class names (e.g., `"myproject.catalogue.apps.CatalogueConfig"`)
- Custom config classes that inherit from oscar's configs (inspects the base class)
- Explicit `label = '...'` attributes on custom config classes

The plugin falls back to oscar's default types for any app that hasn't been forked.

### Forked model unification

When a project forks an oscar app and defines custom model classes, two separate TypeInfos exist in mypy's type system: oscar's original (from the stubs) and the fork (from the project code). At runtime, only the forked version exists.

The plugin unifies these by patching mypy's symbol tables so that all references to the oscar model resolve to the forked TypeInfo. This means `from oscar.apps.order.models import Order` gives the same type as `from myproject.order.models import Order`. The plugin also adds the oscar model to the forked model's MRO, establishing a subtype relationship (`forked IS-A oscar`) so that forked types can be passed where oscar types are expected.

### Abstract model type remapping

Oscar defines abstract models (e.g., `AbstractProduct`, `AbstractBasket`) that serve as the base for concrete models. The plugin automatically remaps these abstract types to their concrete forked equivalents wherever they appear: FK fields, method signatures, return types, and QuerySet generics.

```python
order: Order = ...
order.basket            # type: Basket (your forked Basket, not AbstractBasket)
order.shipping_address  # type: ShippingAddress (remapped from AbstractShippingAddress)
order.billing_address   # type: BillingAddress (remapped from AbstractBillingAddress)
```

This includes cross-app models where the abstract is defined in one app but the concrete model lives in another. For example, `AbstractShippingAddress` is defined in oscar's `address` app, but `ShippingAddress` lives in the `order` app. The plugin knows about these cross-app relationships and resolves to the correct concrete model.

### Override-safe method signatures (LSP compliance)

When you override a method from an oscar base class and use concrete types instead of abstract types in the signature, mypy would normally report an `[override]` LSP (Liskov Substitution Principle) violation. The plugin prevents this by rewriting the base class method signatures to use concrete types before mypy checks for LSP compliance:

```python
from oscar.apps.voucher.abstract_models import AbstractVoucher
from oscar.apps.basket.models import Basket
from oscar.apps.order.models import Order

class MyVoucher(AbstractVoucher):
    # Without plugin: [override] error — base expects AbstractBasket, not Basket
    # With plugin: no error — base signature is rewritten to use Basket
    def is_available_for_basket(self, basket: Basket) -> tuple[bool, str]:
        return (True, "")

    def record_usage(self, order: Order, user: User | AnonymousUser | None) -> None:
        pass
```

This works for both abstract model base classes (e.g., `AbstractVoucher`) and non-model classes loaded via `get_class` (e.g., `BasketMiddleware`, `ProductDetailView`).

### Third-party base class handling

Third-party oscar packages (like `oscarapicheckout`, `oscarbluelight`) often define mixin classes that use `get_model()` to obtain oscar types in their method signatures. When your project forks the corresponding app, these signatures need to be remapped too.

The plugin handles this in two stages:

1. **Normalization**: When a class inherits from a third-party base, the plugin normalizes the base's method signatures — replacing forked types (which `get_model()` may have resolved to) back to their oscar concrete equivalents. This ensures consistent types regardless of processing order.

2. **Remapping**: When a class has oscar or third-party bases in its MRO, the plugin remaps oscar types (both abstract and concrete) in those base class method signatures to their forked equivalents.

This prevents spurious `[override]` and `[return-value]` errors when your forked class overrides methods from third-party mixins:

```python
# Third-party package (e.g., oscarapicheckout/mixins.py):
Order = get_model("order", "Order")
class OrderCreatorMixin(OrderCreator):
    def place_order(self, ...) -> Order:
        ...

# Your project (forked order/utils.py):
from myproject.order.models import Order  # forked Order
class OrderCreator(OrderCreatorMixin, oscar_utils.OrderCreator):
    def place_order(self, ...) -> Order:
        # Without plugin: [return-value] error — super() returns oscar's Order
        # With plugin: no error — mixin's return type is remapped to forked Order
        return super().place_order(...)
```

### MRO cycle prevention

Oscar's app forking pattern can create inheritance cycles when combined with third-party packages. Consider:

```python
# Third-party package:
OrderCreator = get_class("order.utils", "OrderCreator")
class OrderCreatorMixin(OrderCreator): ...

# Your forked app:
class OrderCreator(OrderCreatorMixin, oscar_utils.OrderCreator): ...
```

If `get_class()` resolved to the forked `OrderCreator`, the MRO would become `ForkedOrderCreator → OrderCreatorMixin → ForkedOrderCreator` — a cycle. The plugin prevents this by resolving `get_class()` to oscar's original class (not the fork) when the forked class exists in a project-local module. Third-party forks (e.g., `oscarbluelight`) don't have this issue because they're not part of the project's own inheritance chain.

### Strategy class PurchaseInfo remapping

Oscar's partner strategy classes (`Base`, `Structured`, `Default`, etc.) return `PurchaseInfo` objects. When a project forks the partner app and redefines `PurchaseInfo`, the plugin remaps the return types of strategy methods (`fetch_for_product`, `fetch_for_parent`, `fetch_for_line`) to the forked `PurchaseInfo` type. This handles both resolved `Instance` types and unresolved `UnboundType` references during early semantic analysis.

### Method return type remapping

When calling methods on oscar or forked classes, the plugin remaps the return types to use forked equivalents. For example, calling `strategy.fetch_for_product()` returns the forked `PurchaseInfo` type instead of the oscar stub type.

### Dependency tracking

The plugin declares additional dependencies on oscar stub modules and forked app modules. This ensures that when a file imports from `oscar.apps.*` or `oscar.core.loading`, all relevant type information is loaded before the importing module is analyzed. Without this, type resolution could fail due to missing symbols during early processing passes.
