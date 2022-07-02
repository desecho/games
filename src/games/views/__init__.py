"""Views."""
from .games import GamesView
from .records import AddGameToListView, ChangeListView, RecordDeleteView, RecordsSaveOrderView
from .search import SearchView

__all__ = [
    "SearchView",
    "AddGameToListView",
    "ChangeListView",
    "RecordDeleteView",
    "RecordsSaveOrderView",
    "GamesView",
]
