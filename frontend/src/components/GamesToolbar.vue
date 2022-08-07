<template>
  <v-toolbar color="primary" height="40">
    <v-spacer></v-spacer>
    <ToolbarButton icon="cog" :active="settings.isGamesSettingsActive" @click="toggleGamesSettings()" />
  </v-toolbar>
</template>

<script lang="ts" setup>
import { useSettingsStore } from "../stores/settings";

import ToolbarButton from "./ToolbarButton.vue";

const { settings, toggleGamesSettings } = useSettingsStore();
</script>
