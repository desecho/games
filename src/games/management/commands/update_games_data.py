"""Update games data."""

from typing import Any, Optional

from django.core.management.base import CommandParser
from django_tqdm import BaseCommand

from games.igdb import IGDB
from games.models import Game


class Command(BaseCommand):
    """Update games data."""

    help = """Update all games data

    If one argument is used then the game with the selected game_id is updated.
    If no arguments are used - all games are updated.
    """

    def add_arguments(self, parser: CommandParser) -> None:
        """Add arguments."""
        parser.add_argument("game_id", nargs="?", default=None, type=int)
        parser.add_argument(
            "-s",
            action="store_true",
            dest="start_from_id",
            default=False,
            help="Start running the script from provided game id",
        )

    def __init__(self, *args: Any, **kwargs: Any):
        """Initialize."""
        self.igdb = IGDB()
        super().__init__(*args, **kwargs)

    def _update_game_data(self, game: Game) -> bool:
        """Return if the game was updated or not."""
        game_data = self.igdb.get_game(game.pk)
        # Use filter here to be able to use "update" functionality.
        # We will always have only one game.
        games = Game.objects.filter(pk=game.pk)
        game_initial_data = games.values()[0]
        games.update(**game_data)
        game_updated_data = Game.objects.filter(pk=game.pk).values()[0]
        updated: bool = game_initial_data != game_updated_data
        return updated

    def handle(
        self,
        *args: Any,
        **options: Any,  # pylint: disable=unused-argument
    ) -> None:
        """Execute command."""
        game_id: Optional[int] = options["game_id"]
        start_from_id: bool = options["start_from_id"]
        games = Game.filter(game_id, start_from_id)
        games_total = games.count()
        # We don't want a progress bar if we just have one game to process
        disable = games_total == 1
        if not games:  # In case game_id is too high and we don't get any games
            if start_from_id:
                self.error(f"There are no games with IDs > {game_id}", fatal=True)
            else:
                # Assume we have at least one game in the DB
                self.error(f"There is no game with ID {game_id}", fatal=True)

        tqdm = self.tqdm(total=games_total, unit="games", disable=disable)
        for game in games:
            tqdm.set_description(str(game))
            updated = self._update_game_data(game)
            if updated:
                tqdm.info(f'"{game}" is updated')
            tqdm.update()
