"""Views."""

from .health import HealthView
from .recommendations import RecommendationsView
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
    "RecommendationsView",
    "HealthView",
    "UserRecordsView",
    "UsersView",
    "UserPreferencesView",
    "UserCheckEmailAvailabilityView",
]
