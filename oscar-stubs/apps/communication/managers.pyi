from typing import Any

from django.db import models

class CommunicationTypeManager(models.Manager):
    def get_and_render(self, code: str, context: dict[str, Any]) -> dict[str, str]: ...
