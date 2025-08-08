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
        v-model:records="records"
        :list-key="list.key"
        :username="username"
      />
    </v-window>
  </v-card>
</template>

<script lang="ts" setup>
import { defineModel, onMounted, toRef } from "vue";

import type { RecordType } from "../types";
import type { AxiosError } from "axios";

import { LISTS } from "../const";
import { useAuthStore } from "../stores/auth";
import { useGamesStore } from "../stores/games";
import { $toast } from "../toast";

import GamesList from "./GamesList.vue";
import GamesSettings from "./GamesSettings.vue";
import GamesTabs from "./GamesTabs.vue";
import GamesToolbar from "./GamesToolbar.vue";
import GamesUserBar from "./GamesUserBar.vue";

const { user } = useAuthStore();

defineProps<{
  username?: string;
}>();

const lists = LISTS;
const gamesStore = useGamesStore();
const tab = toRef(gamesStore, "tab");

// Two-way binding for records from parent (required)
const records = defineModel<RecordType[]>("records", { required: true });

// We are loading games here because games need to be loaded even if it is the profile page
onMounted(() => {
  if (user.isLoggedIn) {
    const { loadGames } = useGamesStore();
    loadGames()
      .then(() => {
        console.log("Games loaded");
      })
      .catch((error: AxiosError) => {
        console.log(error);
        $toast.error("Error loading games");
      });
  }
});
</script>
