from collections.abc import Iterable
from typing import IO, Any, Self
import csv
import types

from django.db import models

AUTH_USER_MODEL: str
AUTH_USER_APP_LABEL: str
AUTH_USER_MODEL_NAME: str

def get_user_model() -> type[models.Model]: ...
def existing_user_fields(fields: list[str]) -> list[str]: ...

class UnicodeCSVWriter:
    filename: str | None
    f: IO[str] | None
    dialect: type[csv.Dialect]
    encoding: str
    kw: dict[str, Any]
    writer: Any
    def __init__(
        self,
        filename: str | None = ...,
        open_file: IO[str] | None = ...,
        dialect: type[csv.Dialect] = ...,
        encoding: str = ...,
        **kw: Any,
    ) -> None: ...
    def __enter__(self) -> Self: ...
    def __exit__(
        self,
        exception_type: type[BaseException] | None,
        exception_value: BaseException | None,
        exception_traceback: types.TracebackType | None,
    ) -> None: ...
    def add_bom(self, f: IO[str]) -> None: ...
    def writerow(self, row: Iterable[Any]) -> None: ...
    def writerows(self, rows: Iterable[Iterable[Any]]) -> None: ...
