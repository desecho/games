"""Search views."""
from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.response import Response

from ..igdb import IGDBGamesSearchResult
from ..models import User
from .common import IGDBAPIView


class SearchView(IGDBAPIView):
    """Search view."""

    permission_classes: list[str] = []  # type: ignore

    def _filter_out_users_games(self, results: list[IGDBGamesSearchResult]) -> None:
        """Filter out users games."""
        user: User = self.request.user  # type: ignore
        user_games_ids = user.records.values_list("game__id", flat=True)
        for result in list(results):
            if result["id"] in user_games_ids:
                results.remove(result)

    def get(self, request: Request) -> Response:
        """Search games."""
        try:
            query = request.GET["query"]
        except KeyError:
            return Response(status=HTTPStatus.BAD_REQUEST)
        results = self.igdb.search_games(query)
        if request.user.is_authenticated:
            self._filter_out_users_games(results)
        return Response(results)
