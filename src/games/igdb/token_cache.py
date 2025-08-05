"""IGDB Token Cache Manager."""

import threading
import time
from typing import Optional

from authlib.integrations.requests_client import OAuth2Session
from django.conf import settings


class IGDBTokenCache:
    """Thread-safe token cache for IGDB API."""

    _instance: Optional["IGDBTokenCache"] = None
    _lock = threading.Lock()

    def __init__(self) -> None:
        """Initialize instance attributes."""
        if not hasattr(self, "_initialized"):
            self._token: Optional[str] = None
            self._expires_at: float = 0
            self._token_lock = threading.Lock()
            self._initialized = True

    def __new__(cls) -> "IGDBTokenCache":
        """Singleton pattern implementation."""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def get_token(self) -> str:
        """Get valid token, refreshing if necessary."""
        with self._token_lock:
            # Check if token exists and is not expired (with 60 second buffer)
            if self._token is not None and time.time() < (self._expires_at - 60):
                return self._token

            # Fetch new token
            return self._fetch_new_token()

    def _fetch_new_token(self) -> str:
        """Fetch a new token from IGDB OAuth endpoint."""
        session = OAuth2Session(  # nosec B106
            settings.IGDB_CLIENT_ID,
            settings.IGDB_CLIENT_SECRET,
            token_endpoint=settings.IGDB_TOKEN_ENDPOINT,
            grant_type="client_credentials",
            token_endpoint_auth_method="client_secret_post",
        )
        token_response = session.fetch_token()

        access_token: str = token_response["access_token"]
        self._token = access_token
        # IGDB tokens typically expire in 3600 seconds (1 hour)
        expires_in = token_response.get("expires_in", 3600)
        self._expires_at = time.time() + expires_in

        return access_token

    def clear_cache(self) -> None:
        """Clear cached token (useful for testing)."""
        with self._token_lock:
            self._token = None
            self._expires_at = 0
