"""Tests for IGDB integration."""

import json
from datetime import date
from unittest.mock import Mock, patch

import requests
from django.test import TestCase

from games.exceptions import IGDBError
from games.igdb.igdb import IGDB
from games.models import Category


class IGDBTest(TestCase):
    """Test IGDB integration."""

    def setUp(self):
        """Set up test data."""
        # Create required categories
        Category.objects.create(id=Category.MAIN_GAME, name="Main Game")
        Category.objects.create(id=Category.DLC, name="DLC")

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    def test_init_creates_igdb_wrapper(self, mock_wrapper, mock_session):  # pylint: disable=no-self-use
        """Test IGDB initialization creates wrapper with token."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        IGDB()

        mock_session.assert_called_once()
        mock_session_instance.fetch_token.assert_called_once()
        mock_wrapper.assert_called_once()

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    def test_process_release_date_with_timestamp(self, mock_wrapper, mock_session):
        """Test processing release date with valid timestamp through get_game."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper
        # January 1, 2020 timestamp
        mock_igdb_wrapper.api_request.return_value = json.dumps(
            [{"id": 1, "name": "Test Game", "category": 0, "first_release_date": 1577836800}]
        )

        igdb = IGDB()
        result = igdb.get_game(1)
        self.assertEqual(result["release_date"], date(2020, 1, 1))

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    def test_process_release_date_with_none(self, mock_wrapper, mock_session):
        """Test processing release date with None through get_game."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper
        mock_igdb_wrapper.api_request.return_value = json.dumps([{"id": 1, "name": "Test Game", "category": 0}])

        igdb = IGDB()
        result = igdb.get_game(1)
        self.assertIsNone(result["release_date"])

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    def test_search_games_success(self, mock_wrapper, mock_session):
        """Test successful game search."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper
        mock_igdb_wrapper.api_request.return_value = json.dumps(
            [
                {
                    "id": 1,
                    "name": "Test Game",
                    "category": 0,
                    "first_release_date": 1577836800,
                    "cover": {"image_id": "test_cover"},
                }
            ]
        )

        igdb = IGDB()
        result = igdb.search_games("test query")

        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["id"], 1)
        self.assertEqual(result[0]["name"], "Test Game")
        self.assertEqual(result[0]["category"], "Main Game")
        self.assertTrue(result[0]["isReleased"])
        self.assertIsNotNone(result[0]["cover"])

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    def test_search_games_without_cover(self, mock_wrapper, mock_session):
        """Test game search with game that has no cover."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper
        mock_igdb_wrapper.api_request.return_value = json.dumps(
            [{"id": 1, "name": "Test Game", "category": 0, "first_release_date": 1577836800}]
        )

        igdb = IGDB()
        result = igdb.search_games("test query")

        self.assertEqual(len(result), 1)
        self.assertIsNone(result[0]["cover"])

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    def test_search_games_api_error(self, mock_wrapper, mock_session):
        """Test game search with API error."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper
        mock_igdb_wrapper.api_request.side_effect = Exception("API Error")

        igdb = IGDB()

        with self.assertRaises(IGDBError):
            igdb.search_games("test query")

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    def test_get_game_success(self, mock_wrapper, mock_session):
        """Test successful get game."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper
        mock_igdb_wrapper.api_request.return_value = json.dumps(
            [
                {
                    "id": 1,
                    "name": "Test Game",
                    "category": 0,
                    "first_release_date": 1577836800,
                    "cover": {"image_id": "test_cover"},
                }
            ]
        )

        igdb = IGDB()
        result = igdb.get_game(1)

        self.assertEqual(result["id"], 1)
        self.assertEqual(result["name"], "Test Game")
        self.assertEqual(result["category_id"], Category.MAIN_GAME)
        self.assertEqual(result["release_date"], date(2020, 1, 1))
        self.assertEqual(result["cover"], "test_cover")

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    def test_get_game_without_cover(self, mock_wrapper, mock_session):
        """Test get game without cover."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper
        mock_igdb_wrapper.api_request.return_value = json.dumps(
            [{"id": 1, "name": "Test Game", "category": 0, "first_release_date": 1577836800}]
        )

        igdb = IGDB()
        result = igdb.get_game(1)

        self.assertIsNone(result["cover"])

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    @patch("time.sleep")
    def test_get_game_rate_limit_retry(self, mock_sleep, mock_wrapper, mock_session):
        """Test get game with rate limit retry."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper

        # First call raises rate limit error, second succeeds
        rate_limit_error = requests.exceptions.HTTPError()
        rate_limit_error.response = Mock()
        rate_limit_error.response.status_code = 429

        mock_igdb_wrapper.api_request.side_effect = [
            rate_limit_error,
            json.dumps([{"id": 1, "name": "Test Game", "category": 0, "first_release_date": 1577836800}]),
        ]

        igdb = IGDB()
        result = igdb.get_game(1)

        self.assertEqual(result["id"], 1)
        mock_sleep.assert_called_once_with(1)  # First retry waits 1 second

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    @patch("time.sleep")
    def test_get_game_max_retries_exceeded(self, _mock_sleep, mock_wrapper, mock_session):
        """Test get game exceeds max retries."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper

        rate_limit_error = requests.exceptions.HTTPError()
        rate_limit_error.response = Mock()
        rate_limit_error.response.status_code = 429

        mock_igdb_wrapper.api_request.side_effect = rate_limit_error

        igdb = IGDB()

        with self.assertRaises(IGDBError):
            igdb.get_game(1, max_retries=2)

    @patch("games.igdb.igdb.OAuth2Session")
    @patch("games.igdb.igdb.IGDBWrapper")
    def test_get_game_non_rate_limit_http_error(self, mock_wrapper, mock_session):
        """Test get game with non-rate-limit HTTP error."""
        mock_session_instance = Mock()
        mock_session.return_value = mock_session_instance
        mock_session_instance.fetch_token.return_value = {"access_token": "test_token"}

        mock_igdb_wrapper = Mock()
        mock_wrapper.return_value = mock_igdb_wrapper

        http_error = requests.exceptions.HTTPError()
        http_error.response = Mock()
        http_error.response.status_code = 500

        mock_igdb_wrapper.api_request.side_effect = http_error

        igdb = IGDB()

        with self.assertRaises(IGDBError):
            igdb.get_game(1)
