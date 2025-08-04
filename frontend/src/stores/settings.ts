import { defineStore } from "pinia";

export const useSettingsStore = defineStore("settings", {
  state: () => ({
    settings: {
      games: {
        areActionButtonsHidden: false,
        areUnreleasedGamesHidden: false,
        areDLCsHidden: false,
      },
      isGamesSettingsActive: false,
      darkMode: false,
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
    toggleDarkMode() {
      this.settings.darkMode = !this.settings.darkMode;
    },
  },
});
