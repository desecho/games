import { getUrl, requireAuthenticated } from "../helpers";
import { useGamesStore } from "../stores/games";

export function addToList(gameId: number, listId: number, index: number, isProfile = false) {
  requireAuthenticated();
  // eslint-disable-next-line no-invalid-this
  this.axios
    .post(getUrl("records/add/"), { listId: listId, gameId: gameId })
    .then(async () => {
      if (!isProfile) {
        // eslint-disable-next-line vue/no-mutating-props,no-invalid-this
        this.games.splice(index, 1);
      }
      const { reloadGames } = useGamesStore();
      await reloadGames().catch((error) => {
        console.log(error);
        // eslint-disable-next-line no-invalid-this
        this.$toast.error("Error loading games");
      });
    })
    .catch((error) => {
      console.log(error);
      // eslint-disable-next-line no-invalid-this
      this.$toast.error("Error adding a game");
    });
}
