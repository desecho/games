"""Common views."""
from typing import Any

from rest_framework.views import APIView

from ..igdb import IGDB


class IGDBAPIView(APIView):
    """IGDB API view."""

    igdb: IGDB

    def __init__(self, **kwargs: Any) -> None:
        """Init."""
        self.igdb = IGDB()
        super().__init__(**kwargs)
