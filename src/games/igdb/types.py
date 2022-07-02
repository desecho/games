"""IDGB types."""
from __future__ import annotations

from datetime import datetime
from typing import Optional

from typing_extensions import NotRequired, TypedDict


class IGDBGameCoverRaw(TypedDict):
    """IGDB game cover raw."""

    id: int
    image_id: str


class IGDBGamesSearchResultRaw(TypedDict):
    """IGDB games search result raw."""

    id: int
    name: str
    category: int
    cover: NotRequired[IGDBGameCoverRaw]


class IGDBGamesSearchResult(TypedDict):
    """IGDB games search result."""

    id: int
    name: str
    category: str
    cover: NotRequired[str]


class IGDBGameRaw(TypedDict):
    """IGDB game raw."""

    id: int
    name: str
    category: int
    first_release_date: NotRequired[int]
    cover: NotRequired[IGDBGameCoverRaw]


class IGDBGame(TypedDict):
    """IGDB game."""

    id: int
    name: str
    category_id: int
    release_date: Optional[datetime]
    cover: Optional[str]
