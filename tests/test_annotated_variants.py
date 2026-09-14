"""Tests for the plugin's repair of django-stubs' `Model@AnnotatedWith` classes."""

from collections.abc import Sequence

from mypy.mro import calculate_mro
from mypy.nodes import GDEF, Block, ClassDef, SymbolTable, SymbolTableNode, TypeInfo
from mypy.types import Instance
import pytest

from mypy_oscar_plugin import _rebase_annotated_variants

OSCAR_ORDER = "oscar.apps.order.models.Order"
FORKED_ORDER = "myproject.order.models.Order"
MIXIN = "thirdparty.mixins.OrderMixin"
ANNOTATED = "@AnnotatedWith"


def make_type_info(fullname: str, bases: Sequence[TypeInfo] = ()) -> TypeInfo:
    module, _, name = fullname.rpartition(".")
    defn = ClassDef(name, Block([]))
    defn.fullname = fullname
    info = TypeInfo(SymbolTable(), defn, module)
    defn.info = info
    info.bases = [Instance(base, []) for base in bases]
    calculate_mro(info)
    return info


def cross_link(oscar_info: TypeInfo, forked_info: TypeInfo) -> None:
    """Stand in for the MRO half of `_unify_forked_model_hook`."""
    forked_info.mro.insert(forked_info.mro.index(oscar_info.mro[1]), oscar_info)
    oscar_info.mro.insert(1, forked_info)


class Models:
    """The TypeInfos the plugin sees for an oscar app whose order model is forked."""

    def __init__(self) -> None:
        self.object = make_type_info("builtins.object")
        self.annotations = make_type_info("django_stubs_ext.annotations.Annotations", [self.object])
        self.abstract = make_type_info("oscar.apps.order.abstract_models.AbstractOrder", [self.object])
        self.oscar = make_type_info(OSCAR_ORDER, [self.abstract])
        self.mixin = make_type_info(MIXIN, [self.object])
        self.forked = make_type_info(FORKED_ORDER, [self.mixin, self.abstract])

    def annotated(self, model_info: TypeInfo) -> TypeInfo:
        return make_type_info(model_info.fullname + ANNOTATED, [model_info, self.annotations])

    def rebase(self, annotated_by_fullname: dict[str, TypeInfo]) -> None:
        def lookup(fullname: str) -> SymbolTableNode | None:
            info = annotated_by_fullname.get(fullname)
            return None if info is None else SymbolTableNode(GDEF, info)

        _rebase_annotated_variants(OSCAR_ORDER, self.forked, lookup)


@pytest.fixture
def models() -> Models:
    return Models()


def test_star_imported_variant_is_rebased_onto_the_fork(models: Models) -> None:
    """A forked models module star-imports oscar's, so both names can reach one variant."""
    annotated = models.annotated(models.oscar)
    cross_link(models.oscar, models.forked)
    assert models.forked not in annotated.mro

    models.rebase(
        {
            OSCAR_ORDER + ANNOTATED: annotated,
            FORKED_ORDER + ANNOTATED: annotated,
        }
    )

    assert annotated.bases[0].type is models.forked
    assert models.forked in annotated.mro
    # The fork's own bases have to be reachable, or its fields go missing.
    assert models.mixin in annotated.mro
    # Still usable where the oscar model is expected.
    assert models.oscar in annotated.mro


def test_variant_built_before_unification_learns_the_oscar_base(models: Models) -> None:
    annotated = models.annotated(models.forked)
    assert models.oscar not in annotated.mro

    cross_link(models.oscar, models.forked)
    models.rebase({FORKED_ORDER + ANNOTATED: annotated})

    assert models.oscar in annotated.mro
    assert annotated.mro.index(models.forked) < annotated.mro.index(models.oscar)


def test_variant_built_after_unification_is_rebased(models: Models) -> None:
    """Once oscar's module points at the fork, only the name still identifies oscar's model."""
    cross_link(models.oscar, models.forked)
    annotated = models.annotated(models.oscar)
    assert models.mixin not in annotated.mro

    models.rebase({OSCAR_ORDER + ANNOTATED: annotated})

    assert annotated.bases[0].type is models.forked
    assert models.mixin in annotated.mro


def test_repair_is_idempotent(models: Models) -> None:
    """The hook runs on every semantic analysis pass."""
    annotated = models.annotated(models.oscar)
    cross_link(models.oscar, models.forked)

    models.rebase({OSCAR_ORDER + ANNOTATED: annotated})
    once = list(annotated.mro)
    models.rebase({OSCAR_ORDER + ANNOTATED: annotated})

    assert annotated.mro == once
    assert len(set(annotated.mro)) == len(annotated.mro)


def test_variant_that_was_never_built_is_ignored(models: Models) -> None:
    cross_link(models.oscar, models.forked)
    forked_mro = list(models.forked.mro)
    oscar_mro = list(models.oscar.mro)

    models.rebase({})

    assert models.forked.mro == forked_mro
    assert models.oscar.mro == oscar_mro
