from collections.abc import Callable
from typing import Any

from django.contrib.auth.models import AbstractBaseUser, AnonymousUser

def check_permissions(
    user: AbstractBaseUser | AnonymousUser,
    permissions: list[str] | tuple[list[str], ...] | None,
) -> bool: ...
def permissions_required(
    permissions: list[str] | tuple[list[str], ...],
    login_url: str | None = ...,
) -> Callable[[Callable[..., Any]], Callable[..., Any]]: ...
def login_forbidden(
    view_func: Callable[..., Any],
    template_name: str = ...,
    status: int = ...,
) -> Callable[..., Any]: ...
