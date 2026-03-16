from typing import Any

from django.db.models import QuerySet
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.views.generic import ListView

class PageListView(ListView):
    template_name: str
    form_class: type
    paginate_by: int
    desc_template: str
    form: Any
    desc_ctx: dict[str, str]
    def get_queryset(self) -> QuerySet[Any]: ...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

class PageCreateUpdateMixin:
    template_name: str
    form_class: type
    context_object_name: str
    def get_success_url(self) -> str: ...
    def form_valid(self, form: Any) -> HttpResponseRedirect: ...

class PageCreateView(PageCreateUpdateMixin, generic.CreateView):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
    def form_valid(self, form: Any) -> HttpResponse: ...

class PageUpdateView(PageCreateUpdateMixin, generic.UpdateView):
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

class PageDeleteView(generic.DeleteView):
    template_name: str
    def get_success_url(self) -> str: ...
