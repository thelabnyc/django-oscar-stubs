from typing import Any

from django.db.models.expressions import Subquery

EXPAND_UPWARDS_CATEGORY_QUERY: str
EXPAND_DOWNWARDS_CATEGORY_QUERY: str

class ExpandUpwardsCategoryQueryset(Subquery):
    def as_sqlite(self, compiler: Any, connection: Any) -> tuple[str, list[Any]]: ...

class ExpandDownwardsCategoryQueryset(Subquery):
    def as_sqlite(self, compiler: Any, connection: Any) -> tuple[str, list[Any]]: ...
