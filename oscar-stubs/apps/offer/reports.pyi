from typing import Any

from django.db.models import QuerySet
from django.http import HttpResponse
from oscar.apps.dashboard.reports.reports import (
    ReportCSVFormatter,
    ReportGenerator,
    ReportHTMLFormatter,
)

class OfferReportCSVFormatter(ReportCSVFormatter):
    filename_template: str
    def generate_csv(self, response: HttpResponse, offer_discounts: QuerySet[Any]) -> None: ...

class OfferReportHTMLFormatter(ReportHTMLFormatter):
    filename_template: str

class OfferReportGenerator(ReportGenerator):
    code: str
    description: str
    model_class: type
    formatters: dict[str, type]
    def get_queryset(self) -> QuerySet[Any]: ...
