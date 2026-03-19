from typing import Any

from django.db.models import QuerySet
from django.http import HttpResponse
from oscar.apps.dashboard.reports.reports import (
    ReportCSVFormatter,
    ReportGenerator,
    ReportHTMLFormatter,
)

class VoucherReportCSVFormatter(ReportCSVFormatter):
    filename_template: str
    def generate_csv(self, response: HttpResponse, vouchers: QuerySet[Any]) -> None: ...

class VoucherReportHTMLFormatter(ReportHTMLFormatter):
    filename_template: str

class VoucherReportGenerator(ReportGenerator):
    code: str
    description: str
    model_class: type
    formatters: dict[str, type]
