import { defineStore } from "pinia";

import { SettingsStore, GamesSettings } from "./types";

function getSettings(): SettingsStore {
  const settingsLocalStorageData = localStorage.getItem("settings");
  if (settingsLocalStorageData) {
    const settings: SettingsStore = JSON.parse(settingsLocalStorageData);
    return settings;
  }
  return {
    games: {
      areActionButtonsHidden: false,
      areUnreleasedGamesHidden: false,
      areDLCsHidden: false,
    },
    isGamesSettingsActive: false,
  };
}

function saveSettings(settings: SettingsStore) {
  localStorage.setItem("settings", JSON.stringify(settings));
}

export const useSettingsStore = defineStore({
  id: "settings",
  state: () => ({
    settings: getSettings(),
  }),
  actions: {
    saveGamesSettings(gamesSettings: GamesSettings) {
      this.settings.games = gamesSettings;
      saveSettings(this.settings);
    },
    toggleGamesSettings() {
      this.settings.isGamesSettingsActive = !this.settings.isGamesSettingsActive;
      saveSettings(this.settings);
    },
  },
});
