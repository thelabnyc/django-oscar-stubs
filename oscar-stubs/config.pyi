from django.apps import AppConfig
from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarConfig

class Shop(OscarConfig):
    name: str
    catalogue_app: AppConfig
    customer_app: AppConfig
    basket_app: AppConfig
    checkout_app: AppConfig
    search_app: AppConfig
    dashboard_app: AppConfig
    offer_app: AppConfig
    wishlists_app: AppConfig
    password_reset_form: type
    set_password_form: type
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
