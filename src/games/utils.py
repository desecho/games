"""Utils."""
from datetime import date
from typing import Optional

from django.conf import settings


def get_cover_url(img_id: str) -> str:
    """Get cover URL."""
    return f"{settings.IGDB_COVER_BASE_URL}{img_id}.jpg"


def is_game_released(release_date: Optional[date]) -> bool:
    """Return whether game is released."""
    return release_date is not None and release_date <= date.today()
