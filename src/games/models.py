"""Models."""
from typing import Optional

from django.contrib.auth.models import AbstractUser
from django.db.models import (
    CASCADE,
    BooleanField,
    CharField,
    DateField,
    DateTimeField,
    ForeignKey,
    Model,
    PositiveSmallIntegerField,
    UniqueConstraint,
)

from .types import GameObject, RecordObject
from .utils import get_cover_url


class User(AbstractUser):
    """User model."""

    hidden = BooleanField(default=False)

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.username)


class Category(Model):
    """Category."""

    # Full list is available here: https://api-docs.igdb.com/#game-enums
    MAIN_GAME = 1
    DLC = 2
    EXPANSION = 3
    STANDALONE_EXPANSION = 4
    REMAKE = 6
    REMASTER = 7

    name = CharField(max_length=20, unique=True)

    class Meta:
        """Meta."""

        verbose_name_plural = "categories"
        ordering = ["pk"]

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.name)


class Game(Model):
    """Game."""

    name = CharField(max_length=255)
    cover = CharField(max_length=255, null=True)
    release_date = DateField(null=True)
    category = ForeignKey(Category, CASCADE)

    class Meta:
        """Meta."""

        ordering = ["pk"]

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.name)

    @property
    def cover_url(self) -> Optional[str]:
        """Cover URL."""
        if self.cover is None:
            return None
        return get_cover_url(self.cover)

    @property
    def object(self) -> GameObject:
        """Get object."""
        return {
            "id": self.pk,
            "name": self.name,
            "cover": self.cover_url,
            "category": self.category.name,
        }


class ListModel(Model):
    """List."""

    WANT_TO_PLAY = 1
    PLAYING = 2
    BEATEN = 3
    ON_HOLD = 4
    name = CharField(max_length=255, unique=True)
    key_name = CharField(max_length=255, db_index=True, unique=True)

    class Meta:
        """Meta."""

        verbose_name = "list"
        verbose_name_plural = "lists"
        ordering = ["pk"]

    def __str__(self) -> str:
        """Return string representation."""
        return str(self.name)

    @classmethod
    def is_valid_id(cls, list_id: int) -> bool:
        """Return True if list ID is valid."""
        return list_id in [cls.WANT_TO_PLAY, cls.PLAYING, cls.BEATEN, cls.ON_HOLD]


class Record(Model):
    """Record."""

    user = ForeignKey(User, CASCADE, related_name="records")
    game = ForeignKey(Game, CASCADE, related_name="records")
    list = ForeignKey(ListModel, CASCADE)
    rating = PositiveSmallIntegerField(default=0)
    order = PositiveSmallIntegerField(default=0)
    comment = CharField(max_length=255, default="")
    date_added = DateTimeField(auto_now_add=True)

    class Meta:
        """Meta."""

        constraints = [
            # A user should only have one record per game.
            UniqueConstraint(fields=("user", "game"), name="unique_user_game_record"),
        ]
        ordering = ["order"]

    def __str__(self) -> str:
        """Return string representation."""
        return f"{self.user} - {self.game} - {self.list}"

    @property
    def object(self) -> RecordObject:
        """Get object."""
        return {
            "id": self.pk,
            "game": self.game.object,
            "listKey": self.list.key_name,
            "order": self.order,
        }
