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

- **`oscar_third_party_packages`**: Installed packages that use oscar models via `get_model()`. The plugin normalizes their base class method signatures so that overrides in your project don't produce spurious `[override]` errors.
- **`oscar_local_packages`**: Your own project packages (outside the main forked apps) that import oscar models. The plugin remaps oscar types on attribute access within these packages.

## What it does

### Type-safe dynamic loading

Oscar uses `get_model` and `get_class` to dynamically load models and classes. Without the plugin, these return untyped `type` objects. With the plugin, mypy resolves them to the actual types:

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

### Forked app support

When your project [forks an oscar app](https://django-oscar.readthedocs.io/en/latest/topics/customisation.html), the plugin detects this from `INSTALLED_APPS` and resolves to your forked types instead of oscar's defaults:

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

The plugin falls back to oscar's default types for any app that hasn't been forked, or when literal string arguments aren't used.

### Abstract model type remapping

The plugin automatically remaps oscar's abstract model types to their concrete forked equivalents on attribute access. This includes FK fields, method return types, and QuerySet generics:

```python
order: Order = ...
order.basket          # type: Basket (your forked Basket, not AbstractBasket)
order.shipping_address  # type: ShippingAddress (remapped from AbstractShippingAddress)
order.billing_address   # type: BillingAddress (remapped from AbstractBillingAddress)
```

This works even for abstract models whose concrete counterparts live in a different app (e.g., `AbstractShippingAddress` is defined in oscar's `address` app but `ShippingAddress` lives in the `order` app).
