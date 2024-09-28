"""Custom Types."""

from __future__ import annotations

from typing import Any, Optional, TypeAlias

from django.urls import URLPattern, URLResolver
from typing_extensions import NotRequired, TypedDict


class TemplatesSettingsOptions(TypedDict):
    """Templates settings options."""

    context_processors: list[str]
    # loaders: list[str | Tuple[str, list[str]]]
    # builtins: list[str]


class TemplatesSettings(TypedDict):
    """Templates settings."""

    NAME: str
    BACKEND: str
    DIRS: NotRequired[list[str]]
    OPTIONS: NotRequired[TemplatesSettingsOptions]
    APP_DIRS: NotRequired[Optional[bool]]


class GameObject(TypedDict):
    """Game object."""

    id: int
    name: str
    cover: Optional[str]
    category: str
    isReleased: bool


class RecordObject(TypedDict):
    """Record object."""

    id: int
    game: GameObject
    listKey: str
    order: int


class UserPreferences(TypedDict):
    """User preferences."""

    hidden: bool


UntypedObject: TypeAlias = dict[str, Any]
URL: TypeAlias = URLPattern | URLResolver
