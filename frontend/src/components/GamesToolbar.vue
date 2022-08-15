<template>
  <v-toolbar color="primary" height="40">
    <ToolbarButton icon="image-multiple" :active="settings.games.mode === 'gallery'" @click="selectGamesMode('gallery')" />
    <ToolbarButton icon="list-box" :active="settings.games.mode === 'list'" @click="selectGamesMode('list')" />
    <v-spacer></v-spacer>
    <ToolbarButton icon="cog" :active="settings.isGamesSettingsActive" @click="toggleGamesSettings()" />
  </v-toolbar>
</template>

<script lang="ts" setup>
import { useSettingsStore } from "../stores/settings";

import ToolbarButton from "./ToolbarButton.vue";

const { settings, toggleGamesSettings, selectGamesMode } = useSettingsStore();
</script>
