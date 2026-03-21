from typing import ClassVar

from django.db import models
from oscar.apps.basket.abstract_models import (
    AbstractBasket as AbstractBasket,
)
from oscar.apps.basket.abstract_models import (
    AbstractLine as AbstractLine,
)
from oscar.apps.basket.abstract_models import (
    AbstractLineAttribute as AbstractLineAttribute,
)

class InvalidBasketLineError(Exception): ...

class Basket(AbstractBasket):
    id: int
    objects: ClassVar[models.Manager[Basket]]

class Line(AbstractLine):
    id: int

class LineAttribute(AbstractLineAttribute):
    id: int
