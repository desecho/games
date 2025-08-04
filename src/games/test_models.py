"""Tests for games app."""

from django.test import TestCase

from .models import User


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
