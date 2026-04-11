"""OpenAI integration type definitions."""

from dataclasses import dataclass
from typing import Optional, TypedDict


@dataclass
class RecommendationRequest:
    """Request structure for game recommendations."""

    liked_games: Optional[list[str]] = None
    disliked_games: Optional[list[str]] = None
    preferred_genre: Optional[str] = None
    year_range: Optional[dict[str, int]] = None
    min_rating: Optional[int] = None
    recommendations_number: Optional[int] = None


class IGDBItem(TypedDict):
    """Recommended IGDB game identifier."""

    igdb_id: int


RecommendationResponse = list[IGDBItem]
