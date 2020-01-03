from typing import AnyStr, Iterable, Optional, Type
from enum import Enum


BUNDLED_EXECUTABLE: Optional[str]


class LayoutStyle(Enum)...


class InfoStyle(Enum)...


def iterfzf(
    iterable: Iterable[AnyStr], *,
    # Search mode:
    extended: bool = ...,
    exact: bool = ...,
    case_sensitive: Optional[bool] = ...,
    # Interface:
    multi: bool = ...,
    mouse: bool = ...,
    print_query: bool = ...,
    cycle: bool = ...,
    header: Optional[str] = ...,
    # Layout:
    prompt: str = ...,
    preview: Optional[str] = ...,
    border: bool = ...,
    info: Optional[Type(InfoStyle)] = ...,
    margin: Optional[str] = ...,
    layout: Optional[Type(LayoutStyle)] = ...,
    # Misc:
    query: str = ...,
    encoding: Optional[str] = ...,
    executable: str = ...,
) -> Iterable[AnyStr]: ...
