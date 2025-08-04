"""Tests for games app."""

from datetime import date, timedelta

from django.test import TestCase

from games.models import Category, Game, List, Record, User


class UserModelTest(TestCase):
    """Test User model."""

    def test_user_str_representation(self):
        """Test user string representation."""
        user = User.objects.create_user(username="testuser", email="test@example.com")
        self.assertEqual(str(user), "testuser")

    def test_user_preferences_default(self):
        """Test user preferences default values."""
        user = User.objects.create_user(username="testuser", email="test@example.com")
        self.assertEqual(user.preferences, {"hidden": False})

    def test_user_preferences_hidden_true(self):
        """Test user preferences when hidden is True."""
        user = User.objects.create_user(username="testuser", email="test@example.com", hidden=True)
        self.assertEqual(user.preferences, {"hidden": True})


class CategoryModelTest(TestCase):
    """Test Category model."""

    def test_category_str_representation(self):
        """Test category string representation."""
        category = Category.objects.create(name="Main Game")
        self.assertEqual(str(category), "Main Game")

    def test_category_constants(self):
        """Test category constants."""
        self.assertEqual(Category.MAIN_GAME, 1)
        self.assertEqual(Category.DLC, 2)
        self.assertEqual(Category.EXPANSION, 3)
        self.assertEqual(Category.STANDALONE_EXPANSION, 4)
        self.assertEqual(Category.REMAKE, 6)
        self.assertEqual(Category.REMASTER, 7)


class GameModelTest(TestCase):
    """Test Game model."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Main Game")

    def test_game_str_representation(self):
        """Test game string representation."""
        game = Game.objects.create(name="Test Game", category=self.category)
        self.assertEqual(str(game), "Test Game")

    def test_game_cover_url_with_cover(self):
        """Test game cover URL when cover exists."""
        game = Game.objects.create(name="Test Game", cover="test_cover", category=self.category)
        self.assertIn("test_cover.jpg", game.cover_url)

    def test_game_cover_url_without_cover(self):
        """Test game cover URL when cover is None."""
        game = Game.objects.create(name="Test Game", category=self.category)
        self.assertIsNone(game.cover_url)

    def test_game_is_released_with_past_date(self):
        """Test is_released returns True for past release date."""
        past_date = date.today() - timedelta(days=30)
        game = Game.objects.create(name="Test Game", release_date=past_date, category=self.category)
        self.assertTrue(game.is_released)

    def test_game_is_released_with_future_date(self):
        """Test is_released returns False for future release date."""
        future_date = date.today() + timedelta(days=30)
        game = Game.objects.create(name="Test Game", release_date=future_date, category=self.category)
        self.assertFalse(game.is_released)

    def test_game_is_released_with_no_date(self):
        """Test is_released returns False when no release date."""
        game = Game.objects.create(name="Test Game", category=self.category)
        self.assertFalse(game.is_released)

    def test_game_object_property(self):
        """Test game object property."""
        past_date = date.today() - timedelta(days=30)
        game = Game.objects.create(
            name="Test Game", cover="test_cover", release_date=past_date, category=self.category
        )
        obj = game.object
        self.assertEqual(obj["id"], game.pk)
        self.assertEqual(obj["name"], "Test Game")
        self.assertIn("test_cover.jpg", obj["cover"])
        self.assertEqual(obj["category"], "Main Game")
        self.assertTrue(obj["isReleased"])

    def test_game_filter_by_id(self):
        """Test game filter by ID."""
        game = Game.objects.create(name="Test Game", category=self.category)
        filtered = Game.filter(game_id=game.pk)
        self.assertEqual(filtered.count(), 1)
        self.assertEqual(filtered.first(), game)

    def test_game_filter_start_from_id(self):
        """Test game filter starting from ID."""
        game1 = Game.objects.create(name="Game 1", category=self.category)
        game2 = Game.objects.create(name="Game 2", category=self.category)
        filtered = Game.filter(game_id=game1.pk, start_from_id=True)
        self.assertIn(game1, filtered)
        self.assertIn(game2, filtered)


class ListModelTest(TestCase):
    """Test List model."""

    def test_list_str_representation(self):
        """Test list string representation."""
        game_list = List.objects.create(name="Want to Play", key_name="want_to_play")
        self.assertEqual(str(game_list), "Want to Play")

    def test_list_constants(self):
        """Test list constants."""
        self.assertEqual(List.WANT_TO_PLAY, 1)
        self.assertEqual(List.PLAYING, 2)
        self.assertEqual(List.BEATEN, 3)
        self.assertEqual(List.ON_HOLD, 4)

    def test_list_is_valid_id_true(self):
        """Test is_valid_id returns True for valid IDs."""
        self.assertTrue(List.is_valid_id(List.WANT_TO_PLAY))
        self.assertTrue(List.is_valid_id(List.PLAYING))
        self.assertTrue(List.is_valid_id(List.BEATEN))
        self.assertTrue(List.is_valid_id(List.ON_HOLD))

    def test_list_is_valid_id_false(self):
        """Test is_valid_id returns False for invalid IDs."""
        self.assertFalse(List.is_valid_id(0))
        self.assertFalse(List.is_valid_id(5))
        self.assertFalse(List.is_valid_id(999))


class RecordModelTest(TestCase):
    """Test Record model."""

    def setUp(self):
        """Set up test data."""
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Main Game")
        self.game = Game.objects.create(name="Test Game", category=self.category)
        self.game_list = List.objects.create(name="Want to Play", key_name="want_to_play")

    def test_record_str_representation(self):
        """Test record string representation."""
        record = Record.objects.create(user=self.user, game=self.game, list=self.game_list)
        expected = f"{self.user} - {self.game} - {self.game_list}"
        self.assertEqual(str(record), expected)

    def test_record_object_property(self):
        """Test record object property."""
        record = Record.objects.create(user=self.user, game=self.game, list=self.game_list, order=5)
        obj = record.object
        self.assertEqual(obj["id"], record.pk)
        self.assertEqual(obj["game"], self.game.object)
        self.assertEqual(obj["listKey"], "want_to_play")
        self.assertEqual(obj["order"], 5)

    def test_record_defaults(self):
        """Test record default values."""
        record = Record.objects.create(user=self.user, game=self.game, list=self.game_list)
        self.assertEqual(record.rating, 0)
        self.assertEqual(record.order, 0)
        self.assertEqual(record.comment, "")
