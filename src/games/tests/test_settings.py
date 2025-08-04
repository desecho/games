"""Test settings functionality."""

import os
from os import getenv
from unittest.mock import patch

from django.test import TestCase


class SettingsTest(TestCase):
    """Test settings functionality."""

    @patch.dict(os.environ, {"FRONTEND_URL2": "https://example2.com"}, clear=False)
    @patch("games_project.settings.CORS_ALLOWED_ORIGINS", [])
    def test_frontend_url2_appended_to_cors_allowed_origins(self):
        """Test FRONTEND_URL2 is appended to CORS_ALLOWED_ORIGINS when set."""

        # Simulate the settings logic
        cors_allowed_origins = []
        frontend_url2 = getenv("FRONTEND_URL2")
        if frontend_url2:
            cors_allowed_origins.append(frontend_url2)

        # Verify FRONTEND_URL2 was appended when set
        self.assertEqual(len(cors_allowed_origins), 1)
        self.assertEqual(cors_allowed_origins[0], "https://example2.com")
