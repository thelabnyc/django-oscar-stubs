from typing import Any

from django_tables2 import Column, LinkColumn, TemplateColumn
from oscar.apps.dashboard.tables import DashboardTable

class ProductTable(DashboardTable):
    checkbox: TemplateColumn
    title: TemplateColumn
    image: TemplateColumn
    product_class: Column
    variants: TemplateColumn
    stock_records: TemplateColumn
    actions: TemplateColumn
    icon: str

    class Meta(DashboardTable.Meta):
        model: type
        template_name: str
        fields: tuple[str, ...]
        sequence: tuple[str, ...]
        order_by: str

class CategoryTable(DashboardTable):
    checkbox: TemplateColumn
    description: TemplateColumn
    num_children: LinkColumn
    actions: TemplateColumn
    icon: str
    caption: str
    def render_name(self, value: Any, record: Any) -> str: ...

    class Meta(DashboardTable.Meta):
        model: type
        template_name: str
        fields: tuple[str, ...]
        sequence: tuple[str, ...]

class AttributeOptionGroupTable(DashboardTable):
    name: TemplateColumn
    option_summary: TemplateColumn
    actions: TemplateColumn
    icon: str
    caption: str

    class Meta(DashboardTable.Meta):
        model: type
        fields: tuple[str, ...]
        sequence: tuple[str, ...]
        per_page: int

class OptionTable(DashboardTable):
    name: TemplateColumn
    actions: TemplateColumn
    icon: str
    caption: str

    class Meta(DashboardTable.Meta):
        model: type
        fields: tuple[str, ...]
        sequence: tuple[str, ...]
        per_page: int
