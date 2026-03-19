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
from mypy.plugin import AttributeContext, DynamicClassDefContext, FunctionContext, Plugin
from mypy.types import AnyType, Instance, TupleType, Type, TypeOfAny, TypeType, UnionType, get_proper_type

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

    config = configparser.ConfigParser()
    try:
        config.read(options.config_file)
    except (configparser.Error, OSError):
        return None

    for section in ("mypy.plugins.django-stubs", "mypy_django_plugin"):
        if config.has_section(section):
            val = config.get(section, "django_settings_module", fallback=None)
            if val:
                return val

    return None


def _find_settings_file(settings_module: str) -> str | None:
    """Locate the settings .py file on the filesystem."""
    rel_path = settings_module.replace(".", os.sep) + ".py"
    for path_entry in sys.path:
        full_path = os.path.join(path_entry, rel_path)
        if os.path.isfile(full_path):
            return full_path
    return None


def _collect_app_config_entries(settings_file: str) -> list[str]:
    """Collect all AppConfig-style entries from the settings file.

    Scans the entire file for string literals matching the pattern
    ``some.module.apps.ClassName``. This catches entries in the original
    INSTALLED_APPS list as well as index-based replacements like::

        idx = INSTALLED_APPS.index("oscar.apps.partner.apps.PartnerConfig")
        INSTALLED_APPS[idx] = "myproject.partner.apps.PartnerConfig"

    Returns only non-oscar entries (entries whose module path does NOT
    start with ``oscar.``).
    """
    try:
        with open(settings_file) as f:
            tree = ast.parse(f.read())
    except (OSError, SyntaxError):
        return []

    entries: list[str] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Constant) and isinstance(node.value, str):
            value = node.value
            # Match pattern: dotted.path.apps.ClassName
            if ".apps." in value and not value.startswith("oscar.") and not value.startswith("django."):
                # Heuristic: the part after the last dot should be CamelCase (a class name)
                last_part = value.rsplit(".", 1)[-1]
                if last_part and last_part[0].isupper():
                    entries.append(value)

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
# Abstract → concrete model remapping
# ──────────────────────────────────────────────────────────────────────

# Pattern: oscar.apps.<path>.abstract_models.Abstract<Name>
_ABSTRACT_MODEL_RE = re.compile(r"^oscar\.apps\.(.+)\.abstract_models\.Abstract(\w+)$")


def _is_oscar_abstract_model(fullname: str) -> bool:
    """Check if a fully qualified name is an oscar abstract model class."""
    return _ABSTRACT_MODEL_RE.match(fullname) is not None


def _resolve_abstract_to_concrete(fullname: str, plugin: OscarPlugin) -> Type | None:
    """Resolve an oscar abstract model fullname to its concrete model type.

    E.g. oscar.apps.address.abstract_models.AbstractCountry → Country
    from oscar.apps.address.models (or forked equivalent).
    """
    m = _ABSTRACT_MODEL_RE.match(fullname)
    if m is None:
        return None
    oscar_path = m.group(1)  # e.g. "address", "catalogue.reviews"
    model_name = m.group(2)  # e.g. "Country" (without "Abstract" prefix)

    app_label = _OSCAR_PATH_TO_LABEL.get(oscar_path)
    if app_label is None:
        return None

    return _resolve_model(app_label, model_name, plugin)


def _remap_abstract_type(typ: Type, plugin: OscarPlugin) -> Type:
    """Recursively walk a type, replacing oscar abstract model instances with concrete ones."""
    typ = get_proper_type(typ)

    if isinstance(typ, Instance):
        fullname = typ.type.fullname
        # If this is an oscar abstract model, resolve to concrete
        if _is_oscar_abstract_model(fullname):
            concrete = _resolve_abstract_to_concrete(fullname, plugin)
            if concrete is not None:
                concrete = get_proper_type(concrete)
                # Carry over type args from the original if the concrete has matching params
                if isinstance(concrete, Instance) and typ.args:
                    concrete = concrete.copy_modified(args=[_remap_abstract_type(a, plugin) for a in typ.args])
                return concrete

        # Even if not abstract itself, remap type args (e.g. QuerySet[AbstractProduct])
        if typ.args:
            new_args = [_remap_abstract_type(a, plugin) for a in typ.args]
            if new_args != list(typ.args):
                return typ.copy_modified(args=new_args)

    elif isinstance(typ, UnionType):
        new_items = [_remap_abstract_type(item, plugin) for item in typ.items]
        if new_items != typ.items:
            return UnionType.make_union(new_items)

    return typ


def _remap_abstract_attr_hook(ctx: AttributeContext, *, plugin: OscarPlugin) -> Type:
    """Attribute hook callback: remap abstract model types to concrete ones."""
    # Don't remap setter types — keep abstract (more permissive) for assignments
    if ctx.is_lvalue:
        return ctx.default_attr_type

    return _remap_abstract_type(ctx.default_attr_type, plugin)


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

        # Forked app modules (especially their models)
        for override_module in sorted(self._app_overrides.values()):
            deps.append((PRI_HIGH, f"{override_module}.models", -1))

        return deps

    def get_attribute_hook(self, fullname: str) -> Callable[[AttributeContext], Type] | None:
        """Remap abstract model types to concrete ones on attribute access."""
        # fullname is "some.module.ClassName.attr_name"
        class_fullname, _, _ = fullname.rpartition(".")
        if _is_oscar_abstract_model(class_fullname):
            return partial(_remap_abstract_attr_hook, plugin=self)
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
