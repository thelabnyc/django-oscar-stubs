from typing import Any

from django import template
from django.http import HttpRequest
from oscar.apps.catalogue.abstract_models import AbstractProduct
from oscar.apps.partner.strategy import PurchaseInfo

register: template.Library

def purchase_info_for_product(request: HttpRequest, product: AbstractProduct) -> PurchaseInfo: ...
def purchase_info_for_line(request: HttpRequest, line: Any) -> PurchaseInfo: ...
