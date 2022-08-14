"""URL Configuration."""
from django.contrib import admin
from django.urls import include, path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from games.types import URL
from games.views import (
    ChangeListView,
    HealthView,
    RecordAdd,
    RecordDeleteView,
    RecordsSaveOrderView,
    RecordsView,
    SearchView,
    UserCheckEmailAvailabilityView,
    UserPreferencesView,
    UserRecordsView,
    UsersView,
)

urlpatterns: list[URL] = [
    # Health
    path("health/", HealthView.as_view()),
    # Admin
    path("admin/", admin.site.urls),
    # Auth
    path("token/", TokenObtainPairView.as_view()),
    path("token/refresh/", TokenRefreshView.as_view()),
    # User
    path("user/", include("rest_registration.api.urls")),
    path("user/preferences/", UserPreferencesView.as_view()),
    path("user/check-email-availability/", UserCheckEmailAvailabilityView.as_view()),
    # Search
    path("search/", SearchView.as_view()),
    # Users
    path("users/", UsersView.as_view()),
    # Records
    path("records/", RecordsView.as_view()),
    path("records/add/", RecordAdd.as_view()),
    path("records/save-order/", RecordsSaveOrderView.as_view()),
    path("records/<int:record_id>/change-list/", ChangeListView.as_view()),
    path("records/<int:record_id>/delete/", RecordDeleteView.as_view()),
    path("records/users/<str:username>/", UserRecordsView.as_view()),
]
