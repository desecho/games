import axios from "axios";

import type { AxiosError } from "axios";

import { getUrl, requireAuthenticated } from "../helpers";
import { useGamesStore } from "../stores/games";
import { $toast } from "../toast";

export function useAddToList(): {
  addToList: (gameId: number, listId: number) => Promise<void>;
} {
  async function addToList(gameId: number, listId: number): Promise<void> {
    console.log("Adding to list");
    requireAuthenticated();
    await axios.post(getUrl("records/add/"), { listId, gameId });
    const { reloadGames } = useGamesStore();
    reloadGames()
      .then(() => {
        console.log("Games reloaded");
      })
      .catch((error: AxiosError) => {
        console.log(error);
        $toast.error("Error reloading games");
      });
  }

  return { addToList };
}
