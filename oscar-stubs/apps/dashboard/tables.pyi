from django_tables2 import Table

class DashboardTable(Table):
    caption: str
    def get_caption_display(self) -> str: ...

    class Meta:
        template_name: str
        attrs: dict[str, str]
