# django-oscar-stubs

PEP 561 type stubs for [django-oscar](https://github.com/django-oscar/django-oscar).

Includes a custom mypy plugin that resolves the return types of oscar's dynamic class loading functions (`get_model`, `get_class`, `get_classes`) to the actual concrete types, including support for forked apps.

## Installation

```bash
pip install django-oscar-stubs
```

## Configuration

Add `mypy_oscar_plugin` to your mypy plugins, alongside `mypy_django_plugin.main` from [django-stubs](https://github.com/typeddjango/django-stubs):

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
