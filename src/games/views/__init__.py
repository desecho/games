"""Views."""
from .health import HealthView
from .records import ChangeListView, RecordAdd, RecordDeleteView, RecordsSaveOrderView, RecordsView, UserRecordsView
from .search import SearchView
from .user import UserPreferencesView
from .users import UsersView

__all__ = [
    "SearchView",
    "RecordAdd",
    "ChangeListView",
    "RecordDeleteView",
    "RecordsSaveOrderView",
    "RecordsView",
    "HealthView",
    "UserRecordsView",
    "UsersView",
    "UserPreferencesView",
]
