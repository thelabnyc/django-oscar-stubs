from typing import Any
import datetime

from django import forms
from django.contrib.auth import forms as auth_forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.sites.requests import RequestSite
from django.db import models

def generate_username() -> str: ...

class PasswordResetForm(auth_forms.PasswordResetForm):
    def save(self, *args: Any, domain_override: str | None = ..., request: Any | None = ..., **kwargs: Any) -> None: ...
    def send_password_reset_email(self, site: RequestSite, user: Any, request: Any | None = ...) -> None: ...

class EmailAuthenticationForm(AuthenticationForm):
    username: forms.EmailField
    redirect_url: forms.CharField
    host: str

    def __init__(self, host: str, *args: Any, **kwargs: Any) -> None: ...
    def clean_redirect_url(self) -> str | None: ...

class ConfirmPasswordForm(forms.Form):
    password: forms.CharField
    user: Any

    def __init__(self, user: Any, *args: Any, **kwargs: Any) -> None: ...
    def clean_password(self) -> str: ...

class EmailUserCreationForm(forms.ModelForm):
    email: forms.EmailField
    password1: forms.CharField
    password2: forms.CharField
    redirect_url: forms.CharField
    host: str | None

    class Meta:
        model: type[models.Model]
        fields: tuple[str, ...]

    def __init__(self, *args: Any, host: str | None = ..., **kwargs: Any) -> None: ...
    def _post_clean(self) -> None: ...
    def clean_email(self) -> str: ...
    def clean_password2(self) -> str: ...
    def clean_redirect_url(self) -> str: ...
    def save(self, commit: bool = ...) -> Any: ...

class OrderSearchForm(forms.Form):
    date_from: forms.DateField
    date_to: forms.DateField
    order_number: forms.CharField

    def clean(self) -> dict[str, Any]: ...
    def description(self) -> str: ...
    def _orders_description(
        self, date_from: datetime.date | None, date_to: datetime.date | None, order_number: str | None
    ) -> str | None: ...
    def get_filters(self) -> dict[str, Any]: ...

class UserForm(forms.ModelForm):
    user: Any

    class Meta:
        model: type[models.Model]
        fields: list[str]

    def __init__(self, user: Any, *args: Any, **kwargs: Any) -> None: ...
    def clean_email(self) -> str: ...

class ProductAlertForm(forms.ModelForm):
    email: forms.EmailField
    user: Any
    product: Any

    class Meta:
        model: type[models.Model]
        fields: list[str]

    def __init__(self, user: Any, product: Any, *args: Any, **kwargs: Any) -> None: ...
    def save(self, commit: bool = ...) -> Any: ...
    def clean(self) -> dict[str, Any]: ...

class AnonymousOrderForm(forms.Form):
    email: forms.EmailField

ProfileForm: type[forms.ModelForm]
