"""Views."""

from .health import HealthView
from .records import (
    ChangeListView,
    RecordAdd,
    RecordDeleteView,
    RecordRatingView,
    RecordsSaveOrderView,
    RecordsView,
    UserRecordsView,
)
from .search import SearchView
from .user import UserCheckEmailAvailabilityView, UserPreferencesView
from .users import UsersView

__all__ = [
    "SearchView",
    "RecordAdd",
    "ChangeListView",
    "RecordDeleteView",
    "RecordRatingView",
    "RecordsSaveOrderView",
    "RecordsView",
    "HealthView",
    "UserRecordsView",
    "UsersView",
    "UserPreferencesView",
    "UserCheckEmailAvailabilityView",
]
