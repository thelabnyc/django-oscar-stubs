from oscar.apps.address.abstract_models import AbstractPartnerAddress
from oscar.apps.partner.abstract_models import AbstractPartner, AbstractStockAlert, AbstractStockRecord

class Partner(AbstractPartner):
    id: int

class PartnerAddress(AbstractPartnerAddress):
    id: int

class StockRecord(AbstractStockRecord):
    id: int

class StockAlert(AbstractStockAlert):
    id: int
