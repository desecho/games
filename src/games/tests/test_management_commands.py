"""Tests for management commands."""

from io import StringIO
from unittest.mock import Mock, patch

from django.core.management import call_command
from django.test import TestCase

from games.models import Category, Game, List, Record, User


class RemoveUnusedGamesCommandTest(TestCase):
    """Test remove unused games command."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Main Game")
        self.used_game = Game.objects.create(name="Used Game", category=self.category)
        self.unused_game = Game.objects.create(name="Unused Game", category=self.category)

        # Create a record for the used game
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.game_list = List.objects.create(name="Want to Play", key_name="want_to_play")
        Record.objects.create(user=self.user, game=self.used_game, list=self.game_list)

    def test_removes_unused_games_only(self):
        """Test that only unused games are removed."""
        out = StringIO()
        call_command("remove_unused_games", stdout=out)

        # Used game should still exist
        self.assertTrue(Game.objects.filter(id=self.used_game.id).exists())

        # Unused game should be removed
        self.assertFalse(Game.objects.filter(id=self.unused_game.id).exists())

    def test_handles_empty_database(self):
        """Test command handles empty database gracefully."""
        Game.objects.all().delete()
        out = StringIO()
        call_command("remove_unused_games", stdout=out)

        # Should not raise any errors
        self.assertEqual(Game.objects.count(), 0)


class UpdateGamesDataCommandTest(TestCase):
    """Test update games data command."""

    def setUp(self):
        """Set up test data."""
        self.category = Category.objects.create(name="Main Game")
        self.game = Game.objects.create(name="Test Game", category=self.category)

    @patch("games.management.commands.update_games_data.IGDB")
    def test_update_single_game(self, mock_igdb_class):
        """Test updating a single game."""
        mock_igdb = Mock()
        mock_igdb.get_game.return_value = {
            "id": self.game.id,
            "name": "Updated Game Name",
            "category_id": 1,
            "release_date": None,
            "cover": None,
        }
        mock_igdb_class.return_value = mock_igdb

        out = StringIO()
        call_command("update_games_data", str(self.game.id), stdout=out)

        mock_igdb.get_game.assert_called_once_with(self.game.pk)

    @patch("games.management.commands.update_games_data.IGDB")
    def test_update_all_games(self, mock_igdb_class):
        """Test updating all games."""
        mock_igdb = Mock()
        mock_igdb.get_game.return_value = {
            "id": self.game.id,
            "name": "Updated Game Name",
            "category_id": 1,
            "release_date": None,
            "cover": None,
        }
        mock_igdb_class.return_value = mock_igdb

        out = StringIO()
        call_command("update_games_data", stdout=out)

        mock_igdb.get_game.assert_called_with(self.game.pk)

    @patch("games.management.commands.update_games_data.IGDB")
    def test_update_game_with_changes_logs_info(self, mock_igdb_class):
        """Test that updating a game with changes logs info message."""
        mock_igdb = Mock()
        # Return different data to trigger the "updated" condition
        mock_igdb.get_game.return_value = {
            "id": self.game.id,
            "name": "Changed Game Name",  # Different from original
            "category_id": 1,
            "release_date": None,
            "cover": None,
        }
        mock_igdb_class.return_value = mock_igdb

        out = StringIO()
        call_command("update_games_data", str(self.game.id), stdout=out)

        # Check that the info message was logged for updated game
        output = out.getvalue()
        self.assertIn(f'"{self.game.name}" is updated', output)

    @patch("games.management.commands.update_games_data.IGDB")
    def test_start_from_id_option(self, mock_igdb_class):
        """Test start from ID option."""
        # Create another game with higher ID
        Game.objects.create(name="Test Game 2", category=self.category)

        mock_igdb = Mock()

        def mock_get_game(game_id):
            return {"id": game_id, "name": "Updated Game Name", "category_id": 1, "release_date": None, "cover": None}

        mock_igdb.get_game.side_effect = mock_get_game
        mock_igdb_class.return_value = mock_igdb

        out = StringIO()
        call_command("update_games_data", str(self.game.id), "-s", stdout=out)

        # Should process both games (starting from game.id)
        self.assertEqual(mock_igdb.get_game.call_count, 2)

    @patch("games.management.commands.update_games_data.IGDB")
    def test_nonexistent_game_id_error(self, _mock_igdb_class):
        """Test error handling for nonexistent game ID."""
        out = StringIO()
        err = StringIO()

        with self.assertRaises(SystemExit):
            call_command("update_games_data", "999999", stderr=err, stdout=out)

    @patch("games.management.commands.update_games_data.IGDB")
    def test_start_from_too_high_id_error(self, _mock_igdb_class):
        """Test error handling when start_from_id is too high."""
        out = StringIO()
        err = StringIO()

        with self.assertRaises(SystemExit):
            call_command("update_games_data", "999999", "-s", stderr=err, stdout=out)
