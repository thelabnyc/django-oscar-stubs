"""Mypy plugin for django-oscar's dynamic class loading.

Resolves return types for:
- oscar.core.loading.get_model(app_label, model_name) -> type[Model]
- oscar.core.loading.get_class(module_label, classname) -> type[Class]
- oscar.core.loading.get_classes(module_label, classnames) -> tuple[type[C1], type[C2], ...]

Supports oscar's app forking pattern: when a project forks an oscar app
(e.g., replaces oscar.apps.catalogue with myproject.catalogue in INSTALLED_APPS),
the plugin resolves to the forked module's types first, falling back to oscar defaults.
"""

from __future__ import annotations

from collections.abc import Callable
from functools import partial
import ast
import configparser
import os
import re
import sys

from mypy.nodes import (
    GDEF,
    FuncDef,
    Import,
    ImportAll,
    ImportFrom,
    ListExpr,
    MypyFile,
    StrExpr,
    SymbolTableNode,
    TupleExpr,
    TypeInfo,
)
from mypy.options import Options
from mypy.plugin import (
    AttributeContext,
    ClassDefContext,
    DynamicClassDefContext,
    FunctionContext,
    MethodContext,
    Plugin,
)
from mypy.types import (
    AnyType,
    CallableType,
    Instance,
    TupleType,
    Type,
    TypeOfAny,
    TypeType,
    UnboundType,
    UnionType,
    get_proper_type,
)

# ──────────────────────────────────────────────────────────────────────
# Oscar app label → default oscar module path (relative to oscar.apps)
# ──────────────────────────────────────────────────────────────────────

APP_LABEL_MAP: dict[str, str] = {
    "address": "address",
    "analytics": "analytics",
    "basket": "basket",
    "catalogue": "catalogue",
    "reviews": "catalogue.reviews",
    "checkout": "checkout",
    "communication": "communication",
    "customer": "customer",
    "offer": "offer",
    "order": "order",
    "partner": "partner",
    "payment": "payment",
    "search": "search",
    "shipping": "shipping",
    "voucher": "voucher",
    "wishlists": "wishlists",
    "dashboard": "dashboard",
    "catalogue_dashboard": "dashboard.catalogue",
    "communications_dashboard": "dashboard.communications",
    "offers_dashboard": "dashboard.offers",
    "orders_dashboard": "dashboard.orders",
    "pages_dashboard": "dashboard.pages",
    "partners_dashboard": "dashboard.partners",
    "ranges_dashboard": "dashboard.ranges",
    "reports_dashboard": "dashboard.reports",
    "reviews_dashboard": "dashboard.reviews",
    "shipping_dashboard": "dashboard.shipping",
    "users_dashboard": "dashboard.users",
    "vouchers_dashboard": "dashboard.vouchers",
}

# Reverse map: known oscar AppConfig class name → oscar app label.
# When a user forks an app, their config class typically inherits from
# oscar's config and keeps the same class name (or we parse the base class).
_OSCAR_CONFIG_CLASS_TO_LABEL: dict[str, str] = {
    "AddressConfig": "address",
    "AnalyticsConfig": "analytics",
    "BasketConfig": "basket",
    "CatalogueConfig": "catalogue",
    "CatalogueReviewsConfig": "reviews",
    "CheckoutConfig": "checkout",
    "CommunicationConfig": "communication",
    "CustomerConfig": "customer",
    "DashboardConfig": "dashboard",
    "OfferConfig": "offer",
    "OrderConfig": "order",
    "PartnerConfig": "partner",
    "PaymentConfig": "payment",
    "SearchConfig": "search",
    "ShippingConfig": "shipping",
    "VoucherConfig": "voucher",
    "WishlistsConfig": "wishlists",
    "CatalogueDashboardConfig": "catalogue_dashboard",
    "CommunicationsDashboardConfig": "communications_dashboard",
    "OffersDashboardConfig": "offers_dashboard",
    "OrdersDashboardConfig": "orders_dashboard",
    "PagesDashboardConfig": "pages_dashboard",
    "PartnersDashboardConfig": "partners_dashboard",
    "RangesDashboardConfig": "ranges_dashboard",
    "ReportsDashboardConfig": "reports_dashboard",
    "ReviewsDashboardConfig": "reviews_dashboard",
    "ShippingDashboardConfig": "shipping_dashboard",
    "UsersDashboardConfig": "users_dashboard",
    "VouchersDashboardConfig": "vouchers_dashboard",
}

# Reverse map: oscar.apps sub-path → app label
_OSCAR_PATH_TO_LABEL: dict[str, str] = {v: k for k, v in APP_LABEL_MAP.items()}

_OSCAR_GET_MODEL = "oscar.core.loading.get_model"
_OSCAR_GET_CLASS = "oscar.core.loading.get_class"
_OSCAR_GET_CLASSES = "oscar.core.loading.get_classes"


# ──────────────────────────────────────────────────────────────────────
# Settings / fork detection
# ──────────────────────────────────────────────────────────────────────


def _get_django_settings_module(options: Options) -> str | None:
    """Read the django_settings_module from the mypy config or environment."""
    # Environment takes precedence (django-stubs sets this)
    from_env = os.environ.get("DJANGO_SETTINGS_MODULE")
    if from_env:
        return from_env

    # Fall back to parsing the mypy config file for the django-stubs section
    if not options.config_file:
        return None

    config_file = options.config_file

    # Handle pyproject.toml (TOML format)
    if config_file.endswith(".toml"):
        return _read_settings_from_toml(config_file)

    # Handle INI-format files (mypy.ini, setup.cfg, etc.)
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except (configparser.Error, OSError):
        return None

    for section in ("mypy.plugins.django-stubs", "mypy_django_plugin"):
        if config.has_section(section):
            val = config.get(section, "django_settings_module", fallback=None)
            if val:
                return val

    return None


def _read_settings_from_toml(config_file: str) -> str | None:
    """Read django_settings_module from a pyproject.toml file."""
    try:
        import tomllib

        with open(config_file, "rb") as f:
            data = tomllib.load(f)

        # Check [tool.django-stubs] section
        val = data.get("tool", {}).get("django-stubs", {}).get("django_settings_module")
        if val:
            return str(val)

        # Check [tool.mypy_django_plugin] section (alternative config)
        val = data.get("tool", {}).get("mypy_django_plugin", {}).get("django_settings_module")
        if val:
            return str(val)

    except (OSError, Exception):
        pass

    return None


def _read_oscar_package_prefixes(
    options: Options,
) -> tuple[tuple[str, ...], tuple[str, ...]]:
    """Read oscar_third_party_packages and oscar_local_packages from config.

    Returns (third_party_prefixes, local_prefixes) tuples with trailing dots
    appended to each entry.  Defaults are intentionally empty -- the plugin
    only processes third-party/local packages when explicitly configured.
    """
    if not options.config_file:
        return ((), ())

    config_file = options.config_file

    if config_file.endswith(".toml"):
        third_party, local = _read_oscar_prefixes_from_toml(config_file)
    else:
        third_party, local = _read_oscar_prefixes_from_ini(config_file)

    def _normalize(entries: list[str]) -> tuple[str, ...]:
        return tuple(e if e.endswith(".") else f"{e}." for e in entries)

    tp = _normalize(third_party) if third_party else ()
    lp = _normalize(local) if local else ()
    return (tp, lp)


def _read_oscar_prefixes_from_toml(config_file: str) -> tuple[list[str], list[str]]:
    """Read oscar package prefixes from a pyproject.toml file."""
    try:
        import tomllib

        with open(config_file, "rb") as f:
            data = tomllib.load(f)

        section = data.get("tool", {}).get("django-oscar-stubs", {})
        third_party = section.get("oscar_third_party_packages", [])
        local = section.get("oscar_local_packages", [])

        third_party = [str(e) for e in third_party] if isinstance(third_party, list) else []
        local = [str(e) for e in local] if isinstance(local, list) else []
        return (third_party, local)

    except (OSError, Exception):
        pass

    return ([], [])


def _parse_ini_list(raw: str) -> list[str]:
    """Parse a comma-separated or newline-separated INI config value into a list.

    Handles both ``a, b, c`` and multi-line values::

        a
        b
        c

    Empty strings and whitespace-only entries are filtered out.
    """
    # Split on commas and newlines, strip whitespace, filter empties
    entries = re.split(r"[,\n]", raw)
    return [e.strip() for e in entries if e.strip()]


def _read_oscar_prefixes_from_ini(config_file: str) -> tuple[list[str], list[str]]:
    """Read oscar package prefixes from an INI-format config file."""
    config = configparser.ConfigParser()
    try:
        config.read(config_file)
    except (configparser.Error, OSError):
        return ([], [])

    for section_name in ("mypy.plugins.django-oscar-stubs", "django-oscar-stubs"):
        if config.has_section(section_name):
            tp_raw = config.get(section_name, "oscar_third_party_packages", fallback="")
            lp_raw = config.get(section_name, "oscar_local_packages", fallback="")
            third_party = _parse_ini_list(tp_raw)
            local = _parse_ini_list(lp_raw)
            return (third_party, local)

    return ([], [])


def _find_settings_file(settings_module: str) -> str | None:
    """Locate the settings .py file on the filesystem."""
    rel_path = settings_module.replace(".", os.sep) + ".py"
    for path_entry in sys.path:
        full_path = os.path.join(path_entry, rel_path)
        if os.path.isfile(full_path):
            return full_path
    return None


def _extract_app_config_strings(tree: ast.AST) -> list[str]:
    """Extract AppConfig-style string literals from an AST.

    Finds string constants matching ``some.module.apps.ClassName`` that are not
    from oscar or django (i.e., they are user/third-party app configs).
    """
    entries: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            if ".apps." in value and not value.startswith("oscar.") and not value.startswith("django."):
                last_part = value.rsplit(".", 1)[-1]
                if last_part and last_part[0].isupper():
                    entries.append(value)
    return entries


def _resolve_import_source(module_name: str, name: str) -> str | None:
    """Find the source file for a name imported from a module.

    Resolves ``from <module_name> import <name>`` to a filesystem path.
    """
    rel_path = module_name.replace(".", os.sep)
    for path_entry in sys.path:
        # Try as a package (__init__.py)
        pkg_path = os.path.join(path_entry, rel_path, "__init__.py")
        if os.path.isfile(pkg_path):
            return pkg_path
        # Try as a module (.py)
        mod_path = os.path.join(path_entry, rel_path + ".py")
        if os.path.isfile(mod_path):
            return mod_path
    return None


def _collect_app_config_entries(settings_file: str) -> list[str]:
    """Collect all AppConfig-style entries from the settings file.

    Scans the settings file for string literals matching the pattern
    ``some.module.apps.ClassName``. Also follows imported function calls
    used in INSTALLED_APPS (e.g. ``INSTALLED_APPS = [...] + get_core_apps()``)
    by scanning the imported module for the same patterns.

    Returns only non-oscar entries (entries whose module path does NOT
    start with ``oscar.``).
    """
    try:
        with open(settings_file) as f:
            source = f.read()
            tree = ast.parse(source)
    except (OSError, SyntaxError):
        return []

    # Collect entries directly from the settings file
    entries = _extract_app_config_strings(tree)

    # Build import map: name → (module, original_name)
    import_map: dict[str, tuple[str, str]] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.ImportFrom) and node.module:
            for alias in node.names:
                local_name = alias.asname or alias.name
                import_map[local_name] = (node.module, alias.name)

    # Find function calls used with INSTALLED_APPS and follow imports.
    # Handles patterns like:
    #   INSTALLED_APPS = [...] + get_core_apps()
    #   INSTALLED_APPS = get_core_apps() + [...]
    for node in ast.walk(tree):
        if isinstance(node, ast.Call) and isinstance(node.func, ast.Name):
            func_name = node.func.id
            if func_name in import_map:
                module_name, original_name = import_map[func_name]
                source_file = _resolve_import_source(module_name, original_name)
                if source_file:
                    try:
                        with open(source_file) as f:
                            imported_tree = ast.parse(f.read())
                    except (OSError, SyntaxError):
                        continue
                    entries.extend(_extract_app_config_strings(imported_tree))

    return entries


def _determine_oscar_label_from_config(entry: str) -> tuple[str, str] | None:
    """Given an AppConfig entry, determine if it's an oscar app fork.

    Args:
        entry: An INSTALLED_APPS entry like "myproject.catalogue.apps.CatalogueConfig"

    Returns:
        A tuple of (oscar_app_label, forked_module_path) if this is an oscar
        fork, or None if it's not.
    """
    # Split: "myproject.catalogue.apps.CatalogueConfig" → module="myproject.catalogue", class="CatalogueConfig"
    parts = entry.rsplit(".apps.", 1)
    if len(parts) != 2:
        return None
    module_path, config_class_name = parts

    # Strategy 1: match by config class name (handles the common case where
    # the forked config keeps the same name as oscar's config)
    label = _OSCAR_CONFIG_CLASS_TO_LABEL.get(config_class_name)
    if label is not None:
        return (label, module_path)

    # Strategy 2: parse the apps.py source file to find the base class.
    # Handles cases where the user renames their config class.
    label = _parse_config_base_class(module_path, config_class_name)
    if label is not None:
        return (label, module_path)

    return None


def _parse_config_base_class(module_path: str, config_class_name: str) -> str | None:
    """Parse an apps.py file to determine the oscar app label from base classes."""
    apps_file = module_path.replace(".", os.sep) + os.sep + "apps.py"

    for path_entry in sys.path:
        full_path = os.path.join(path_entry, apps_file)
        if os.path.isfile(full_path):
            try:
                with open(full_path) as f:
                    tree = ast.parse(f.read())
            except (OSError, SyntaxError):
                return None

            # Build a map of import aliases → original names so we can
            # resolve e.g. ``from oscar.apps.catalogue.apps import CatalogueConfig as Base``
            alias_map: dict[str, str] = {}
            for node in ast.walk(tree):
                if isinstance(node, ast.ImportFrom):
                    for alias in node.names:
                        if alias.asname:
                            alias_map[alias.asname] = alias.name
                        else:
                            alias_map[alias.name] = alias.name

            for node in ast.walk(tree):
                if isinstance(node, ast.ClassDef) and node.name == config_class_name:
                    # Check for explicit label = '...' attribute
                    for item in node.body:
                        if isinstance(item, ast.Assign):
                            for target in item.targets:
                                if (
                                    isinstance(target, ast.Name)
                                    and target.id == "label"
                                    and isinstance(item.value, ast.Constant)
                                    and isinstance(item.value.value, str)
                                ):
                                    label = item.value.value
                                    if label in APP_LABEL_MAP:
                                        return label

                    # Check base class names (resolving aliases)
                    for base in node.bases:
                        if isinstance(base, ast.Attribute):
                            base_name = base.attr
                        elif isinstance(base, ast.Name):
                            base_name = base.id
                        else:
                            continue
                        # Resolve alias to original name
                        original_name = alias_map.get(base_name, base_name)
                        label = _OSCAR_CONFIG_CLASS_TO_LABEL.get(original_name)
                        if label is not None:
                            return label

                    break

    return None


def _detect_forked_apps(options: Options) -> dict[str, str]:
    """Detect oscar apps that have been forked in the user's project.

    Returns a mapping of oscar_app_label → forked_module_path.
    For example: {"catalogue": "myproject.catalogue", "partner": "myproject.partner"}
    """
    settings_module = _get_django_settings_module(options)
    if not settings_module:
        return {}

    settings_file = _find_settings_file(settings_module)
    if not settings_file:
        return {}

    entries = _collect_app_config_entries(settings_file)
    overrides: dict[str, str] = {}

    for entry in entries:
        result = _determine_oscar_label_from_config(entry)
        if result is not None:
            app_label, module_path = result
            overrides[app_label] = module_path

    return overrides


# ──────────────────────────────────────────────────────────────────────
# Stub module discovery
# ──────────────────────────────────────────────────────────────────────


def _find_stubbed_modules() -> set[str]:
    """Discover oscar modules that have stubs by scanning the oscar-stubs directory."""
    modules: set[str] = set()

    for path_entry in sys.path:
        stubs_dir = os.path.join(path_entry, "oscar-stubs")
        if os.path.isdir(stubs_dir):
            apps_dir = os.path.join(stubs_dir, "apps")
            if os.path.isdir(apps_dir):
                for root, _dirs, files in os.walk(apps_dir):
                    for f in files:
                        if f.endswith(".pyi") and f != "__init__.pyi":
                            rel = os.path.relpath(os.path.join(root, f), stubs_dir)
                            mod = "oscar." + rel.replace(os.sep, ".").removesuffix(".pyi")
                            modules.add(mod)
            break

    return modules


# ──────────────────────────────────────────────────────────────────────
# Oscar type remapping (abstract → concrete, oscar → forked)
# ──────────────────────────────────────────────────────────────────────

# Cross-app model map: maps (abstract_app_path, model_name) to the concrete
# app label where the concrete model actually lives.  In Oscar, most abstract
# models have their concrete counterpart in the same app.  A few, however,
# are defined in one app but the concrete model lives in a different app
# (because the abstract model's Meta sets ``app_label`` to another app).
#
# These entries were discovered by searching oscar's abstract_models.py files
# for inner ``class Meta`` definitions that set ``app_label`` to a different
# app than the file they reside in.  For example,
# ``oscar/apps/address/abstract_models.py::AbstractShippingAddress`` has
# ``class Meta: app_label = 'order'``, meaning its concrete model lives in
# ``oscar.apps.order.models``, not ``oscar.apps.address.models``.
_CROSS_APP_MODEL_MAP: dict[tuple[str, str], str] = {
    # oscar.apps.address.abstract_models.AbstractShippingAddress → order app
    ("address", "ShippingAddress"): "order",
    # oscar.apps.address.abstract_models.AbstractBillingAddress → order app
    ("address", "BillingAddress"): "order",
    # oscar.apps.address.abstract_models.AbstractPartnerAddress → partner app
    ("address", "PartnerAddress"): "partner",
}

# Pattern: oscar.apps.<path>.abstract_models.Abstract<Name>
_ABSTRACT_MODEL_RE = re.compile(r"^oscar\.apps\.(.+)\.abstract_models\.Abstract(\w+)$")

# Pattern: oscar.apps.<path>.models.<Name> (concrete models)
_CONCRETE_MODEL_RE = re.compile(r"^oscar\.apps\.(.+)\.models\.(\w+)$")

# Pattern: oscar.apps.<path>.<submodule>.<Name> (any oscar class, e.g. strategy.PurchaseInfo)
_OSCAR_CLASS_RE = re.compile(r"^oscar\.apps\.(.+?)\.(\w+)\.(\w+)$")


def _is_oscar_abstract_model(fullname: str) -> bool:
    """Check if a fully qualified name is an oscar abstract model class."""
    return _ABSTRACT_MODEL_RE.match(fullname) is not None


def _resolve_abstract_to_concrete(fullname: str, plugin: OscarPlugin) -> Type | None:
    """Resolve an oscar abstract model fullname to its concrete model type.

    E.g. oscar.apps.address.abstract_models.AbstractCountry → Country
    from oscar.apps.address.models (or forked equivalent).

    Handles cross-app models where the abstract is defined in one app but the
    concrete lives in another (e.g. AbstractShippingAddress in address app →
    ShippingAddress in order app).
    """
    m = _ABSTRACT_MODEL_RE.match(fullname)
    if m is None:
        return None
    oscar_path = m.group(1)  # e.g. "address", "catalogue.reviews"
    model_name = m.group(2)  # e.g. "Country" (without "Abstract" prefix)

    app_label = _OSCAR_PATH_TO_LABEL.get(oscar_path)
    if app_label is None:
        return None

    # Check for cross-app models first: the abstract may live in one app
    # but the concrete model is in a different app.
    cross_app_label = _CROSS_APP_MODEL_MAP.get((oscar_path, model_name))
    if cross_app_label is not None:
        result = _resolve_model(cross_app_label, model_name, plugin)
        if result is not None:
            return result

    return _resolve_model(app_label, model_name, plugin)


def _resolve_concrete_to_forked(fullname: str, plugin: OscarPlugin) -> Type | None:
    """Resolve an oscar concrete model to its forked equivalent.

    E.g. oscar.apps.catalogue.models.Product → myproject.catalogue.models.Product
    Only remaps if the app is actually forked.
    """
    m = _CONCRETE_MODEL_RE.match(fullname)
    if m is None:
        return None
    oscar_path = m.group(1)  # e.g. "catalogue"
    model_name = m.group(2)  # e.g. "Product"

    app_label = _OSCAR_PATH_TO_LABEL.get(oscar_path)
    if app_label is None:
        return None

    # Only remap if the app is forked
    override_module = plugin._app_overrides.get(app_label)
    if not override_module:
        return None

    return _resolve_type(f"{override_module}.models.{model_name}", plugin)


def _resolve_oscar_class_to_forked(fullname: str, plugin: OscarPlugin) -> Type | None:
    """Resolve any oscar.apps class to its forked equivalent.

    Handles non-model classes like oscar.apps.partner.strategy.PurchaseInfo
    → myproject.partner.strategy.PurchaseInfo when the app is forked.
    """
    m = _OSCAR_CLASS_RE.match(fullname)
    if m is None:
        return None
    oscar_path = m.group(1)  # e.g. "partner"
    submodule = m.group(2)  # e.g. "strategy"
    class_name = m.group(3)  # e.g. "PurchaseInfo"

    # Skip abstract_models (handled by _resolve_abstract_to_concrete)
    if submodule == "abstract_models":
        return None

    app_label = _OSCAR_PATH_TO_LABEL.get(oscar_path)
    if app_label is None:
        return None

    # Only remap if the app is forked
    override_module = plugin._app_overrides.get(app_label)
    if not override_module:
        return None

    forked_fullname = f"{override_module}.{submodule}.{class_name}"

    # Guard: skip remapping unconditionally (regardless of whether the
    # fork is third-party or project-local) when the forked module
    # defines a class with the same name.  This function is used by the
    # attribute/method type remapping hooks, where remapping to the
    # forked type would always create a cycle: the forked class extends
    # the oscar original, so its attribute types must resolve to the
    # oscar base, not back to itself.
    #
    # This differs from the guard in _resolve_class, which only skips
    # project-local forks.  _resolve_class handles get_class() calls,
    # where third-party packages legitimately need to resolve to the
    # forked type (they call get_class() to obtain the class the user
    # has overridden).
    forked_sym = plugin.lookup_fully_qualified(forked_fullname)
    if forked_sym is not None and isinstance(forked_sym.node, TypeInfo):
        return None

    return _resolve_type(forked_fullname, plugin)


def _remap_oscar_type(typ: Type, plugin: OscarPlugin) -> Type:
    """Recursively walk a type, replacing oscar types with forked equivalents.

    Handles:
    - Abstract models → concrete models (in forked app or oscar default)
    - Concrete oscar models → forked models (when app is forked)
    - Other oscar classes → forked equivalents (e.g. strategy classes)
    """
    typ = get_proper_type(typ)

    if isinstance(typ, Instance):
        fullname = typ.type.fullname
        remapped: Type | None = None

        # Priority 1: abstract model → concrete (handles forked apps)
        if _is_oscar_abstract_model(fullname):
            remapped = _resolve_abstract_to_concrete(fullname, plugin)

        # Priority 2: concrete oscar model → forked model
        if remapped is None:
            remapped = _resolve_concrete_to_forked(fullname, plugin)

        # Priority 3: any oscar class → forked class
        if remapped is None:
            remapped = _resolve_oscar_class_to_forked(fullname, plugin)

        if remapped is not None:
            remapped = get_proper_type(remapped)
            if isinstance(remapped, Instance) and typ.args:
                remapped = remapped.copy_modified(args=[_remap_oscar_type(a, plugin) for a in typ.args])
            return remapped

        # Even if not remapped itself, remap type args (e.g. QuerySet[AbstractProduct])
        if typ.args:
            new_args = [_remap_oscar_type(a, plugin) for a in typ.args]
            if any(a is not b for a, b in zip(new_args, typ.args)):
                return typ.copy_modified(args=new_args)

    elif isinstance(typ, TupleType):
        new_items = [_remap_oscar_type(item, plugin) for item in typ.items]
        if any(a is not b for a, b in zip(new_items, typ.items)):
            return typ.copy_modified(items=new_items)

    elif isinstance(typ, UnionType):
        new_items = [_remap_oscar_type(item, plugin) for item in typ.items]
        if any(a is not b for a, b in zip(new_items, typ.items)):
            return UnionType.make_union(new_items)

    return typ


def _remap_oscar_attr_hook(ctx: AttributeContext, *, plugin: OscarPlugin) -> Type:
    """Attribute hook callback: remap oscar types to forked equivalents."""
    # Don't remap setter types — keep abstract (more permissive) for assignments
    if ctx.is_lvalue:
        return ctx.default_attr_type

    return _remap_oscar_type(ctx.default_attr_type, plugin)


# ──────────────────────────────────────────────────────────────────────
# Type resolution
# ──────────────────────────────────────────────────────────────────────


def _resolve_type(fullname: str, plugin: OscarPlugin) -> Type | None:
    """Try to resolve a fully qualified type name to a mypy Instance.

    Returns the Instance, or None if the type can't be found.
    """
    sym = plugin.lookup_fully_qualified(fullname)
    if sym is not None and isinstance(sym.node, TypeInfo):
        return Instance(sym.node, [])
    return None


def _resolve_model(
    app_label: str,
    model_name: str,
    plugin: OscarPlugin,
) -> Type | None:
    """Resolve a model by app label, checking forked modules first."""
    # Try forked module first
    override_module = plugin._app_overrides.get(app_label)
    if override_module:
        instance = _resolve_type(f"{override_module}.models.{model_name}", plugin)
        if instance is not None:
            return instance

    # Fall back to oscar default
    oscar_path = APP_LABEL_MAP.get(app_label)
    if oscar_path is not None:
        instance = _resolve_type(f"oscar.apps.{oscar_path}.models.{model_name}", plugin)
        if instance is not None:
            return instance

    return None


def _resolve_class(
    module_label: str,
    classname: str,
    plugin: OscarPlugin,
) -> Type | None:
    """Resolve a class by module label, checking forked modules first.

    module_label is like 'catalogue.forms' or 'dashboard.catalogue.forms'.
    The first component is the app label used to look up the registered app.
    """
    app_label = module_label.split(".")[0]
    submodule = ".".join(module_label.split(".")[1:])

    # Try forked module first
    override_module = plugin._app_overrides.get(app_label)
    if override_module:
        if submodule:
            fqn = f"{override_module}.{submodule}.{classname}"
        else:
            fqn = f"{override_module}.{classname}"

        # Cycle prevention: if the forked module is from the project's own
        # code (not a third-party oscar package) and it defines a class with
        # this exact name, don't resolve to it.  The forked class necessarily
        # extends the oscar original (that's how oscar app forking works).
        # Resolving to it here would create inheritance cycles when a
        # third-party package uses get_class() to obtain a base class that
        # the forked class itself overrides.
        #
        # For example, oscarapicheckout.mixins does:
        #   OrderCreator = get_class("order.utils", "OrderCreator")
        #   class OrderCreatorMixin(OrderCreator): ...
        # And the forked app does:
        #   class OrderCreator(OrderCreatorMixin, oscar_utils.OrderCreator): ...
        # Resolving the get_class() call to the forked OrderCreator would
        # create: ForkedOrderCreator -> OrderCreatorMixin -> ForkedOrderCreator.
        #
        # We only skip project-local forks (not third-party forks like
        # oscarbluelight) because third-party packages that fork oscar apps
        # are not part of the project's own inheritance chain.
        is_third_party_fork = any(fqn.startswith(prefix) for prefix in plugin._third_party_prefixes)
        # Skip resolution to the forked type when a project-local fork
        # defines this class itself -- resolving to it would create an
        # inheritance cycle (forked class extends oscar original, but
        # get_class() would point back to the fork).  Third-party forks
        # are not part of the project's own inheritance chain, so they
        # are always resolved normally.
        skip_fork = False
        if not is_third_party_fork:
            forked_sym = plugin.lookup_fully_qualified(fqn)
            skip_fork = forked_sym is not None and isinstance(forked_sym.node, TypeInfo)

        if not skip_fork:
            instance = _resolve_type(fqn, plugin)
            if instance is not None:
                return instance

    # Fall back to oscar default
    instance = _resolve_type(f"oscar.apps.{module_label}.{classname}", plugin)
    if instance is not None:
        return instance

    return None


# ──────────────────────────────────────────────────────────────────────
# Function hooks
# ──────────────────────────────────────────────────────────────────────


def _get_model_hook(ctx: FunctionContext, *, plugin: OscarPlugin) -> Type:
    """Resolve get_model('app_label', 'ModelName') -> type[Model]."""
    if len(ctx.args) < 2:
        return ctx.default_return_type

    app_label_args = ctx.args[0]
    model_name_args = ctx.args[1]

    if not app_label_args or not model_name_args:
        return ctx.default_return_type

    app_label_expr = app_label_args[0]
    model_name_expr = model_name_args[0]

    if not isinstance(app_label_expr, StrExpr) or not isinstance(model_name_expr, StrExpr):
        return ctx.default_return_type

    instance = _resolve_model(app_label_expr.value, model_name_expr.value, plugin)
    if instance is None:
        return ctx.default_return_type

    return TypeType(instance)


def _get_class_hook(ctx: FunctionContext, *, plugin: OscarPlugin) -> Type:
    """Resolve get_class('app.module', 'ClassName') -> type[Class]."""
    if len(ctx.args) < 2:
        return ctx.default_return_type

    module_label_args = ctx.args[0]
    classname_args = ctx.args[1]

    if not module_label_args or not classname_args:
        return ctx.default_return_type

    module_label_expr = module_label_args[0]
    classname_expr = classname_args[0]

    if not isinstance(module_label_expr, StrExpr) or not isinstance(classname_expr, StrExpr):
        return ctx.default_return_type

    instance = _resolve_class(module_label_expr.value, classname_expr.value, plugin)
    if instance is None:
        return ctx.default_return_type

    return TypeType(instance)


def _get_classes_hook(ctx: FunctionContext, *, plugin: OscarPlugin) -> Type:
    """Resolve get_classes('app.module', ['C1', 'C2']) -> tuple[type[C1], type[C2]]."""
    if len(ctx.args) < 2:
        return ctx.default_return_type

    module_label_args = ctx.args[0]
    classnames_args = ctx.args[1]

    if not module_label_args or not classnames_args:
        return ctx.default_return_type

    module_label_expr = module_label_args[0]
    if not isinstance(module_label_expr, StrExpr):
        return ctx.default_return_type

    module_label = module_label_expr.value

    classnames_expr = classnames_args[0]
    if isinstance(classnames_expr, (ListExpr, TupleExpr)):
        str_exprs = classnames_expr.items
    else:
        return ctx.default_return_type

    classnames: list[str] = []
    for item in str_exprs:
        if not isinstance(item, StrExpr):
            return ctx.default_return_type
        classnames.append(item.value)

    if not classnames:
        return ctx.default_return_type

    resolved_types: list[Type] = []
    for classname in classnames:
        instance = _resolve_class(module_label, classname, plugin)
        if instance is None:
            return ctx.default_return_type
        resolved_types.append(TypeType(instance))

    fallback = ctx.api.named_generic_type("builtins.tuple", [AnyType(TypeOfAny.special_form)])
    return TupleType(resolved_types, fallback)


# ──────────────────────────────────────────────────────────────────────
# Dynamic class hooks (semantic analysis phase)
# ──────────────────────────────────────────────────────────────────────


def _create_type_info_ref(ctx: DynamicClassDefContext, instance: Type) -> None:
    """Add a direct TypeInfo reference to the symbol table.

    Instead of creating a TypeAlias, we add the resolved TypeInfo directly,
    which is equivalent to what ``from module import ClassName`` does.
    This avoids Var/TypeAlias conflicts during mypy re-analysis.
    """
    proper = get_proper_type(instance)
    if not isinstance(proper, Instance):
        return

    type_info = proper.type

    # Check if already set up correctly
    existing = ctx.api.lookup_qualified(ctx.name, ctx.call)
    if existing is not None and existing.node is type_info:
        return

    ctx.api.add_symbol_table_node(ctx.name, SymbolTableNode(GDEF, type_info))


def _get_model_dynamic_class_hook(ctx: DynamicClassDefContext, *, plugin: OscarPlugin) -> None:
    """Handle Model = get_model('app_label', 'ModelName') as a type alias."""
    if len(ctx.call.args) < 2:
        return

    app_label_expr = ctx.call.args[0]
    model_name_expr = ctx.call.args[1]

    if not isinstance(app_label_expr, StrExpr) or not isinstance(model_name_expr, StrExpr):
        return

    instance = _resolve_model(app_label_expr.value, model_name_expr.value, plugin)
    if instance is not None:
        _create_type_info_ref(ctx, instance)
    elif not ctx.api.final_iteration:
        ctx.api.defer()


def _get_class_dynamic_class_hook(ctx: DynamicClassDefContext, *, plugin: OscarPlugin) -> None:
    """Handle Cls = get_class('module_label', 'ClassName') as a type alias."""
    if len(ctx.call.args) < 2:
        return

    module_label_expr = ctx.call.args[0]
    classname_expr = ctx.call.args[1]

    if not isinstance(module_label_expr, StrExpr) or not isinstance(classname_expr, StrExpr):
        return

    instance = _resolve_class(module_label_expr.value, classname_expr.value, plugin)
    if instance is not None:
        _create_type_info_ref(ctx, instance)
    elif not ctx.api.final_iteration:
        ctx.api.defer()


# ──────────────────────────────────────────────────────────────────────
# Base class hook: remap oscar types in base class method signatures
# ──────────────────────────────────────────────────────────────────────

# Oscar strategy classes whose method return types should be remapped
# when a project forks the partner app and redefines PurchaseInfo.
_STRATEGY_CLASSES = frozenset(
    {
        "oscar.apps.partner.strategy.Base",
        "oscar.apps.partner.strategy.Structured",
        "oscar.apps.partner.strategy.UseFirstStockRecord",
        "oscar.apps.partner.strategy.StockRequired",
        "oscar.apps.partner.strategy.NoTax",
        "oscar.apps.partner.strategy.FixedRateTax",
        "oscar.apps.partner.strategy.DeferredTax",
        "oscar.apps.partner.strategy.Default",
        "oscar.apps.partner.strategy.UK",
        "oscar.apps.partner.strategy.US",
    }
)


def _normalize_forked_to_oscar_type(typ: Type, plugin: OscarPlugin) -> Type:
    """Reverse-map forked types back to their oscar concrete equivalents.

    When get_model() resolves names in third-party packages to the forked
    model type (e.g. tsicommon.oscarapps.basket.models.Basket), this function
    maps them back to the oscar concrete type (oscar.apps.basket.models.Basket).
    This is needed so that base class method signatures in third-party packages
    are compatible with child class overrides that use direct oscar imports.
    """
    typ = get_proper_type(typ)

    if isinstance(typ, Instance):
        fullname = typ.type.fullname

        # Check if this type belongs to a forked module
        for app_label, override_module in plugin._app_overrides.items():
            if fullname.startswith(f"{override_module}."):
                # Extract the relative path after the override module
                # e.g. "tsicommon.oscarapps.basket.models.Basket" → "models.Basket"
                relative = fullname[len(override_module) + 1 :]
                oscar_path = APP_LABEL_MAP.get(app_label)
                if oscar_path is not None:
                    oscar_fullname = f"oscar.apps.{oscar_path}.{relative}"
                    result = _resolve_type(oscar_fullname, plugin)
                    if result is not None:
                        result = get_proper_type(result)
                        if isinstance(result, Instance) and typ.args:
                            result = result.copy_modified(
                                args=[_normalize_forked_to_oscar_type(a, plugin) for a in typ.args]
                            )
                        return result
                break

        # Recurse into type args
        if typ.args:
            new_args = [_normalize_forked_to_oscar_type(a, plugin) for a in typ.args]
            if any(a is not b for a, b in zip(new_args, typ.args)):
                return typ.copy_modified(args=new_args)

    elif isinstance(typ, TupleType):
        new_items = [_normalize_forked_to_oscar_type(item, plugin) for item in typ.items]
        if any(a is not b for a, b in zip(new_items, typ.items)):
            return typ.copy_modified(items=new_items)

    elif isinstance(typ, UnionType):
        new_items = [_normalize_forked_to_oscar_type(item, plugin) for item in typ.items]
        if any(a is not b for a, b in zip(new_items, typ.items)):
            return UnionType.make_union(new_items)

    return typ


def _is_third_party_oscar_fullname(fullname: str, plugin: OscarPlugin) -> bool:
    """Check if a fully-qualified name belongs to a third-party oscar package."""
    for prefix in plugin._third_party_prefixes:
        if fullname.startswith(prefix):
            return True
    return False


def _resolve_and_normalize_type(typ: Type, plugin: OscarPlugin) -> Type:
    """Resolve UnboundType references and normalize forked types to oscar types.

    During semantic analysis, method signatures may contain UnboundType
    references (e.g. ``Basket?``) that haven't been resolved yet. This
    function attempts to resolve them through the plugin's symbol table
    and then normalizes any forked types back to their oscar equivalents.
    """
    proper = get_proper_type(typ)

    # Don't touch AnyType -- replacing an UnboundType("Any") with a resolved
    # Instance(typing.Any) can change mypy's behavior for type compatibility.
    if isinstance(proper, AnyType):
        return typ

    if isinstance(proper, Instance):
        return _normalize_forked_to_oscar_type(proper, plugin)

    if isinstance(proper, TupleType):
        new_items = [_resolve_and_normalize_type(item, plugin) for item in proper.items]
        if any(a is not b for a, b in zip(new_items, proper.items)):
            return proper.copy_modified(items=new_items)
        return typ

    if isinstance(proper, UnionType):
        new_items = [_resolve_and_normalize_type(item, plugin) for item in proper.items]
        if any(a is not b for a, b in zip(new_items, proper.items)):
            return UnionType.make_union(new_items)
        return typ

    # Handle UnboundType: try to resolve the name to a concrete oscar type.
    # This handles cases where get_model() created a module-level name like
    # ``Basket = get_model("basket", "Basket")`` that resolves to a forked
    # type, but the method signature still contains an UnboundType("Basket").
    #
    # Note: we check the original ``typ`` (not ``proper``) because
    # get_proper_type() may have already resolved UnboundType to something
    # else.  If the original is an UnboundType, we try to resolve it.
    if isinstance(typ, UnboundType):
        unbound_name = typ.name
        # Oscar model names are unique across apps (e.g. there is only one
        # "Basket" model, only one "Product" model, etc.), so matching the
        # first app that has a model with this name is correct.
        for app_label in plugin._app_overrides:
            oscar_path = APP_LABEL_MAP.get(app_label)
            if oscar_path is None:
                continue
            # Try to find a concrete oscar model with this name
            candidate = f"oscar.apps.{oscar_path}.models.{unbound_name}"
            result = _resolve_type(candidate, plugin)
            if result is not None:
                return result

    return typ


def _type_might_contain_forked_type(typ: Type, plugin: OscarPlugin) -> bool:
    """Quick check: could this type contain a forked module type?

    Used as a pre-filter before more expensive normalization.  Only returns
    True if the type (or its components) reference a forked app module.
    """
    proper = get_proper_type(typ)

    if isinstance(proper, Instance):
        fullname = proper.type.fullname
        for override_module in plugin._app_overrides.values():
            if fullname.startswith(f"{override_module}."):
                return True
        return any(_type_might_contain_forked_type(a, plugin) for a in proper.args) if proper.args else False

    if isinstance(proper, TupleType):
        return any(_type_might_contain_forked_type(item, plugin) for item in proper.items)

    if isinstance(proper, UnionType):
        return any(_type_might_contain_forked_type(item, plugin) for item in proper.items)

    # For UnboundType, we can't easily tell without resolving it, so we
    # check if the name matches a model name in any forked app.
    if isinstance(typ, UnboundType):
        unbound_name = typ.name
        for app_label in plugin._app_overrides:
            oscar_path = APP_LABEL_MAP.get(app_label)
            if oscar_path is None:
                continue
            candidate = f"oscar.apps.{oscar_path}.models.{unbound_name}"
            sym = plugin.lookup_fully_qualified(candidate)
            if sym is not None and isinstance(sym.node, TypeInfo):
                return True

    return False


def _normalize_callable_forked_to_oscar(func_type: CallableType, plugin: OscarPlugin) -> CallableType | None:
    """Reverse-map forked types in a CallableType back to oscar types.

    Handles both already-resolved Instance types and UnboundType references
    that may resolve to forked types.

    Returns the modified CallableType if any changes were made, or None
    if no remapping was needed.
    """
    # Pre-filter: check if any arg or return type might reference forked types.
    # This avoids modifying method signatures that don't need normalization,
    # which can cause spurious type errors from CallableType.copy_modified.
    has_forked = False
    for arg_type in func_type.arg_types:
        if _type_might_contain_forked_type(arg_type, plugin):
            has_forked = True
            break
    if not has_forked:
        if not _type_might_contain_forked_type(func_type.ret_type, plugin):
            return None

    changed = False

    new_arg_types: list[Type] = []
    for arg_type in func_type.arg_types:
        normalized = _resolve_and_normalize_type(arg_type, plugin)
        if normalized is not arg_type:
            changed = True
        new_arg_types.append(normalized)

    new_ret = _resolve_and_normalize_type(func_type.ret_type, plugin)
    if new_ret is not func_type.ret_type:
        changed = True

    if changed:
        return func_type.copy_modified(arg_types=new_arg_types, ret_type=new_ret)
    return None


def _remap_base_class_methods_hook(ctx: ClassDefContext, *, plugin: OscarPlugin) -> None:
    """Normalize forked types in third-party base class method signatures.

    When a class extends a third-party oscar package base class (e.g.
    oscarcch.calculator.CCHTaxCalculator), the base class may have method
    signatures containing forked types (from get_model() resolution).
    These forked types are sibling types to the oscar concrete types that
    child classes typically import via TYPE_CHECKING, causing spurious
    ``[override]`` errors.

    This hook normalizes forked types back to their oscar concrete equivalents
    in third-party base class methods, so that both parent and child use
    compatible types.

    Only fires for third-party oscar package classes -- oscar.apps.* classes
    are handled by the attribute hook.
    """
    for base_info in ctx.cls.info.mro:
        if not _is_third_party_oscar_fullname(base_info.fullname, plugin):
            continue

        for name, sym in base_info.names.items():
            if not isinstance(sym.node, FuncDef):
                continue
            func_type = sym.node.type
            if not isinstance(func_type, CallableType):
                continue
            normalized = _normalize_callable_forked_to_oscar(func_type, plugin)
            if normalized is not None:
                sym.node.type = normalized


def _remap_strategy_base_hook(ctx: ClassDefContext, *, plugin: OscarPlugin) -> None:
    """Remap PurchaseInfo return types in oscar strategy base class methods.

    When a forked app redefines PurchaseInfo (common with monkey-patching),
    this hook updates the base class method signatures so that mypy sees
    the override return types as compatible.

    During semantic analysis, return types are still UnboundType (not yet
    resolved). We replace them with the already-resolved forked Instance.
    """
    # First, apply the general base-class method remapping
    _remap_base_class_methods_hook(ctx, plugin=plugin)

    # Then handle the special PurchaseInfo case with UnboundType resolution
    if "partner" not in plugin._app_overrides:
        return

    forked_module = plugin._app_overrides["partner"]
    forked_pi = _resolve_type(f"{forked_module}.strategy.PurchaseInfo", plugin)
    if forked_pi is None:
        return

    oscar_pi_fullname = "oscar.apps.partner.strategy.PurchaseInfo"

    # Walk the MRO and remap PurchaseInfo in oscar strategy class methods
    for base_info in ctx.cls.info.mro:
        if base_info.fullname not in _STRATEGY_CLASSES:
            continue

        for method_name in ("fetch_for_product", "fetch_for_parent", "fetch_for_line"):
            sym = base_info.names.get(method_name)
            if sym is None or sym.type is None:
                continue
            # sym.type is read-only; modify the underlying FuncDef node
            if not isinstance(sym.node, FuncDef):
                continue

            func_type = sym.node.type
            if not isinstance(func_type, CallableType):
                continue

            ret = func_type.ret_type
            proper_ret = get_proper_type(ret)

            # Handle already-resolved types (Instance)
            if isinstance(proper_ret, Instance) and proper_ret.type.fullname == oscar_pi_fullname:
                sym.node.type = func_type.copy_modified(ret_type=forked_pi)
                continue

            # Handle unresolved types (UnboundType) during semantic analysis.
            # At this point the return type is still "PurchaseInfo?" — replace
            # it directly with the resolved forked PurchaseInfo Instance.
            if isinstance(ret, UnboundType) and ret.name == "PurchaseInfo":
                sym.node.type = func_type.copy_modified(ret_type=forked_pi)


def _resolve_and_remap_type(
    typ: Type,
    base_info: TypeInfo,
    plugin: OscarPlugin,
) -> Type:
    """Resolve and remap a type from an oscar base class method signature.

    Handles both fully resolved Instance types (via ``_remap_oscar_type``)
    and UnboundType references that haven't been resolved yet during early
    semantic analysis.  For UnboundType, looks up the name in the base
    class's module scope and remaps the resolved type.
    """
    # First try the normal remap (works for Instance types)
    remapped = _remap_oscar_type(typ, plugin)
    if remapped is not typ:
        return remapped

    # Handle UnboundType: resolve the name using the base class's module scope
    proper = get_proper_type(typ)
    if isinstance(proper, UnboundType):
        resolved = _resolve_unbound_oscar_type(proper, base_info, plugin)
        if resolved is not None:
            return resolved

    # Handle TupleType containing UnboundType items (e.g. tuple[AbstractLine, bool])
    if isinstance(proper, TupleType):
        changed = False
        new_items: list[Type] = []
        for item in proper.items:
            item_proper = get_proper_type(item)
            if isinstance(item_proper, UnboundType):
                resolved = _resolve_unbound_oscar_type(item_proper, base_info, plugin)
                if resolved is not None:
                    new_items.append(resolved)
                    changed = True
                    continue
            new_items.append(item)
        if changed:
            return proper.copy_modified(items=new_items)

    # Handle UnionType containing UnboundType items (e.g. AbstractOrder | None)
    if isinstance(proper, UnionType):
        changed = False
        new_items2: list[Type] = []
        for item in proper.items:
            item_proper = get_proper_type(item)
            if isinstance(item_proper, UnboundType):
                resolved = _resolve_unbound_oscar_type(item_proper, base_info, plugin)
                if resolved is not None:
                    new_items2.append(resolved)
                    changed = True
                    continue
            new_items2.append(item)
        if changed:
            return UnionType.make_union(new_items2)

    return typ


def _resolve_unbound_oscar_type(
    ubt: UnboundType,
    base_info: TypeInfo,
    plugin: OscarPlugin,
) -> Type | None:
    """Try to resolve an UnboundType from a base class's module and remap it."""
    fqn = f"{base_info.module_name}.{ubt.name}"
    sym = plugin.lookup_fully_qualified(fqn)
    if sym is not None and isinstance(sym.node, TypeInfo):
        temp_instance = Instance(sym.node, [])
        resolved = _remap_oscar_type(temp_instance, plugin)
        if resolved is not temp_instance:
            return resolved
    return None


def _unify_forked_model_hook(ctx: ClassDefContext, *, plugin: OscarPlugin) -> None:
    """Unify forked model types with their oscar concrete counterparts.

    When a forked model (e.g. ``sandbox.basket.models.Basket``) is processed,
    update the oscar concrete model's module symbol table AND patch all modules
    that have already imported the oscar type, so that all references to
    ``oscar.apps.basket.models.Basket`` resolve to the forked TypeInfo.

    This ensures that ``from oscar.apps.basket.models import Basket`` gives
    the same type as ``sandbox.basket.models.Basket`` — because at runtime,
    only one Basket model exists.

    Additionally, the oscar concrete model's TypeInfo is added to the forked
    model's MRO.  This makes the forked model a subtype of the oscar model
    from mypy's perspective.  This is necessary because third-party packages
    (e.g. oscarapicheckout) may have their method signatures normalized to use
    the oscar concrete type *before* unification runs (due to processing
    order).  Without this MRO entry, passing a forked type where a normalized
    oscar type is expected would be a type error.
    """
    forked_fullname = ctx.cls.fullname
    forked_info = ctx.cls.info

    for app_label, override_module in plugin._app_overrides.items():
        if not forked_fullname.startswith(f"{override_module}.models."):
            continue

        model_name = forked_fullname.removeprefix(f"{override_module}.models.")
        if "." in model_name:
            continue

        oscar_path = APP_LABEL_MAP.get(app_label)
        if oscar_path is None:
            continue

        oscar_model_fqn = f"oscar.apps.{oscar_path}.models.{model_name}"
        oscar_sym = plugin.lookup_fully_qualified(oscar_model_fqn)
        if oscar_sym is None or not isinstance(oscar_sym.node, TypeInfo):
            continue

        old_info = oscar_sym.node

        # Add the oscar concrete model to the forked model's MRO.
        # This establishes a subtype relationship (forked IS-A oscar) so that
        # forked types can be passed where oscar types are expected -- even if
        # those oscar types are stale Instance objects created by earlier
        # normalization passes in third-party base class hooks.
        if old_info not in forked_info.mro:
            # Insert right before the first oscar.apps.* abstract model entry
            # so that the forked model's own methods and mixin methods still
            # take precedence in resolution order.
            insert_pos = len(forked_info.mro)
            for i, base in enumerate(forked_info.mro):
                if base is not forked_info and base.fullname.startswith("oscar.apps."):
                    insert_pos = i
                    break
            forked_info.mro.insert(insert_pos, old_info)

        # Also add the forked model to the oscar concrete model's MRO.
        # This establishes the reverse subtype relationship (oscar IS-A
        # forked) so that stale Instance objects parameterized with the
        # old oscar TypeInfo (created before unification ran, e.g. by
        # django-stubs Manager/QuerySet inference) are treated as
        # compatible with the forked type.  Together with the forward
        # relationship above, this makes the two TypeInfos mutually
        # substitutable -- effectively the same type for type-checking.
        if forked_info not in old_info.mro:
            old_info.mro.insert(1, forked_info)

        # Update the oscar module's symbol table
        oscar_module_fqn = f"oscar.apps.{oscar_path}.models"
        module_sym = plugin.lookup_fully_qualified(oscar_module_fqn)
        if module_sym is not None and isinstance(module_sym.node, MypyFile):
            sym_in_module = module_sym.node.names.get(model_name)
            if sym_in_module is not None:
                sym_in_module.node = forked_info

        # Patch all modules that already imported the old TypeInfo.
        # Walk every loaded module's names dict and replace references.
        try:
            modules = ctx.api.modules  # type: ignore[attr-defined]
        except AttributeError:
            break
        for mod in modules.values():
            if not isinstance(mod, MypyFile):
                continue
            for sym_name, sym_node in mod.names.items():
                if sym_node.node is old_info:
                    sym_node.node = forked_info
        break


def _base_should_be_remapped(base_info: TypeInfo, plugin: OscarPlugin) -> bool:
    """Check if a base class's methods should have oscar types remapped.

    Returns True for:
    1. oscar.apps.* classes (abstract models, non-model classes)
    2. Third-party oscar packages (e.g. oscarapicheckout mixins)

    Third-party bases are included because their method signatures may contain
    oscar types (from get_model/get_class resolution followed by normalization),
    which need to be remapped to forked equivalents when the corresponding app
    is forked.
    """
    return base_info.fullname.startswith("oscar.apps.") or _is_third_party_oscar_fullname(base_info.fullname, plugin)


def _remap_oscar_base_methods_hook(ctx: ClassDefContext, *, plugin: OscarPlugin) -> None:
    """Remap abstract model types in oscar base class method signatures.

    When a class inherits from an oscar class — whether an abstract model
    (e.g. ``AbstractVoucher``) or a non-model class loaded via ``get_class``
    (e.g. ``BasketMiddleware``, ``ProductDetailView``) — or a third-party
    package that uses oscar types in its method signatures (e.g.
    ``oscarapicheckout.mixins.OrderCreatorMixin``), the base class methods may
    reference oscar types (abstract or concrete) in their signatures.

    At runtime, ``AbstractBasket`` doesn't exist — only the concrete Basket
    model (whether oscar's default or a forked version).  This hook remaps
    oscar types in the base class method signatures to their concrete/forked
    equivalents, preventing spurious ``[override]`` errors when child classes
    use the concrete types.
    """
    for base_info in ctx.cls.info.mro:
        if not _base_should_be_remapped(base_info, plugin):
            continue

        for name, sym in base_info.names.items():
            if not isinstance(sym.node, FuncDef):
                continue
            func_type = sym.node.type
            if not isinstance(func_type, CallableType):
                continue

            changed = False
            new_arg_types: list[Type] = []
            for arg_type in func_type.arg_types:
                remapped = _resolve_and_remap_type(arg_type, base_info, plugin)
                if remapped is not arg_type:
                    changed = True
                new_arg_types.append(remapped)

            new_ret = _resolve_and_remap_type(func_type.ret_type, base_info, plugin)
            if new_ret is not func_type.ret_type:
                changed = True

            if changed:
                sym.node.type = func_type.copy_modified(arg_types=new_arg_types, ret_type=new_ret)


# ──────────────────────────────────────────────────────────────────────
# Method hooks: remap return types on oscar method calls
# ──────────────────────────────────────────────────────────────────────


def _remap_method_return_hook(ctx: MethodContext, *, plugin: OscarPlugin) -> Type:
    """Remap the return type of oscar strategy method calls."""
    return _remap_oscar_type(ctx.default_return_type, plugin)


# ──────────────────────────────────────────────────────────────────────
# Plugin class
# ──────────────────────────────────────────────────────────────────────


class OscarPlugin(Plugin):
    """Mypy plugin that resolves oscar dynamic class loading return types.

    Detects forked oscar apps by reading INSTALLED_APPS from the Django
    settings module and resolves types from forked modules first, falling
    back to oscar's own stubs when the class/model isn't found in the fork.
    """

    def __init__(self, options: Options) -> None:
        super().__init__(options)
        self._stubbed_modules = _find_stubbed_modules()
        self._app_overrides = _detect_forked_apps(options)
        self._third_party_prefixes, self._local_prefixes = _read_oscar_package_prefixes(options)

    @staticmethod
    def _module_exists(module_name: str) -> bool:
        """Check if a Python module can be found on sys.path."""
        rel_path = module_name.replace(".", os.sep)
        for path_entry in sys.path:
            # Check as package (__init__.py)
            if os.path.isfile(os.path.join(path_entry, rel_path, "__init__.py")):
                return True
            # Check as module (.py)
            if os.path.isfile(os.path.join(path_entry, rel_path + ".py")):
                return True
        return False

    def get_additional_deps(self, file: MypyFile) -> list[tuple[int, str, int]]:
        """Declare dependencies on oscar app modules.

        When a file imports from oscar.apps.* or oscar.core.loading, ensure
        that all stubbed oscar modules AND any forked override modules are
        loaded so that type lookup succeeds in hooks.
        """
        from mypy.build import PRI_HIGH

        has_oscar_import = False
        for imp in file.imports:
            if isinstance(imp, (ImportFrom, ImportAll)):
                if imp.id == "oscar.core.loading" or imp.id.startswith("oscar.apps."):
                    has_oscar_import = True
                    break
            elif isinstance(imp, Import):
                if any(mod_id == "oscar.core.loading" or mod_id.startswith("oscar.apps.") for mod_id, _ in imp.ids):
                    has_oscar_import = True
                    break
        if not has_oscar_import:
            return []

        deps: list[tuple[int, str, int]] = []

        # Oscar stub modules — use PRI_HIGH so they're available before
        # the first semantic analysis pass of the importing module.
        for mod in sorted(self._stubbed_modules):
            deps.append((PRI_HIGH, mod, -1))

        # Forked app modules — only add deps for modules that actually have
        # a models submodule (avoid import errors for dashboard apps etc.)
        for override_module in sorted(self._app_overrides.values()):
            models_mod = f"{override_module}.models"
            if self._module_exists(models_mod):
                deps.append((PRI_HIGH, models_mod, -1))

        return deps

    def _is_oscar_related_class(self, class_fullname: str) -> bool:
        """Check if a class belongs to oscar, a forked app, or an oscar-using package."""
        if class_fullname.startswith("oscar.apps."):
            return True

        # Third-party oscar-using packages (installed)
        for prefix in self._third_party_prefixes:
            if class_fullname.startswith(prefix):
                return True

        # Project-local oscar-using packages
        for prefix in self._local_prefixes:
            if class_fullname.startswith(prefix):
                return True

        # Forked app modules
        for override_module in self._app_overrides.values():
            if class_fullname.startswith(f"{override_module}."):
                return True

        return False

    def get_customize_class_mro_hook(self, fullname: str) -> Callable[[ClassDefContext], None] | None:
        """Remap abstract model types in oscar base class method signatures.

        The django-stubs plugin intercepts get_base_class_hook for all Model
        subclasses, so we use get_customize_class_mro_hook instead.  This fires
        for every class after MRO computation.  We check if the class has any
        oscar.apps.* class in its MRO and, if so, remap abstract types in
        those base class method signatures to concrete equivalents.

        This covers both abstract models (e.g. AbstractVoucher) and non-model
        classes loaded via get_class (e.g. BasketMiddleware, ProductDetailView).
        """
        info = self.lookup_fully_qualified(fullname)
        if info is None or not isinstance(info.node, TypeInfo):
            return None

        # Check if this is a forked concrete model
        is_forked_model = False
        for override_module in self._app_overrides.values():
            if fullname.startswith(f"{override_module}.models."):
                model_name = fullname.removeprefix(f"{override_module}.models.")
                if "." not in model_name:
                    is_forked_model = True
                    break

        has_oscar_base = any(b.fullname.startswith("oscar.apps.") for b in info.node.mro)

        if is_forked_model and has_oscar_base:

            def combined_hook(ctx: ClassDefContext, *, plugin: OscarPlugin = self) -> None:
                _unify_forked_model_hook(ctx, plugin=plugin)
                _remap_oscar_base_methods_hook(ctx, plugin=plugin)

            return combined_hook
        elif is_forked_model:
            return partial(_unify_forked_model_hook, plugin=self)
        elif has_oscar_base:
            return partial(_remap_oscar_base_methods_hook, plugin=self)
        return None

    def get_attribute_hook(self, fullname: str) -> Callable[[AttributeContext], Type] | None:
        """Remap oscar types to forked equivalents on attribute access.

        Fires for attribute access on:
        1. oscar.apps.* classes (abstract and concrete models)
        2. Forked module classes (so that inherited oscar fields are remapped)
        3. Third-party oscar-using packages (oscarcch, oscarbluelight, etc.)

        This ensures that field types (e.g. ForeignKey targets) are remapped
        to forked app types when the app is forked.
        """
        # fullname is "some.module.ClassName.attr_name"
        class_fullname, _, _ = fullname.rpartition(".")
        if self._is_oscar_related_class(class_fullname):
            return partial(_remap_oscar_attr_hook, plugin=self)

        return None

    def get_base_class_hook(self, fullname: str) -> Callable[[ClassDefContext], None] | None:
        """Normalize types in base class method signatures.

        Handles two cases:
        1. Strategy classes: special PurchaseInfo → forked PurchaseInfo remapping.
        2. Third-party oscar packages: normalize forked types (from get_model())
           back to oscar concrete types so they match child class imports.

        Note: oscar abstract models are handled by get_customize_class_mro_hook
        because the django-stubs plugin intercepts get_base_class_hook for all
        Model subclasses.
        """
        if fullname in _STRATEGY_CLASSES:
            return partial(_remap_strategy_base_hook, plugin=self)
        if _is_third_party_oscar_fullname(fullname, self):
            return partial(_remap_base_class_methods_hook, plugin=self)
        return None

    def _is_method_hook_class(self, class_fullname: str) -> bool:
        """Check if a class should have its method return types remapped.

        The method hook is more targeted than the attribute hook. It fires for:
        1. oscar.apps.* classes (strategy classes, models, etc.)
        2. Forked app modules (overridden strategy classes)

        It does NOT fire for third-party or project-local oscar packages because
        those don't typically need return type remapping (their types are already
        resolved by get_model()) and broad method hook registration can cause
        spurious type errors.
        """
        if class_fullname.startswith("oscar.apps."):
            return True

        for override_module in self._app_overrides.values():
            if class_fullname.startswith(f"{override_module}."):
                return True

        return False

    def get_method_hook(self, fullname: str) -> Callable[[MethodContext], Type] | None:
        """Remap oscar types in method call return values.

        Ensures that calling e.g. strategy.fetch_for_product() returns
        the forked PurchaseInfo type instead of the oscar stub type.
        """
        class_fullname, _, _ = fullname.rpartition(".")
        if self._is_method_hook_class(class_fullname):
            return partial(_remap_method_return_hook, plugin=self)

        return None

    def get_dynamic_class_hook(self, fullname: str) -> Callable[[DynamicClassDefContext], None] | None:
        """Handle Name = get_model/get_class(...) assignments as type aliases."""
        if fullname == _OSCAR_GET_MODEL:
            return partial(_get_model_dynamic_class_hook, plugin=self)
        if fullname == _OSCAR_GET_CLASS:
            return partial(_get_class_dynamic_class_hook, plugin=self)
        return None

    def get_function_hook(self, fullname: str) -> Callable[[FunctionContext], Type] | None:
        if fullname == _OSCAR_GET_MODEL:
            return partial(_get_model_hook, plugin=self)
        if fullname == _OSCAR_GET_CLASS:
            return partial(_get_class_hook, plugin=self)
        if fullname == _OSCAR_GET_CLASSES:
            return partial(_get_classes_hook, plugin=self)
        return None


def plugin(version: str) -> type[OscarPlugin]:
    return OscarPlugin
