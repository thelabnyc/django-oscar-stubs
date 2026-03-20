from django.utils.functional import _StrPromise
from oscar.core.application import OscarConfig

class AddressConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
