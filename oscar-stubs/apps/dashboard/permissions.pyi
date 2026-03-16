class DashboardPermission:
    permissions: dict[str, list[str]]
    staff: list[str]
    partner_dashboard_access: list[str]
    @classmethod
    def get(cls, app_label: str, *codenames: str) -> list[str]: ...
