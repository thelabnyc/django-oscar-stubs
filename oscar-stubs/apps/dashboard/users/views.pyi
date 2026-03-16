from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views.generic import DeleteView, DetailView, FormView, ListView, UpdateView
from django.views.generic.detail import SingleObjectMixin
from django.views.generic.edit import FormMixin
from django_tables2 import SingleTableView
from oscar.views.generic import BulkEditMixin

class IndexView(BulkEditMixin, FormMixin, SingleTableView):
    template_name: str
    actions: tuple[str, ...]
    form_class: type
    table_class: type
    context_table_name: str
    desc_template: str
    description: str
    form: Any
    desc_ctx: dict[str, str]

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_table_pagination(self, table: Any) -> dict[str, int]: ...
    def get_form_kwargs(self) -> dict[str, Any]: ...
    def get_queryset(self) -> QuerySet[Any]: ...
    def apply_search(self, queryset: QuerySet[Any]) -> QuerySet[Any]: ...
    def apply_search_filters(self, queryset: QuerySet[Any], data: dict[str, Any]) -> QuerySet[Any]: ...
    def get_table(self, **kwargs: Any) -> Any: ...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
    def make_inactive(self, request: HttpRequest, users: QuerySet[Any]) -> HttpResponse: ...
    def make_active(self, request: HttpRequest, users: QuerySet[Any]) -> HttpResponse: ...

class UserDetailView(DetailView):
    template_name: str
    context_object_name: str
    def get_queryset(self) -> QuerySet[Any]: ...

class PasswordResetView(SingleObjectMixin, FormView):
    form_class: type
    http_method_names: list[str]
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_form_kwargs(self) -> dict[str, Any]: ...
    def form_valid(self, form: Any) -> HttpResponse: ...
    def get_success_url(self) -> str: ...

class ProductAlertListView(ListView):
    form_class: type
    context_object_name: str
    template_name: str
    paginate_by: int
    base_description: str
    description: str
    form: Any
    def get_queryset(self) -> QuerySet[Any]: ...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

class ProductAlertUpdateView(UpdateView):
    template_name: str
    form_class: type
    context_object_name: str
    def get_success_url(self) -> str: ...

class ProductAlertDeleteView(DeleteView):
    template_name: str
    context_object_name: str
    def get_success_url(self) -> str: ...
