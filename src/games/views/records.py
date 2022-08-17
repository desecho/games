"""Records views."""
from datetime import datetime
from http import HTTPStatus

from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Game, List, Record, User
from ..types import RecordObject
from .common import IGDBAPIView


def get_records_objects(user: User) -> list[RecordObject]:
    """Get records for user."""
    records: QuerySet[Record] = user.records.all()
    return [record.object for record in records]


class RecordsView(APIView):
    """Records view."""

    def get(self, request: Request) -> Response:  # pylint: disable=no-self-use
        """Get game records."""
        user: User = request.user  # type: ignore
        return Response(get_records_objects(user))


class UserRecordsView(APIView):
    """User records view."""

    permission_classes: list[str] = []  # type: ignore

    def get(self, request: Request, username: str) -> Response:  # pylint: disable=no-self-use,unused-argument
        """Get game records."""
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response(status=HTTPStatus.NOT_FOUND)

        if user.hidden:
            return Response(status=HTTPStatus.FORBIDDEN)

        return Response(get_records_objects(user))


class RecordAdd(IGDBAPIView):
    """Add game to list view."""

    def _get_game(self, game_id: int) -> Game:
        """Get game."""
        games = Game.objects.filter(pk=game_id)
        if games.exists():
            game: Game = games.first()  # type: ignore
            return game
        game_data = self.igdb.get_game(game_id)
        return Game.objects.create(**game_data)

    def _add_game_to_list(self, game_id: int, list_id: int) -> None:
        """Add game to list."""
        game = self._get_game(game_id)
        user: User = self.request.user  # type: ignore
        records = Record.objects.filter(game=game, user=user)
        if records.exists():
            records.update(list_id=list_id, date_added=datetime.now())
        else:
            Record.objects.create(game=game, list_id=list_id, user=user)

    def post(self, request: Request) -> Response:
        """Add game to list."""
        try:
            list_id = int(request.data["listId"])
            game_id = int(request.data["gameId"])
        except (KeyError, ValueError):
            return Response(status=HTTPStatus.BAD_REQUEST)

        if not List.is_valid_id(list_id):
            return Response(status=HTTPStatus.BAD_REQUEST)

        self._add_game_to_list(game_id, list_id)
        return Response(status=HTTPStatus.CREATED)


class ChangeListView(APIView):
    """Change list view."""

    def put(self, request: Request, record_id: int) -> Response:  # pylint: disable=no-self-use
        """Change list."""
        try:
            list_id = int(request.data["listId"])
        except (KeyError, ValueError):
            return Response(status=HTTPStatus.BAD_REQUEST)

        if not List.is_valid_id(list_id):
            return Response(status=HTTPStatus.BAD_REQUEST)

        user: User = request.user  # type: ignore
        records: QuerySet[Record] = user.records.filter(pk=record_id)
        if not records.exists():
            return Response(status=HTTPStatus.NOT_FOUND)
        records.update(list_id=list_id)
        return Response()


class RecordDeleteView(APIView):
    """Record delete view."""

    def delete(self, request: Request, record_id: int) -> Response:  # pylint: disable=no-self-use
        """Delete record."""
        user: User = request.user  # type: ignore
        records: QuerySet[Record] = user.records.filter(pk=record_id)
        if not records.exists():
            return Response(status=HTTPStatus.NOT_FOUND)
        records.delete()
        return Response()


class RecordsSaveOrderView(APIView):
    """Records save order view."""

    def put(self, request: Request) -> Response:  # pylint: disable=no-self-use
        """Save records order."""
        try:
            records = request.data["records"]
        except KeyError:
            return Response(status=HTTPStatus.BAD_REQUEST)

        user: User = self.request.user  # type: ignore
        for record in records:
            # If record ID is not found we silently ignore it
            Record.objects.filter(pk=record["id"], user=user).update(order=record["order"])
        return Response()
