"""Admin."""
from typing import Optional

from django.contrib.admin import ModelAdmin, register, site
from django.contrib.auth.models import Group
from django.http import HttpRequest

from .models import Category, Game, List, Record, User


@register(Record)
class RecordAdmin(ModelAdmin[Record]):  # pylint:disable=unsubscriptable-object
    """Record admin."""

    list_display = ("user", "game", "list", "date_added")
    search_fields = ("game__name", "user__username", "user__first_name", "user__last_name")


@register(Game)
class GameAdmin(ModelAdmin[Game]):  # pylint:disable=unsubscriptable-object
    """Game admin."""

    list_display = ("name",)
    search_fields = ("name",)


@register(List)
class ListAdmin(ModelAdmin[List]):  # pylint:disable=unsubscriptable-object
    """List admin."""

    def has_delete_permission(  # pylint:disable=no-self-use,unused-argument
        self, request: HttpRequest, obj: Optional[List] = None
    ) -> bool:
        """Return True if the user has delete permission."""
        return False


@register(Category)
class CategoryAdmin(ModelAdmin[Category]):  # pylint:disable=unsubscriptable-object
    """Category admin."""

    list_display = ("name",)
    search_fields = ("name",)

    def has_delete_permission(  # pylint:disable=no-self-use,unused-argument
        self, request: HttpRequest, obj: Optional[Category] = None
    ) -> bool:
        """Return True if the user has delete permission."""
        return False


@register(User)
class UserAdmin(ModelAdmin[User]):  # pylint:disable=unsubscriptable-object
    """User admin."""

    list_display = ("username", "first_name", "last_name")
    search_fields = ("username", "first_name", "last_name")


site.unregister(Group)
