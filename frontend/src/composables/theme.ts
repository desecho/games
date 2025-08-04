import { watch } from "vue";
import { useTheme } from "vuetify";

import { useSettingsStore } from "../stores/settings";

export function useAppTheme(): { initializeTheme: () => void; applyTheme: () => void } {
  const settingsStore = useSettingsStore();
  const theme = useTheme();

  // Apply the current theme setting
  function applyTheme(): void {
    theme.global.name.value = settingsStore.settings.darkMode ? "dark" : "light";
  }

  // Initialize theme and watch for changes
  function initializeTheme(): void {
    applyTheme();

    // Watch for changes in dark mode setting
    watch(
      () => settingsStore.settings.darkMode,
      () => {
        applyTheme();
      },
      { immediate: true },
    );
  }

  return {
    initializeTheme,
    applyTheme,
  };
}
