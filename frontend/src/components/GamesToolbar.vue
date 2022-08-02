<template>
  <v-toolbar color="primary" height="40">
    <v-spacer></v-spacer>
    <v-btn icon>
      <v-icon :color="settingsIconColor" @click="toggleSettings()">mdi-cog</v-icon>
    </v-btn>
  </v-toolbar>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapState } from "pinia";

import { useSettingsStore } from "../stores/settings";

export default defineComponent({
  name: "GamesToolbar",
  computed: {
    settingsIconColor(): string {
      if (this.settings.isGamesSettingsActive) {
        return "grey";
      }
      return "white";
    },
    ...mapState(useSettingsStore, ["settings"]),
  },
  methods: {
    toggleSettings() {
      const { toggleGamesSettings } = useSettingsStore();
      toggleGamesSettings();
    },
  },
});
</script>
