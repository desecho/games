<template>
  <v-card variant="flat">
    <GamesUserBar v-if="username" :username="username" />
    <GamesToolbar />
    <GamesTabs :username="username" />
    <GamesSettings :username="username" />
    <v-window v-model="tab">
      <GamesList
        v-for="list in lists"
        :key="list.id"
        :records-prop="records"
        :list-key="list.key"
        :username="username"
      />
    </v-window>
  </v-card>
</template>

<script lang="ts" setup>
import { onMounted, toRef } from "vue";

import type { RecordType } from "../types";

import { Lists } from "../const";
import { useAuthStore } from "../stores/auth";
import { useGamesStore } from "../stores/games";

import GamesList from "./GamesList.vue";
import GamesSettings from "./GamesSettings.vue";
import GamesTabs from "./GamesTabs.vue";
import GamesToolbar from "./GamesToolbar.vue";
import GamesUserBar from "./GamesUserBar.vue";

const { user } = useAuthStore();

defineProps<{
  records: RecordType[];
  username?: string;
}>();

const lists = Lists;
const gamesStore = useGamesStore();
const tab = toRef(gamesStore, "tab");

// We are loading games here because games need to be loaded even if it is the profile page
onMounted(async () => {
  if (user.isLoggedIn) {
    const { loadGames } = useGamesStore();
    await loadGames();
  }
});
</script>
