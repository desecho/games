"""Remove unused games."""
from typing import Any

from django_tqdm import BaseCommand

from games.models import Game


class Command(BaseCommand):
    """Remove unused games."""

    help = "Remove unused games"

    def handle(self, *args: Any, **options: Any) -> None:  # pylint: disable=unused-argument
        """Remove unused games."""
        games = Game.objects.all()
        tqdm = self.tqdm(total=games.count(), unit="game")
        for game in games:
            tqdm.set_description(game.name)
            if not game.records.exists():
                game.delete()
                message = f"{game} removed"
                tqdm.info(message)
            tqdm.update()
