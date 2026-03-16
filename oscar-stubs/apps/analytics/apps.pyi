from oscar.core.application import OscarConfig

class AnalyticsConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str
    def ready(self) -> None: ...
