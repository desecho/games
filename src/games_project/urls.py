"""URL Configuration."""
from typing import List

import debug_toolbar
from django.conf import settings
from django.conf.urls import include
from django.contrib import admin
from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from games.types import URL
from games.views import (
    AddGameToListView,
    ChangeListView,
    GamesView,
    HealthView,
    RecordDeleteView,
    RecordsSaveOrderView,
    SearchView,
)

urlpatterns: List[URL] = []

if settings.DEBUG:  # pragma: no cover
    urlpatterns += [
        path("__debug__/", include(debug_toolbar.urls)),
    ]


urlpatterns += [
    # Admin
    path("admin/", admin.site.urls),
    # Auth
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    # Search
    path("search/", SearchView.as_view()),
    # Health
    path("health/", HealthView.as_view()),
    # Games
    path("games/", GamesView.as_view()),
    # Records
    path("records/add/", AddGameToListView.as_view()),
    path("records/save-order/", RecordsSaveOrderView.as_view()),
    path("records/<int:record_id>/change-list/", ChangeListView.as_view()),
    path("records/<int:record_id>/delete/", RecordDeleteView.as_view()),
]
