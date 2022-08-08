import { defineStore } from "pinia";

import { SettingsStore } from "./types";

function getSettings(): SettingsStore {
  const settingsLocalStorageData = localStorage.getItem("settings");
  if (settingsLocalStorageData) {
    const settings = JSON.parse(settingsLocalStorageData) as SettingsStore;
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

function saveSettingsToLocalStorage(settings: SettingsStore) {
  localStorage.setItem("settings", JSON.stringify(settings));
}

export const useSettingsStore = defineStore({
  id: "settings",
  state: () => ({
    settings: getSettings(),
  }),
  actions: {
    persistSettings() {
      saveSettingsToLocalStorage(this.settings);
    },
    toggleGamesSettings() {
      this.settings.isGamesSettingsActive = !this.settings.isGamesSettingsActive;
      saveSettingsToLocalStorage(this.settings);
    },
  },
});
