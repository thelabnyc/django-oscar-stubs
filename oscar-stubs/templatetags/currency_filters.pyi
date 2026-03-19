from decimal import Decimal

from django import template

register: template.Library

def currency(value: Decimal | str | float, currency_format: str | None = ...) -> str: ...
