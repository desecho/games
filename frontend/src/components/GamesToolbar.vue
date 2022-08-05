<template>
  <v-toolbar color="primary" height="40">
    <v-spacer></v-spacer>
    <ToolbarButton icon="cog" :active="settings.isGamesSettingsActive" @click="toggleSettings()" />
  </v-toolbar>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapState } from "pinia";

import { useSettingsStore } from "../stores/settings";

import ToolbarButton from "./ToolbarButton.vue";

export default defineComponent({
  name: "GamesToolbar",
  components: {
    ToolbarButton,
  },
  computed: {
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
