from typing import Any

class Node:
    label: str
    icon: str | None
    url_name: str | None
    url_args: Any
    url_kwargs: Any
    access_fn: Any
    children: list[Node]

    def __init__(
        self,
        label: str,
        url_name: str | None = ...,
        url_args: Any = ...,
        url_kwargs: Any = ...,
        access_fn: Any = ...,
        icon: str | None = ...,
    ) -> None: ...
    @property
    def is_heading(self) -> bool: ...
    @property
    def url(self) -> str: ...
    def add_child(self, node: Node) -> None: ...
    def is_visible(self, user: Any) -> bool: ...
    def filter(self, user: Any) -> Node | None: ...
    def has_children(self) -> bool: ...

def default_access_fn(
    user: Any,
    url_name: str | None,
    url_args: Any = ...,
    url_kwargs: Any = ...,
) -> bool: ...
