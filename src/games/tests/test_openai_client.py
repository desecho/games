"""Tests for OpenAI client functionality."""

from datetime import datetime
from unittest.mock import Mock, patch

from django.conf import settings
from django.test import TestCase, override_settings

from games.openai.client import OpenAIClient
from games.openai.exceptions import OpenAIConfigurationError, OpenAIError
from games.openai.types import RecommendationRequest


class OpenAIClientInitializationTestCase(TestCase):
    """Test cases for OpenAI client initialization."""

    @override_settings(OPENAI_API_KEY=None)
    def test_init_without_api_key_raises_configuration_error(self):
        """Test that initializing without API key raises OpenAIConfigurationError."""
        with self.assertRaises(OpenAIConfigurationError) as context:
            OpenAIClient()

        self.assertEqual(str(context.exception), "OPENAI_API_KEY is not configured in settings")

    @override_settings(OPENAI_API_KEY="test-api-key", OPENAI_MODEL="gpt-4")
    @patch("games.openai.client.OpenAI")
    def test_init_with_valid_api_key_creates_client(self, mock_openai):
        """Test that initializing with valid API key creates OpenAI client."""
        mock_client_instance = Mock()
        mock_openai.return_value = mock_client_instance

        client = OpenAIClient()

        mock_openai.assert_called_once_with(api_key="test-api-key")
        self.assertEqual(client.client, mock_client_instance)
        self.assertEqual(client.model, "gpt-4")


class OpenAIClientValidationTestCase(TestCase):
    """Test cases for OpenAI client validation methods."""

    @override_settings(AI_MIN_RECOMMENDATIONS=1, AI_MAX_RECOMMENDATIONS=10)
    def test_validate_recommendations_number(self):
        """Test validation of recommendations number."""
        OpenAIClient._validate_recommendations_number(1)
        OpenAIClient._validate_recommendations_number(10)
        OpenAIClient._validate_recommendations_number(None)

        with self.assertRaises(ValueError) as context:
            OpenAIClient._validate_recommendations_number(0)
        self.assertIn("Number of recommendations must be between 1 and 10", str(context.exception))

    @override_settings(AI_MIN_RATING=0, AI_MAX_RATING=5)
    def test_validate_rating(self):
        """Test validation of ratings."""
        OpenAIClient._validate_rating(0)
        OpenAIClient._validate_rating(5)
        OpenAIClient._validate_rating(None)

        with self.assertRaises(ValueError) as context:
            OpenAIClient._validate_rating(6)
        self.assertIn("Minimum rating must be between 0 and 5", str(context.exception))

    @override_settings(AI_MAX_GAME_TITLE_LENGTH=10)
    def test_validate_game_list(self):
        """Test validation of game title lists."""
        OpenAIClient._validate_game_list(["Game 1"], "liked")
        OpenAIClient._validate_game_list([], "liked")
        OpenAIClient._validate_game_list(None, "liked")

        with self.assertRaises(ValueError) as context:
            OpenAIClient._validate_game_list([""], "disliked")
        self.assertEqual(str(context.exception), "Disliked game titles cannot be empty")

        with self.assertRaises(ValueError) as context:
            OpenAIClient._validate_game_list(["A" * 11], "liked")
        self.assertIn("exceeds maximum length of 10 characters", str(context.exception))

    @override_settings(GAME_GENRES=["Action", "Strategy"])
    def test_validate_genre(self):
        """Test validation of game genres."""
        OpenAIClient._validate_genre("Action")
        OpenAIClient._validate_genre(None)

        with self.assertRaises(ValueError) as context:
            OpenAIClient._validate_genre("Unknown")
        self.assertEqual(
            str(context.exception),
            "Preferred genre 'Unknown' is not valid. Valid genres are: Action, Strategy",
        )

    def test_validate_year_range(self):
        """Test validation of year ranges."""
        current_year = datetime.now().year
        OpenAIClient._validate_year_range({"start": 1971, "end": current_year})
        OpenAIClient._validate_year_range(None)

        with self.assertRaises(ValueError) as context:
            OpenAIClient._validate_year_range({"start": 2020, "end": 2010})
        self.assertEqual(str(context.exception), "Start year cannot be greater than end year")

        with self.assertRaises(ValueError) as context:
            OpenAIClient._validate_year_range({"start": 1970, "end": current_year})
        self.assertEqual(str(context.exception), f"Year range must be between 1971 and {current_year}")


class OpenAIClientPromptTestCase(TestCase):
    """Test cases for prompt building."""

    def test_build_recommendation_prompt_empty_preferences(self):
        """Test building prompt with empty preferences."""
        preferences = RecommendationRequest()
        prompt = OpenAIClient._build_recommendation_prompt(preferences)

        expected_lines = [
            "Recommend games based on the following user preferences:",
            f"Number of recommendations: {settings.AI_MAX_RECOMMENDATIONS}",
        ]
        self.assertEqual(prompt, "\n\n".join(expected_lines))

    def test_build_recommendation_prompt_comprehensive(self):
        """Test building prompt with all preferences."""
        preferences = RecommendationRequest(
            liked_games=["Game A"],
            disliked_games=["Game B"],
            preferred_genre="Action",
            year_range={"start": 2000, "end": 2020},
            min_rating=4,
            recommendations_number=7,
        )
        prompt = OpenAIClient._build_recommendation_prompt(preferences)

        self.assertIn("Games they liked: Game A", prompt)
        self.assertIn("Games they disliked: Game B", prompt)
        self.assertIn("Preferred genre: Action", prompt)
        self.assertIn("Preferred year range: 2000-2020", prompt)
        self.assertIn("Minimum rating: 80/100", prompt)
        self.assertIn("Number of recommendations: 7", prompt)


class OpenAIClientResponseTestCase(TestCase):
    """Test cases for parsing OpenAI responses."""

    def test_parse_recommendation_response_valid(self):
        """Test parsing valid recommendation response."""
        result = OpenAIClient._parse_recommendation_response('[{"igdb_id": 1020}]')
        self.assertEqual(result, [{"igdb_id": 1020}])

    def test_parse_recommendation_response_invalid_json(self):
        """Test parsing invalid JSON response."""
        with self.assertRaises(ValueError) as context:
            OpenAIClient._parse_recommendation_response("not json")
        self.assertIn("Invalid JSON response from OpenAI", str(context.exception))

    def test_parse_recommendation_response_missing_id(self):
        """Test parsing response with missing IGDB ID."""
        with self.assertRaises(ValueError) as context:
            OpenAIClient._parse_recommendation_response('[{"title": "Game"}]')
        self.assertEqual(str(context.exception), "Each recommendation must have an 'igdb_id' field")

    def test_parse_recommendation_response_non_integer_id(self):
        """Test parsing response with invalid IGDB ID type."""
        with self.assertRaises(ValueError) as context:
            OpenAIClient._parse_recommendation_response('[{"igdb_id": "1020"}]')
        self.assertEqual(str(context.exception), "Each recommendation 'igdb_id' must be an integer")

    def test_filter_out_duplicated_ids(self):
        """Test duplicate IGDB IDs are filtered in place."""
        recommendations = [{"igdb_id": 1}, {"igdb_id": 2}, {"igdb_id": 1}]
        OpenAIClient._filter_out_duplicated_ids(recommendations)
        self.assertEqual(recommendations, [{"igdb_id": 1}, {"igdb_id": 2}])


class OpenAIClientFlowTestCase(TestCase):
    """Test full OpenAI recommendation flow."""

    @override_settings(OPENAI_API_KEY="test-api-key", OPENAI_MODEL="gpt-4", OPENAI_MAX_TOKENS=1000)
    @patch("games.openai.client.OpenAI")
    def test_get_game_recommendations_success(self, mock_openai):
        """Test successful game recommendations flow."""
        mock_client_instance = Mock()
        mock_openai.return_value = mock_client_instance

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = '[{"igdb_id": 1}, {"igdb_id": 1}, {"igdb_id": 2}]'
        mock_client_instance.chat.completions.create.return_value = mock_response

        client = OpenAIClient()
        result = client.get_game_recommendations(RecommendationRequest(liked_games=["Game A"]))

        self.assertEqual(result, [{"igdb_id": 1}, {"igdb_id": 2}])
        mock_client_instance.chat.completions.create.assert_called_once()
        call_kwargs = mock_client_instance.chat.completions.create.call_args.kwargs
        self.assertEqual(call_kwargs["model"], "gpt-4")
        self.assertEqual(call_kwargs["max_completion_tokens"], 1000)

    @override_settings(OPENAI_API_KEY="test-api-key")
    @patch("games.openai.client.OpenAI")
    def test_get_game_recommendations_empty_content(self, mock_openai):
        """Test empty OpenAI content raises OpenAIError."""
        mock_client_instance = Mock()
        mock_openai.return_value = mock_client_instance

        mock_response = Mock()
        mock_response.choices = [Mock()]
        mock_response.choices[0].message.content = None
        mock_client_instance.chat.completions.create.return_value = mock_response

        client = OpenAIClient()

        with self.assertRaises(OpenAIError) as context:
            client.get_game_recommendations(RecommendationRequest())

        self.assertIn("OpenAI API returned empty content", str(context.exception))
