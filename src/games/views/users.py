"""Users views."""

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from games.models import User


class UsersView(APIView):
    """Users view."""

    permission_classes: list[str] = []  # type: ignore

    def get(self, request: Request) -> Response:  # pylint: disable=no-self-use,unused-argument
        """Get user list."""
        users = User.objects.filter(hidden=False).values_list("username", flat=True)
        return Response(users)
