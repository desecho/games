import { defineStore } from "pinia";

export const useSettingsStore = defineStore({
  id: "settings",
  state: () => ({
    settings: {
      games: {
        areActionButtonsHidden: false,
        areUnreleasedGamesHidden: false,
        areDLCsHidden: false,
      },
      isGamesSettingsActive: false,
    },
  }),
  persist: {
    enabled: true,
    strategies: [
      {
        key: "settings",
        storage: localStorage,
      },
    ],
  },
  actions: {
    toggleGamesSettings() {
      this.settings.isGamesSettingsActive = !this.settings.isGamesSettingsActive;
    },
  },
});
