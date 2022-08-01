import { defineStore } from "pinia";

import { SettingsStore, GamesSettings } from "./types";

function getSettings(): SettingsStore {
  const settingsLocalStorageData = localStorage.getItem("settings");
  if (settingsLocalStorageData) {
    const user: SettingsStore = JSON.parse(settingsLocalStorageData);
    return user;
  }
  return {
    games: {
      areActionButtonsHidden: false,
      areUnreleasedGamesHidden: false,
    },
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
  },
});
