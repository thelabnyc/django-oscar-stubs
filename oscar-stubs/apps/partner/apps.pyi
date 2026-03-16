from oscar.core.application import OscarConfig

class PartnerConfig(OscarConfig):
    label: str
    name: str
    verbose_name: str

    def ready(self) -> None: ...
