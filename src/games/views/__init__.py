"""Views."""
from .games import GamesView
from .health import HealthView
from .records import AddGameToListView, ChangeListView, RecordDeleteView, RecordsSaveOrderView
from .search import SearchView

__all__ = [
    "SearchView",
    "AddGameToListView",
    "ChangeListView",
    "RecordDeleteView",
    "RecordsSaveOrderView",
    "GamesView",
    "HealthView",
]
