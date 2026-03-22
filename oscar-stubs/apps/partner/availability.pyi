from typing import ClassVar
import datetime

class Base:
    @property
    def code(self) -> str: ...
    @property
    def message(self) -> str: ...
    dispatch_date: ClassVar[datetime.date | None]
    # num_available is defined by subclasses (e.g. StockRequired) and accessed
    # by oscar.apps.basket.abstract_models and other oscar code on Base-typed
    # references. Declared here so that callers using Base don't need to narrow.
    @property
    def num_available(self) -> int: ...
    @property
    def short_message(self) -> str: ...
    @property
    def is_available_to_buy(self) -> bool: ...
    def is_purchase_permitted(self, quantity: int) -> tuple[bool, str]: ...

class Unavailable(Base):
    code: ClassVar[str]
    message: ClassVar[str]

class Available(Base):
    code: ClassVar[str]
    message: ClassVar[str]

    def is_purchase_permitted(self, quantity: int) -> tuple[bool, str]: ...

class StockRequired(Base):
    CODE_IN_STOCK: ClassVar[str]
    CODE_OUT_OF_STOCK: ClassVar[str]

    num_available: int

    def __init__(self, num_available: int) -> None: ...
    def is_purchase_permitted(self, quantity: int) -> tuple[bool, str]: ...
    @property
    def code(self) -> str: ...
    @property
    def short_message(self) -> str: ...
    @property
    def message(self) -> str: ...
