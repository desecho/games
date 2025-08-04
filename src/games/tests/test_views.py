"""Tests for views."""

from unittest.mock import Mock, patch

from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from games.models import Category, Game, List, Record, User


class HealthViewTest(TestCase):
    """Test health view."""

    def setUp(self):
        """Set up test client."""
        self.client = APIClient()

    def test_health_check(self):
        """Test health check endpoint."""
        response = self.client.get("/health/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"status": "ok"})


class UsersViewTest(TestCase):
    """Test users view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.visible_user = User.objects.create_user(username="visible", email="visible@example.com")
        self.hidden_user = User.objects.create_user(username="hidden", email="hidden@example.com", hidden=True)

    def test_get_visible_users_only(self):
        """Test that only visible users are returned."""
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("visible", response.data)
        self.assertNotIn("hidden", response.data)


class UserCheckEmailAvailabilityViewTest(TestCase):
    """Test user email availability view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        User.objects.create_user(username="existing", email="existing@example.com")

    def test_email_available(self):
        """Test available email returns True."""
        response = self.client.post("/user/check-email-availability/", {"email": "new@example.com"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data)

    def test_email_not_available(self):
        """Test existing email returns False."""
        response = self.client.post(
            "/user/check-email-availability/", {"email": "existing@example.com"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(response.data)

    def test_missing_email_parameter(self):
        """Test missing email parameter returns 400."""
        response = self.client.post("/user/check-email-availability/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserPreferencesViewTest(TestCase):
    """Test user preferences view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.client.force_authenticate(user=self.user)

    def test_get_preferences(self):
        """Test getting user preferences."""
        response = self.client.get("/user/preferences/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, {"hidden": False})

    def test_update_preferences(self):
        """Test updating user preferences."""
        response = self.client.put("/user/preferences/", {"hidden": True}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.hidden)

    def test_update_preferences_missing_parameter(self):
        """Test updating preferences with missing parameter returns 400."""
        response = self.client.put("/user/preferences/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_preferences_invalid_value(self):
        """Test updating preferences with string value succeeds (converted to bool)."""
        response = self.client.put("/user/preferences/", {"hidden": "invalid"}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.user.refresh_from_db()
        self.assertTrue(self.user.hidden)  # Non-empty string converts to True


class RecordsViewTest(TestCase):
    """Test records view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Main Game")
        self.game = Game.objects.create(name="Test Game", category=self.category)
        self.game_list = List.objects.create(name="Want to Play", key_name="want_to_play")
        self.record = Record.objects.create(user=self.user, game=self.game, list=self.game_list)
        self.client.force_authenticate(user=self.user)

    def test_get_user_records(self):
        """Test getting authenticated user's records."""
        response = self.client.get("/records/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["game"]["name"], "Test Game")


class UserRecordsViewTest(TestCase):
    """Test user records view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.visible_user = User.objects.create_user(username="visible", email="visible@example.com")
        self.hidden_user = User.objects.create_user(username="hidden", email="hidden@example.com", hidden=True)
        self.category = Category.objects.create(name="Main Game")
        self.game = Game.objects.create(name="Test Game", category=self.category)
        self.game_list = List.objects.create(name="Want to Play", key_name="want_to_play")
        Record.objects.create(user=self.visible_user, game=self.game, list=self.game_list)

    def test_get_visible_user_records(self):
        """Test getting visible user's records."""
        response = self.client.get(f"/records/users/{self.visible_user.username}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_hidden_user_records_forbidden(self):
        """Test getting hidden user's records returns 403."""
        response = self.client.get(f"/records/users/{self.hidden_user.username}/")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_nonexistent_user_records(self):
        """Test getting nonexistent user's records returns 404."""
        response = self.client.get("/records/users/nonexistent/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RecordAddViewTest(TestCase):
    """Test record add view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Main Game")
        self.game = Game.objects.create(name="Test Game", category=self.category)
        self.game_list = List.objects.create(name="Want to Play", key_name="want_to_play")
        self.client.force_authenticate(user=self.user)

    @patch("games.views.common.IGDB")
    def test_add_game_to_list_missing_parameters(self, _mock_igdb_class):
        """Test adding game with missing parameters returns 400."""
        response = self.client.post("/records/add/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("games.views.common.IGDB")
    def test_add_game_to_list_invalid_list_id(self, _mock_igdb_class):
        """Test adding game with invalid list ID returns 400."""
        response = self.client.post("/records/add/", {"gameId": self.game.id, "listId": 999}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("games.views.common.IGDB")
    def test_add_existing_game_to_list(self, _mock_igdb_class):
        """Test adding existing game to list creates record."""
        response = self.client.post(
            "/records/add/", {"gameId": self.game.id, "listId": self.game_list.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(Record.objects.filter(user=self.user, game=self.game, list=self.game_list).exists())

    @patch("games.views.common.IGDB")
    def test_update_existing_record(self, _mock_igdb_class):
        """Test adding game that user already has updates the record."""
        Record.objects.create(user=self.user, game=self.game, list=self.game_list)

        new_list = List.objects.create(name="Playing", key_name="playing")
        response = self.client.post("/records/add/", {"gameId": self.game.id, "listId": new_list.id}, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        record = Record.objects.get(user=self.user, game=self.game)
        self.assertEqual(record.list_id, new_list.id)

    @patch("games.views.common.IGDB")
    def test_add_nonexistent_game_creates_from_igdb(self, mock_igdb_class):
        """Test adding nonexistent game fetches from IGDB and creates game."""
        mock_igdb = Mock()
        mock_igdb.get_game.return_value = {
            "id": 999,
            "name": "New Game from IGDB",
            "category_id": self.category.id,
            "release_date": None,
            "cover": None,
        }
        mock_igdb_class.return_value = mock_igdb

        # Use a game ID that doesn't exist
        nonexistent_game_id = 999
        response = self.client.post(
            "/records/add/", {"gameId": nonexistent_game_id, "listId": self.game_list.id}, format="json"
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        mock_igdb.get_game.assert_called_once_with(nonexistent_game_id)

        # Verify the game was created
        created_game = Game.objects.get(id=nonexistent_game_id)
        self.assertEqual(created_game.name, "New Game from IGDB")

        # Verify the record was created
        self.assertTrue(Record.objects.filter(user=self.user, game=created_game, list=self.game_list).exists())


class ChangeListViewTest(TestCase):
    """Test change list view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Main Game")
        self.game = Game.objects.create(name="Test Game", category=self.category)
        self.game_list = List.objects.create(name="Want to Play", key_name="want_to_play")
        self.new_list = List.objects.create(name="Playing", key_name="playing")
        self.record = Record.objects.create(user=self.user, game=self.game, list=self.game_list)
        self.client.force_authenticate(user=self.user)

    def test_change_list_success(self):
        """Test successfully changing list."""
        response = self.client.put(
            f"/records/{self.record.id}/change-list/", {"listId": self.new_list.id}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.record.refresh_from_db()
        self.assertEqual(self.record.list_id, self.new_list.id)

    def test_change_list_missing_parameter(self):
        """Test changing list with missing parameter returns 400."""
        response = self.client.put(f"/records/{self.record.id}/change-list/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_list_invalid_list_id(self):
        """Test changing list with invalid list ID returns 400."""
        response = self.client.put(f"/records/{self.record.id}/change-list/", {"listId": 999}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_change_list_nonexistent_record(self):
        """Test changing list for nonexistent record returns 404."""
        response = self.client.put("/records/999/change-list/", {"listId": self.new_list.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RecordDeleteViewTest(TestCase):
    """Test record delete view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Main Game")
        self.game = Game.objects.create(name="Test Game", category=self.category)
        self.game_list = List.objects.create(name="Want to Play", key_name="want_to_play")
        self.record = Record.objects.create(user=self.user, game=self.game, list=self.game_list)
        self.client.force_authenticate(user=self.user)

    def test_delete_record_success(self):
        """Test successfully deleting record."""
        response = self.client.delete(f"/records/{self.record.id}/delete/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertFalse(Record.objects.filter(id=self.record.id).exists())

    def test_delete_nonexistent_record(self):
        """Test deleting nonexistent record returns 404."""
        response = self.client.delete("/records/999/delete/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class RecordsSaveOrderViewTest(TestCase):
    """Test records save order view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Main Game")
        self.game_list = List.objects.create(name="Want to Play", key_name="want_to_play")

        game1 = Game.objects.create(name="Test Game 1", category=self.category)
        game2 = Game.objects.create(name="Test Game 2", category=self.category)
        self.record1 = Record.objects.create(user=self.user, game=game1, list=self.game_list)
        self.record2 = Record.objects.create(user=self.user, game=game2, list=self.game_list)
        self.client.force_authenticate(user=self.user)

    def test_save_order_success(self):
        """Test successfully saving order."""
        records_data = [{"id": self.record1.id, "order": 5}, {"id": self.record2.id, "order": 10}]
        response = self.client.put("/records/save-order/", {"records": records_data}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.record1.refresh_from_db()
        self.record2.refresh_from_db()
        self.assertEqual(self.record1.order, 5)
        self.assertEqual(self.record2.order, 10)

    def test_save_order_missing_parameter(self):
        """Test saving order with missing parameter returns 400."""
        response = self.client.put("/records/save-order/", {}, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_save_order_with_invalid_record_id(self):
        """Test saving order with invalid record ID is silently ignored."""
        records_data = [{"id": 999, "order": 5}, {"id": self.record1.id, "order": 10}]
        response = self.client.put("/records/save-order/", {"records": records_data}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.record1.refresh_from_db()
        self.assertEqual(self.record1.order, 10)


class SearchViewTest(TestCase):
    """Test search view."""

    def setUp(self):
        """Set up test data."""
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", email="test@example.com")
        self.category = Category.objects.create(name="Main Game")
        self.game = Game.objects.create(name="Test Game", category=self.category)
        self.game_list = List.objects.create(name="Want to Play", key_name="want_to_play")

    @patch("games.views.common.IGDB")
    def test_search_missing_query_parameter(self, _mock_igdb_class):
        """Test search with missing query parameter returns 400."""
        response = self.client.get("/search/")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @patch("games.views.common.IGDB")
    def test_search_unauthenticated_user(self, mock_igdb_class):
        """Test search works for unauthenticated users."""
        # Mock the IGDB search to avoid external API calls
        mock_igdb = mock_igdb_class.return_value
        mock_igdb.search_games.return_value = []

        with self.settings(TESTING=True):
            response = self.client.get("/search/?query=test")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("games.views.common.IGDB")
    def test_search_authenticated_user_filters_owned_games(self, mock_igdb_class):
        """Test search filters out user's owned games for authenticated users."""
        Record.objects.create(user=self.user, game=self.game, list=self.game_list)
        self.client.force_authenticate(user=self.user)

        mock_igdb = mock_igdb_class.return_value
        mock_igdb.search_games.return_value = []

        with self.settings(TESTING=True):
            response = self.client.get("/search/?query=test")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

    @patch("games.views.common.IGDB")
    def test_search_authenticated_user_removes_owned_games(self, mock_igdb_class):
        """Test search removes user's owned games from results for authenticated users."""
        # Create a record for the user owning the game
        Record.objects.create(user=self.user, game=self.game, list=self.game_list)
        self.client.force_authenticate(user=self.user)

        # Mock IGDB to return search results including the user's game
        mock_igdb = mock_igdb_class.return_value
        mock_igdb.search_games.return_value = [
            {"id": self.game.id, "name": "Test Game"},  # User owns this game
            {"id": 999, "name": "Other Game"},  # User doesn't own this game
        ]

        with self.settings(TESTING=True):
            response = self.client.get("/search/?query=test")
            self.assertEqual(response.status_code, status.HTTP_200_OK)

            # Verify the user's owned game was filtered out
            results = response.json()
            self.assertEqual(len(results), 1)
            self.assertEqual(results[0]["id"], 999)
            self.assertEqual(results[0]["name"], "Other Game")
