"""Utils."""
from django.conf import settings


def get_cover_url(img_id: str) -> str:
    """Get cover URL."""
    return f"{settings.IGDB_COVER_BASE_URL}{img_id}.jpg"
