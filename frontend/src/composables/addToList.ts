import { AxiosError, AxiosStatic } from "axios";
import { inject, Ref } from "vue";

import { Game } from "../types";
import { $toast } from "../toast";
import { getUrl, requireAuthenticated } from "../helpers";
import { useGamesStore } from "../stores/games";

export function useAddToList() {
  // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  const axios: AxiosStatic = inject("axios")!;

  function addToList(gameId: number, listId: number, index: number | null = null, games: Ref<Game[]> | null = null) {
    requireAuthenticated();
    axios
      .post(getUrl("records/add/"), { listId: listId, gameId: gameId })
      .then(async () => {
        if (index !== null && games !== null) {
          games.value.splice(index, 1);
        }
        const { reloadGames } = useGamesStore();
        await reloadGames().catch((error: AxiosError) => {
          console.log(error);
          $toast.error("Error loading games");
        });
      })
      .catch((error: AxiosError) => {
        console.log(error);
        $toast.error("Error adding a game");
      });
  }

  return { addToList };
}
