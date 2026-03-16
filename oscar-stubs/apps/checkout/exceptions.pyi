class FailedPreCondition(Exception):
    url: str
    messages: list[str]
    def __init__(
        self,
        url: str,
        message: str | None = ...,
        messages: list[str] | None = ...,
    ) -> None: ...

class PassedSkipCondition(Exception):
    url: str
    def __init__(self, url: str) -> None: ...
