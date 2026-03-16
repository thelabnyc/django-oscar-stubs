from typing import Any

from django.db.models import QuerySet
from django_tables2 import Column, LinkColumn, TemplateColumn
from oscar.apps.dashboard.tables import DashboardTable

class UserTable(DashboardTable):
    check: TemplateColumn
    email: LinkColumn
    name: Column
    active: Column
    staff: Column
    date_registered: Column
    num_orders: Column
    actions: TemplateColumn
    icon: str

    class Meta(DashboardTable.Meta):
        template_name: str

    def order_num_orders(self, queryset: QuerySet[Any], is_descending: bool) -> tuple[QuerySet[Any], bool]: ...
