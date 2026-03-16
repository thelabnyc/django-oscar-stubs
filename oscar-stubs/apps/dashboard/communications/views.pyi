from typing import Any

from django.http import HttpResponse
from django.views import generic

class ListView(generic.ListView):
    template_name: str
    context_object_name: str

class UpdateView(generic.UpdateView):
    form_class: type
    template_name: str
    context_object_name: str
    success_url: str
    slug_field: str
    def form_invalid(self, form: Any) -> HttpResponse: ...
    def form_valid(self, form: Any) -> HttpResponse: ...
    def get_messages_context(self, form: Any) -> dict[str, Any]: ...
    def show_preview(self, form: Any) -> HttpResponse: ...
    def send_preview(self, form: Any) -> HttpResponse: ...
