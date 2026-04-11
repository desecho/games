"""AI Recommendations view."""

from datetime import datetime
from http import HTTPStatus
from typing import Optional, cast

from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView
from sentry_sdk import capture_exception

from ..exceptions import IGDBError
from ..igdb import IGDB
from ..models import Record, User
from ..openai.client import MIN_YEAR, OpenAIClient
from ..openai.exceptions import OpenAIError
from ..openai.types import RecommendationRequest, RecommendationResponse
from ..types import GameObject


class RecommendationsView(APIView):
    """AI Recommendations view."""

    permission_classes = [IsAuthenticated]

    @staticmethod
    def _parse_year_range(year_start: Optional[str], year_end: Optional[str]) -> Optional[dict[str, int]]:
        """Parse year range parameters."""
        if not year_start or not year_end:
            return None
        try:
            parsed_year_range = {"start": int(year_start), "end": int(year_end)}
        except ValueError as exc:
            raise ValueError("Invalid year range values") from exc

        if parsed_year_range["start"] > parsed_year_range["end"]:
            raise ValueError("Start year cannot be greater than end year")
        current_year = datetime.now().year
        if parsed_year_range["start"] < MIN_YEAR or parsed_year_range["end"] > current_year:
            raise ValueError(f"Year range must be between {MIN_YEAR} and {current_year}")
        return parsed_year_range

    @staticmethod
    def _parse_min_rating(min_rating: Optional[str]) -> Optional[int]:
        """Parse minimum rating parameter."""
        if min_rating is None:
            return None
        try:
            min_rating_int = int(min_rating)
        except ValueError as exc:
            raise ValueError("Invalid minimum rating value") from exc

        if not settings.AI_MIN_RATING <= min_rating_int <= settings.AI_MAX_RATING:
            raise ValueError(f"Minimum rating must be between {settings.AI_MIN_RATING} and {settings.AI_MAX_RATING}")
        return min_rating_int

    @staticmethod
    def _parse_recommendations_number(recommendations_number: Optional[str]) -> Optional[int]:
        """Parse recommendations number parameter."""
        if recommendations_number is None:
            return None
        try:
            recommendations_number_int = int(recommendations_number)
        except ValueError as exc:
            raise ValueError("Invalid recommendations number value") from exc

        min_recommendations = settings.AI_MIN_RECOMMENDATIONS
        max_recommendations = settings.AI_MAX_RECOMMENDATIONS
        if not min_recommendations <= recommendations_number_int <= max_recommendations:
            raise ValueError(
                f"Number of recommendations must be between {min_recommendations} and {max_recommendations}"
            )
        return recommendations_number_int

    @staticmethod
    def _parse_preferred_genre(preferred_genre: Optional[str]) -> Optional[str]:
        """Parse preferred genre parameter."""
        if not preferred_genre:
            return None
        if preferred_genre not in settings.GAME_GENRES:
            raise ValueError(
                f"Preferred genre '{preferred_genre}' is not valid. "
                f"Valid genres are: {', '.join(settings.GAME_GENRES)}"
            )
        return preferred_genre

    @staticmethod
    def _get_user_game_preferences(user: User) -> tuple[list[str], list[str]]:
        """Get user's liked and disliked games based on ratings."""
        liked_records = user.records.filter(rating__gte=3).select_related("game")
        liked_games = [record.game.name for record in liked_records]

        disliked_records = user.records.filter(rating__lte=2, rating__gt=0).select_related("game")
        disliked_games = [record.game.name for record in disliked_records]

        return liked_games, disliked_games

    @staticmethod
    def _convert_recommendations_to_games(recommendations: RecommendationResponse, igdb: IGDB) -> list[GameObject]:
        """Convert IGDB ID recommendations to game results."""
        game_ids = []
        for recommendation in recommendations:
            try:
                game_ids.append(recommendation["igdb_id"])
            except (KeyError, TypeError) as exc:
                capture_exception(exc)
                continue

        try:
            return igdb.get_games(game_ids)
        except IGDBError as exc:
            capture_exception(exc)
            return []

    @staticmethod
    def _filter_out_users_games(games: list[GameObject], user: User) -> None:
        """Filter out games the user already has in any list."""
        user_games_ids = set(Record.objects.filter(user=user).values_list("game_id", flat=True))
        for game in list(games):
            if game["id"] in user_games_ids:
                games.remove(game)

    def get(self, request: Request) -> Response:
        """Return AI-generated game recommendations based on user preferences."""
        try:
            try:
                preferred_genre = self._parse_preferred_genre(request.GET.get("preferredGenre"))
                year_range = self._parse_year_range(request.GET.get("yearStart"), request.GET.get("yearEnd"))
                min_rating = self._parse_min_rating(request.GET.get("minRating"))
                recommendations_number = self._parse_recommendations_number(request.GET.get("recommendationsNumber"))
            except ValueError as exc:
                return Response({"error": str(exc)}, status=HTTPStatus.BAD_REQUEST)

            user = cast(User, request.user)
            liked_games, disliked_games = self._get_user_game_preferences(user)
            recommendation_request = RecommendationRequest(
                liked_games=liked_games or None,
                disliked_games=disliked_games or None,
                preferred_genre=preferred_genre,
                year_range=year_range,
                min_rating=min_rating,
                recommendations_number=recommendations_number or settings.AI_MAX_RECOMMENDATIONS,
            )

            try:
                openai_client = OpenAIClient()
                recommendations = openai_client.get_game_recommendations(recommendation_request)
            except OpenAIError as exc:
                capture_exception(exc)
                return Response(
                    {"error": "Failed to get AI recommendations. Please try again later."},
                    status=HTTPStatus.INTERNAL_SERVER_ERROR,
                )

            games = self._convert_recommendations_to_games(recommendations, IGDB())
            self._filter_out_users_games(games, user)
            return Response(games)

        except (AttributeError, TypeError, KeyError) as exc:
            capture_exception(exc)
            return Response({"error": "An unexpected error occurred"}, status=HTTPStatus.INTERNAL_SERVER_ERROR)
