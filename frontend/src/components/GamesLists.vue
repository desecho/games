<template>
  <v-card variant="flat">
    <GamesUserBar v-if="username" :username="username" />
    <GamesToolbar />
    <GamesTabs :username="username" />
    <GamesSettings :username="username" />
    <GamesList
      v-for="list in lists"
      :key="list.id"
      :records-prop="records"
      :list-key="list.key"
      :username="username"
    />
  </v-card>
</template>

<script lang="ts" setup>
import { onMounted } from "vue";

import type { RecordType } from "../types";

import { Lists } from "../const";
import { useGamesStore } from "../stores/games";

import GamesList from "./GamesList.vue";
import GamesSettings from "./GamesSettings.vue";
import GamesTabs from "./GamesTabs.vue";
import GamesToolbar from "./GamesToolbar.vue";
import GamesUserBar from "./GamesUserBar.vue";

defineProps<{
  records: RecordType[];
  username?: string;
}>();

const lists = Lists;

onMounted(async () => {
  const { loadGames } = useGamesStore();
  await loadGames();
});
</script>
