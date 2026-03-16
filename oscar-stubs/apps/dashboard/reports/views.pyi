from typing import Any

from django.http import HttpRequest, HttpResponse
from django.views.generic import ListView

class IndexView(ListView):
    template_name: str
    paginate_by: int
    context_object_name: str
    report_form_class: type
    generator_repository: type
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
