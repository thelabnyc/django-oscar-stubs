from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.views import generic
from oscar.views.generic import BulkEditMixin

class ReviewListView(BulkEditMixin, generic.ListView):
    template_name: str
    context_object_name: str
    form_class: type
    review_form_class: type
    paginate_by: int
    actions: tuple[str, ...]
    checkbox_object_name: str
    desc_template: str
    form: Any
    desc_ctx: dict[str, str]

    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_date_from_to_queryset(
        self, date_from: Any, date_to: Any, queryset: QuerySet[Any] | None = ...
    ) -> QuerySet[Any]: ...
    def get_queryset(self) -> QuerySet[Any]: ...
    def add_filter_status(self, queryset: QuerySet[Any], status: str) -> QuerySet[Any]: ...
    def add_filter_keyword(self, queryset: QuerySet[Any], keyword: str) -> QuerySet[Any]: ...
    def add_filter_name(self, queryset: QuerySet[Any], name: str) -> QuerySet[Any]: ...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
    def update_selected_review_status(self, request: HttpRequest, reviews: QuerySet[Any]) -> HttpResponseRedirect: ...

class ReviewUpdateView(generic.UpdateView):
    template_name: str
    form_class: type
    context_object_name: str
    def get_success_url(self) -> str: ...

class ReviewDeleteView(generic.DeleteView):
    template_name: str
    context_object_name: str
    def get_success_url(self) -> str: ...
