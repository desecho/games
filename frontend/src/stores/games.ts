import { defineStore } from "pinia";
import axios from "axios";

import { RecordType } from "../types";
import { getUrl } from "../helpers";
import { router } from "../router";
import { useAuthStore } from "./auth";

const recordsInitialState: RecordType[] = [];

export const useGamesStore = defineStore({
  id: "games",
  state: () => ({
    records: recordsInitialState,
    areLoaded: false,
  }),
  actions: {
    async loadGames(reload = false) {
      const { user } = useAuthStore();
      if (!user.isLoggedIn) {
        router.push("/login").catch(() => {});
      }
      if (this.areLoaded && !reload) {
        return;
      }

      const response = await axios.get(getUrl("records/"));
      this.areLoaded = true;
      this.records = response.data;
    },
    async reloadGames() {
      await this.loadGames(true);
    },
  },
});
