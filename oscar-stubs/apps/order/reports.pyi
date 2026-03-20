from typing import Any

from django.db.models import QuerySet
from django.http import HttpResponse
from oscar.apps.dashboard.reports.reports import (
    ReportCSVFormatter as ReportCSVFormatter,
)
from oscar.apps.dashboard.reports.reports import (
    ReportGenerator as ReportGenerator,
)
from oscar.apps.dashboard.reports.reports import (
    ReportHTMLFormatter as ReportHTMLFormatter,
)
from oscar.apps.order.abstract_models import AbstractOrder

Order: type[AbstractOrder]

class OrderReportCSVFormatter(ReportCSVFormatter):
    filename_template: str
    def generate_csv(self, response: HttpResponse, orders: QuerySet[Any]) -> None: ...
    def filename(self, **kwargs: Any) -> str: ...

class OrderReportHTMLFormatter(ReportHTMLFormatter):
    filename_template: str

class OrderReportGenerator(ReportGenerator):
    code: str
    description: str
    date_range_field_name: str
    model_class: type[AbstractOrder]
    formatters: dict[str, type]
    def generate(self) -> HttpResponse | QuerySet[Any]: ...
    def is_available_to(self, user: Any) -> bool: ...
