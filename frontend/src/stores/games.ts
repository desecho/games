import { defineStore } from "pinia";
import axios from "axios";

import { GamesStore } from "../types";
import { getUrl } from "../helpers";
import { router } from "../router";

import { useAuthStore } from "./auth";

const gamesInitialState: GamesStore = {
  records: [],
  areLoaded: false,
};

export const useGamesStore = defineStore({
  id: "games",
  state: () => ({
    games: gamesInitialState,
  }),
  actions: {
    async loadGames(reload = false) {
      const { user } = useAuthStore();
      if (!user.isLoggedIn) {
        router.push("/login").catch(() => {});
      }
      if (this.games.areLoaded && !reload) {
        return;
      }

      const response = await axios.get(getUrl("games/"));
      this.games = {
        areLoaded: true,
        records: response.data,
      };
    },
    async reloadGames() {
      await this.loadGames(true);
    },
  },
});
