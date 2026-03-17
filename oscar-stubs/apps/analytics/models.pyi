from oscar.apps.analytics.abstract_models import (
    AbstractProductRecord,
    AbstractUserProductView,
    AbstractUserRecord,
    AbstractUserSearch,
)

class ProductRecord(AbstractProductRecord):
    id: int

class UserRecord(AbstractUserRecord):
    id: int

class UserProductView(AbstractUserProductView):
    id: int

class UserSearch(AbstractUserSearch):
    id: int
