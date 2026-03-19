from typing import Any

from django.db.models import QuerySet
from django.http import HttpRequest, HttpResponse, HttpResponseRedirect
from django.utils.functional import _StrPromise
from django.views.generic import DeleteView, ListView
from oscar.apps.dashboard.offers.wizard_views import OfferWizardStepView
from oscar.views import sort_queryset as sort_queryset

class OfferListView(ListView):
    context_object_name: str
    template_name: str
    form_class: type
    paginate_by: int
    form: Any
    advanced_form: Any
    search_filters: list[str | _StrPromise]
    def get_queryset(self) -> QuerySet[Any]: ...
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]: ...

class OfferMetaDataView(OfferWizardStepView):
    step_name: str
    form_class: type
    template_name: str
    url_name: str
    success_url_name: str
    def get_instance(self) -> Any: ...
    def get_title(self) -> str: ...

class OfferBenefitView(OfferWizardStepView):
    step_name: str
    form_class: type
    template_name: str
    url_name: str
    success_url_name: str
    previous_view: type
    def get_instance(self) -> Any: ...
    def get_title(self) -> str: ...

class OfferConditionView(OfferWizardStepView):
    step_name: str
    form_class: type
    template_name: str
    url_name: str
    success_url_name: str
    previous_view: type
    def get_instance(self) -> Any: ...

class OfferRestrictionsView(OfferWizardStepView):
    step_name: str
    form_class: type
    template_name: str
    previous_view: type
    url_name: str
    def form_valid(self, form: Any) -> HttpResponse: ...
    def get_instance(self) -> Any: ...
    def get_title(self) -> str: ...

class OfferDeleteView(DeleteView):
    template_name: str
    context_object_name: str
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def get_success_url(self) -> str: ...

class OfferDetailView(ListView):
    template_name: str
    context_object_name: str
    paginate_by: int
    offer: Any
    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse: ...
    def post(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse | None: ...
    def suspend(self) -> HttpResponseRedirect: ...
    def unsuspend(self) -> HttpResponseRedirect: ...
    def get_queryset(self) -> QuerySet[Any]: ...
    def get_context_data(self, *args: Any, **kwargs: Any) -> dict[str, Any]: ...
    def render_to_response(self, context: dict[str, Any], *args: Any, **kwargs: Any) -> HttpResponse: ...
