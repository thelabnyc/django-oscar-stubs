from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse
from django.views import generic

class WeightBasedListView(generic.ListView):
    template_name: str
    context_object_name: str

class WeightBasedCreateView(generic.CreateView):
    form_class: type
    template_name: str
    def get_success_url(self) -> str: ...

class WeightBasedDetailView(generic.CreateView):
    form_class: type
    template_name: str
    method: Any
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_form_kwargs(self, **kwargs: Any) -> dict[str, Any]: ...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...
    def get_success_url(self) -> str: ...

class WeightBasedUpdateView(generic.UpdateView):
    form_class: type
    template_name: str
    context_object_name: str
    def get_success_url(self) -> str: ...

class WeightBandUpdateView(generic.UpdateView):
    form_class: type
    template_name: str
    context_object_name: str
    method: Any
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_queryset(self) -> QuerySet[Any]: ...
    def get_form_kwargs(self, **kwargs: Any) -> dict[str, Any]: ...
    def get_success_url(self) -> str: ...

class WeightBandDeleteView(generic.DeleteView):
    template_name: str
    context_object_name: str
    method: Any
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_queryset(self) -> QuerySet[Any]: ...
    def get_success_url(self) -> str: ...

class WeightBasedDeleteView(generic.DeleteView):
    template_name: str
    context_object_name: str
    def get_success_url(self) -> str: ...
