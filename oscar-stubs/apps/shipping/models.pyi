from oscar.apps.shipping.abstract_models import (
    AbstractOrderAndItemCharges,
    AbstractWeightBand,
    AbstractWeightBased,
)

class OrderAndItemCharges(AbstractOrderAndItemCharges):
    id: int

class WeightBased(AbstractWeightBased):
    id: int

class WeightBand(AbstractWeightBand):
    id: int
