import axios from "axios";
import { defineStore } from "pinia";

import type { RecordType } from "../types";

import { getUrl } from "../helpers";
import { router } from "../router";

import { useAuthStore } from "./auth";

const recordsInitialState: RecordType[] = [];

export const useGamesStore = defineStore({
  id: "games",
  state: () => ({
    records: recordsInitialState,
    areLoaded: false,
    tab: "want-to-play",
  }),
  actions: {
    async loadGames(reload = false) {
      console.log("Loading games...");
      const { user } = useAuthStore();
      if (!user.isLoggedIn) {
        void router.push("/login");
      }
      if (this.areLoaded && !reload) {
        return;
      }

      const response = await axios.get(getUrl("records/"));
      this.areLoaded = true;
      this.records = response.data as RecordType[];
    },
    async reloadGames() {
      await this.loadGames(true);
    },
  },
});
