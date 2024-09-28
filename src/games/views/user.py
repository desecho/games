"""User views."""

from http import HTTPStatus

from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import User


class UserCheckEmailAvailabilityView(APIView):
    """Check email availability view."""

    permission_classes: list[str] = []  # type: ignore

    def post(self, request: Request) -> Response:  # pylint: disable=no-self-use
        """Return True if email is available."""
        try:
            email = request.data["email"]
        except KeyError:
            return Response(status=HTTPStatus.BAD_REQUEST)
        response = not User.objects.filter(email=email).exists()
        return Response(response)


class UserPreferencesView(APIView):
    """User preferences view."""

    def put(self, request: Request) -> Response:  # pylint: disable=no-self-use
        """Save preferences."""
        user: User = request.user  # type: ignore
        try:
            hidden = bool(request.data["hidden"])
        except (KeyError, ValueError):
            return Response(status=HTTPStatus.BAD_REQUEST)
        user.hidden = hidden
        user.save()
        return Response()

    def get(self, request: Request) -> Response:  # pylint: disable=no-self-use
        """Load preferences."""
        user: User = request.user  # type: ignore
        return Response(user.preferences)
