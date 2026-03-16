from typing import Any

from django.db.models import QuerySet
from django.http import HttpResponse
from oscar.apps.dashboard.reports.reports import ReportCSVFormatter

class OrderDiscountCSVFormatter(ReportCSVFormatter):
    filename_template: str
    def generate_csv(self, response: HttpResponse, order_discounts: QuerySet[Any]) -> None: ...
    def filename(self, offer: Any) -> str: ...
