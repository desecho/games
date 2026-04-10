"""Settings for tests."""

from .settings import *  # noqa: F403,F401

DATABASES["default"] = {  # noqa
    "ENGINE": "django.db.backends.sqlite3",
    "NAME": ":memory:",
}


CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.dummy.DummyCache",
    }
}

SECRET_KEY = "key"  # nosec B105
IS_TEST = True
