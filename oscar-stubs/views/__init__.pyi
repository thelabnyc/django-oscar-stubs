from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse

def handler403(request: HttpRequest, exception: Exception) -> HttpResponse: ...
def handler404(request: HttpRequest, exception: Exception) -> HttpResponse: ...
def handler500(request: HttpRequest) -> HttpResponse: ...
def sort_queryset(
    queryset: QuerySet[Any],
    request: HttpRequest,
    allowed_sorts: list[str],
    default: str | None = ...,
) -> QuerySet[Any]: ...
