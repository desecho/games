"""Custom Types."""
from __future__ import annotations

from typing import Any, Dict, List, Optional, TypeAlias, Union

from django.urls import URLPattern, URLResolver
from typing_extensions import NotRequired, TypedDict


class TemplatesSettingsOptions(TypedDict):
    """Templates settings options."""

    context_processors: List[str]
    # loaders: List[str | Tuple[str, List[str]]]
    # builtins: List[str]


class TemplatesSettings(TypedDict):
    """Templates settings."""

    NAME: str
    BACKEND: str
    DIRS: NotRequired[List[str]]
    OPTIONS: NotRequired[TemplatesSettingsOptions]
    APP_DIRS: NotRequired[Optional[bool]]


class GameObject(TypedDict):
    """Game object."""

    name: str
    cover: Optional[str]
    category: str


class RecordObject(TypedDict):
    """Record object."""

    id: int
    game: GameObject
    listKey: str
    order: int


UntypedObject: TypeAlias = Dict[str, Any]
URL: TypeAlias = Union[URLPattern, URLResolver]
