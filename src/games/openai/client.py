"""OpenAI client for game recommendations."""

import json
import logging
from datetime import datetime
from typing import Any, Optional, cast

from django.conf import settings
from openai import OpenAI

from .exceptions import OpenAIConfigurationError, OpenAIError
from .types import IGDBItem, RecommendationRequest, RecommendationResponse

logger = logging.getLogger(__name__)

SYSTEM_PROMPT = """You are a video game recommendation expert.

Provide personalized game recommendations based on the user's preferences and game history. Output only a plain JSON array of objects with the following structure, without markdown or extra explanation:

[
    {
        "igdb_id": 123
    }
]

The list should contain ONLY IGDB IDs of recommended games, NOT titles. Each game should be relevant to the user's preferences, avoiding duplicates and ensuring variety in genre and style.
The list should contain games only. Movies, TV shows, board games, and non-game media should not be included.

Recommendation logic:
- If the user has no specific preferences, recommend popular and critically acclaimed games.
- Avoid recommending games the user already likes or dislikes.
- Use disliked and liked games to refine suggestions.
- If a minimum rating is specified, all recommendations must meet or exceed it.
- If a preferred year range is given, restrict recommendations to that range.
- If preferred genres are specified, prioritize them.
- If the user requests a specific number of games, return exactly that many.
- If genre is not specified, ensure diversity in genre and style.
- Prefer notable PC games when there is a choice between platforms.
- Always aim to match user preferences while introducing some variety.

IMPORTANT: Do NOT ask any questions or seek clarification. Give the results to your best ability. If there are no suitable recommendations, return at least something - you can relax user's preferences in this case.
"""

MIN_YEAR = 1971


class OpenAIClient:
    """Client for OpenAI API interactions."""

    def __init__(self) -> None:
        """Initialize OpenAI client with API key from settings."""
        if not settings.OPENAI_API_KEY:
            raise OpenAIConfigurationError("OPENAI_API_KEY is not configured in settings")

        self.client = OpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL

    def get_game_recommendations(self, user_preferences: RecommendationRequest) -> RecommendationResponse:
        """
        Get game recommendations based on user preferences.

        Raises
        ------
        OpenAIError
            If validation or the API call fails.

        """
        logger.info("Starting game recommendation request")
        logger.debug("User preferences: %s", user_preferences)
        try:
            OpenAIClient._validate_user_preferences(user_preferences)
            prompt = OpenAIClient._build_recommendation_prompt(user_preferences)

            logger.info("Calling OpenAI API with model: %s", self.model)
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "system", "content": SYSTEM_PROMPT}, {"role": "user", "content": prompt}],
                max_completion_tokens=settings.OPENAI_MAX_TOKENS,
            )
            logger.info("OpenAI API call completed successfully")

            content = response.choices[0].message.content
            if content is None:
                raise OpenAIError("OpenAI API returned empty content")

            parsed_content = OpenAIClient._parse_recommendation_response(content)
            OpenAIClient._filter_out_duplicated_ids(parsed_content)
            logger.info("Successfully generated %d game recommendations", len(parsed_content))
            return parsed_content

        except Exception as exc:
            logger.error("Error during game recommendation: %s", str(exc), exc_info=True)
            if hasattr(exc, "__module__") and "openai" in exc.__module__:
                raise OpenAIError(f"OpenAI API error: {str(exc)}") from exc
            raise OpenAIError(f"Unexpected error: {str(exc)}") from exc

    @staticmethod
    def _convert_rating(rating: int) -> int:
        """Convert a 5-star rating to a 100-point rating."""
        return rating * 20

    @staticmethod
    def _validate_user_preferences(preferences: RecommendationRequest) -> None:
        """Validate user preferences against settings constraints."""
        OpenAIClient._validate_recommendations_number(preferences.recommendations_number)
        OpenAIClient._validate_rating(preferences.min_rating)
        OpenAIClient._validate_game_list(preferences.liked_games, "liked")
        OpenAIClient._validate_game_list(preferences.disliked_games, "disliked")
        OpenAIClient._validate_genre(preferences.preferred_genre)
        OpenAIClient._validate_year_range(preferences.year_range)

    @staticmethod
    def _validate_recommendations_number(recommendations_number: Optional[int]) -> None:
        """Validate recommendations number."""
        if recommendations_number is None:
            return
        if not settings.AI_MIN_RECOMMENDATIONS <= recommendations_number <= settings.AI_MAX_RECOMMENDATIONS:
            raise ValueError(
                f"Number of recommendations must be between {settings.AI_MIN_RECOMMENDATIONS} "
                f"and {settings.AI_MAX_RECOMMENDATIONS}"
            )

    @staticmethod
    def _validate_rating(min_rating: Optional[int]) -> None:
        """Validate rating."""
        if min_rating is None:
            return
        if not settings.AI_MIN_RATING <= min_rating <= settings.AI_MAX_RATING:
            raise ValueError(f"Minimum rating must be between {settings.AI_MIN_RATING} and {settings.AI_MAX_RATING}")

    @staticmethod
    def _validate_game_list(games: Optional[list[str]], game_type: str) -> None:
        """Validate game list."""
        if games is None:
            return
        for game in games:
            if not isinstance(game, str):
                raise ValueError(f"All {game_type} games must be strings")
            if len(game.strip()) == 0:
                raise ValueError(f"{game_type.capitalize()} game titles cannot be empty")
            if len(game) > settings.AI_MAX_GAME_TITLE_LENGTH:
                raise ValueError(
                    f"{game_type.capitalize()} game title '{game[:50]}...' exceeds maximum length of "
                    f"{settings.AI_MAX_GAME_TITLE_LENGTH} characters"
                )

    @staticmethod
    def _validate_genre(preferred_genre: Optional[str]) -> None:
        """Validate preferred genre."""
        if preferred_genre is None:
            return
        if preferred_genre not in settings.GAME_GENRES:
            raise ValueError(
                f"Preferred genre '{preferred_genre}' is not valid. "
                f"Valid genres are: {', '.join(settings.GAME_GENRES)}"
            )

    @staticmethod
    def _validate_year_range(year_range: Optional[dict[str, int]]) -> None:
        """Validate year range."""
        if year_range is None:
            return
        if not isinstance(year_range, dict):
            raise ValueError("Year range must be a dictionary with 'start' and 'end' keys")
        if "start" not in year_range or "end" not in year_range:
            raise ValueError("Year range must contain both 'start' and 'end' keys")

        start_year = year_range["start"]
        end_year = year_range["end"]
        if not isinstance(start_year, int) or not isinstance(end_year, int):
            raise ValueError("Year range values must be integers")
        if start_year > end_year:
            raise ValueError("Start year cannot be greater than end year")

        current_year = datetime.now().year
        if start_year < MIN_YEAR or end_year > current_year:
            raise ValueError(f"Year range must be between {MIN_YEAR} and {current_year}")

    @staticmethod
    def _build_recommendation_prompt(preferences: RecommendationRequest) -> str:
        """Build the prompt for game recommendations."""
        prompt_parts = ["Recommend games based on the following user preferences:"]

        if preferences.liked_games:
            prompt_parts.append(f"Games they liked: {', '.join(preferences.liked_games)}")

        if preferences.disliked_games:
            prompt_parts.append(f"Games they disliked: {', '.join(preferences.disliked_games)}")

        if preferences.preferred_genre:
            prompt_parts.append(f"Preferred genre: {preferences.preferred_genre}")

        if preferences.year_range:
            prompt_parts.append(
                f"Preferred year range: {preferences.year_range['start']}-{preferences.year_range['end']}"
            )

        if preferences.min_rating is not None:
            min_rating = OpenAIClient._convert_rating(preferences.min_rating)
            prompt_parts.append(f"Minimum rating: {min_rating}/100")

        if preferences.recommendations_number:
            prompt_parts.append(f"Number of recommendations: {preferences.recommendations_number}")
        else:
            prompt_parts.append(f"Number of recommendations: {settings.AI_MAX_RECOMMENDATIONS}")

        return "\n\n".join(prompt_parts)

    @staticmethod
    def _parse_recommendation_response(content: str) -> RecommendationResponse:
        """Parse the OpenAI response into structured data."""
        try:
            parsed_data: Any = json.loads(content.strip())
            if not isinstance(parsed_data, list):
                raise ValueError("Expected a list of recommendations")

            recommendations: RecommendationResponse = []
            for item in parsed_data:
                if not isinstance(item, dict) or "igdb_id" not in item:
                    raise ValueError("Each recommendation must have an 'igdb_id' field")
                igdb_id = item["igdb_id"]
                if isinstance(igdb_id, bool) or not isinstance(igdb_id, int):
                    raise ValueError("Each recommendation 'igdb_id' must be an integer")
                recommendations.append(cast(IGDBItem, {"igdb_id": igdb_id}))

            return recommendations
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON response from OpenAI: {str(exc)}") from exc

    @staticmethod
    def _filter_out_duplicated_ids(recommendations: RecommendationResponse) -> None:
        """Remove duplicate IGDB IDs from recommendations list in-place."""
        seen_ids = set()
        filtered_recommendations: RecommendationResponse = []

        for item in recommendations:
            igdb_id = item.get("igdb_id")
            if igdb_id and igdb_id not in seen_ids:
                seen_ids.add(igdb_id)
                filtered_recommendations.append(item)

        recommendations.clear()
        recommendations.extend(filtered_recommendations)
