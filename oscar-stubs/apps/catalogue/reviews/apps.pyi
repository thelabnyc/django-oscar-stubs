from django.urls import URLPattern, URLResolver
from oscar.core.application import OscarConfig

class CatalogueReviewsConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str
    hidable_feature_name: str
    detail_view: type
    create_view: type
    vote_view: type
    list_view: type
    def ready(self) -> None: ...
    def get_urls(self) -> list[URLPattern | URLResolver]: ...
