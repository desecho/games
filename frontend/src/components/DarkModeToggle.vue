<template>
  <v-tooltip :text="tooltipText" location="bottom">
    <template #activator="{ props }">
      <v-btn v-bind="props" :icon="darkModeIcon" variant="text" size="small" @click="toggleDarkMode" />
    </template>
  </v-tooltip>
</template>

<script lang="ts" setup>
import { computed } from "vue";

import { useSettingsStore } from "../stores/settings";

const settingsStore = useSettingsStore();

const darkModeIcon = computed(() => (settingsStore.settings.darkMode ? "mdi-weather-night" : "mdi-weather-sunny"));

const tooltipText = computed(() => (settingsStore.settings.darkMode ? "Switch to Light Mode" : "Switch to Dark Mode"));

function toggleDarkMode(): void {
  settingsStore.toggleDarkMode();
}
</script>
