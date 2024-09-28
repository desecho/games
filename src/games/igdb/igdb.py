"""IGDB."""

import json
from datetime import date, datetime
from typing import Optional

from authlib.integrations.requests_client import OAuth2Session
from django.conf import settings
from igdb.wrapper import IGDBWrapper

from ..exceptions import IGDBError
from ..models import Category
from ..types import GameObject
from ..utils import get_cover_url, is_game_released
from .types import IGDBGame, IGDBGameRaw

# Full list is available here: https://api-docs.igdb.com/#game-enums
CATEGORY_MAIN_GAME = 0
CATEGORY_DLC = 1
CATEGORY_EXPANSION = 2
CATEGORY_STANDALONE_EXPANSION = 4
CATEGORY_REMAKE = 8
CATEGORY_REMASTER = 9

GAME_CATEGORIES_SUPPORTED = (
    CATEGORY_MAIN_GAME,
    CATEGORY_DLC,
    CATEGORY_EXPANSION,
    CATEGORY_STANDALONE_EXPANSION,
    CATEGORY_REMAKE,
    CATEGORY_REMASTER,
)

GAME_CATEGORIES = {
    CATEGORY_MAIN_GAME: "Main Game",
    CATEGORY_DLC: "DLC",
    CATEGORY_EXPANSION: "Expansion",
    CATEGORY_STANDALONE_EXPANSION: "Standalone Expansion",
    CATEGORY_REMAKE: "Remake",
    CATEGORY_REMASTER: "Remaster",
}

# We have to use a mapping here because CATEGORY_MAIN_GAME is 0 which is not supported by Django as a primary key.
GAME_CATEGORIES_MAPPING = {
    CATEGORY_MAIN_GAME: Category.MAIN_GAME,
    CATEGORY_DLC: Category.DLC,
    CATEGORY_EXPANSION: Category.EXPANSION,
    CATEGORY_STANDALONE_EXPANSION: Category.STANDALONE_EXPANSION,
    CATEGORY_REMAKE: Category.REMAKE,
    CATEGORY_REMASTER: Category.REMASTER,
}

PLATFORM_PC_WINDOWS = 6
PLATFORM_PC_DOS = 13

PLATFORMS_SUPPORTED = (
    PLATFORM_PC_WINDOWS,
    PLATFORM_PC_DOS,
)


class IGDB:
    """IGDB."""

    igdb: IGDBWrapper

    def __init__(self) -> None:
        """Init."""
        session = OAuth2Session(  # nosec B106
            settings.IGDB_CLIENT_ID,
            settings.IGDB_CLIENT_SECRET,
            token_endpoint=settings.IGDB_TOKEN_ENDPOINT,
            grant_type="client_credentials",
            token_endpoint_auth_method="client_secret_post",
        )
        token = session.fetch_token()["access_token"]
        self.igdb = IGDBWrapper(settings.IGDB_CLIENT_ID, token)

    @staticmethod
    def _process_release_date(release_date: Optional[int]) -> Optional[date]:
        """Process release date."""
        if release_date is None:
            return None
        return datetime.fromtimestamp(release_date).date()

    def _process_search_games_results(self, results: list[IGDBGameRaw]) -> list[GameObject]:
        """Process search games results."""
        results_processed: list[GameObject] = []
        for result in results:
            release_date = self._process_release_date(result.get("first_release_date"))
            result_processed: GameObject = {
                "id": result["id"],
                "name": result["name"],
                "category": GAME_CATEGORIES[result["category"]],
                "isReleased": is_game_released(release_date),
                "cover": get_cover_url(result["cover"]["image_id"]) if "cover" in result else None,
            }
            results_processed.append(result_processed)
        return results_processed

    def search_games(self, query: str) -> list[GameObject]:
        """Search games."""
        request = f"""
            fields name, cover.image_id, first_release_date, category;
            search "{query}";
            where version_parent = null &
                platforms = {PLATFORMS_SUPPORTED} &
                category = {GAME_CATEGORIES_SUPPORTED};
            limit {settings.MAX_RESULTS};
        """
        try:
            response = self.igdb.api_request("games", request)
        except Exception as exc:
            raise IGDBError from exc
        results: list[IGDBGameRaw] = json.loads(response)
        return self._process_search_games_results(results)

    def _process_game(self, game: IGDBGameRaw) -> IGDBGame:
        """Process game."""
        return {
            "id": game["id"],
            "name": game["name"],
            "category_id": GAME_CATEGORIES_MAPPING[game["category"]],
            "release_date": self._process_release_date(game.get("first_release_date")),
            "cover": game["cover"]["image_id"] if "cover" in game else None,
        }

    def get_game(self, game_id: int) -> IGDBGame:
        """Get game."""
        request = f"""
            fields name, cover.image_id, first_release_date, category;
            where id = {game_id};
        """
        try:
            response = self.igdb.api_request("games", request)
        except Exception as exc:
            raise IGDBError from exc
        result: IGDBGameRaw = json.loads(response)[0]
        return self._process_game(result)
