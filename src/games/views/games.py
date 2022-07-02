"""Games views."""

from django.db.models import QuerySet
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Record, User


class GamesView(APIView):
    """Games view."""

    def get(self, request: Request) -> Response:  # pylint: disable=no-self-use
        """Get games."""
        user: User = request.user  # type: ignore
        records: QuerySet[Record] = user.records.all()
        results = [record.object for record in records]
        return Response(results)
