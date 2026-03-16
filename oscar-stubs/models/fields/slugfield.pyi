from typing import Any

from django.db.models import SlugField as DjangoSlugField

class SlugField(DjangoSlugField):
    def __init__(self, *args: Any, **kwargs: Any) -> None: ...
