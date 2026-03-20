from django.utils.functional import _StrPromise
from oscar.core.application import OscarConfig

class CommunicationConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str | _StrPromise
