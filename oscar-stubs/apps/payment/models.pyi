from oscar.apps.payment.abstract_models import (
    AbstractBankcard,
    AbstractSource,
    AbstractSourceType,
    AbstractTransaction,
)

class Transaction(AbstractTransaction):
    id: int

class Source(AbstractSource):
    id: int

class SourceType(AbstractSourceType):
    id: int

class Bankcard(AbstractBankcard):
    id: int
