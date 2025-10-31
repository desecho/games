"""IDGB types."""

from __future__ import annotations

from datetime import date
from typing import Optional

from typing_extensions import NotRequired, TypedDict


class IGDBGameCoverRaw(TypedDict):
    """IGDB game cover raw."""

    id: int
    image_id: str


class IGDBGameRaw(TypedDict):
    """IGDB game raw."""

    id: int
    name: str
    game_type: int
    first_release_date: NotRequired[int]
    cover: NotRequired[IGDBGameCoverRaw]


class IGDBGame(TypedDict):
    """IGDB game."""

    id: int
    name: str
    category_id: int
    release_date: Optional[date]
    cover: Optional[str]
