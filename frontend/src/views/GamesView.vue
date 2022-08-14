<template>
  <GamesLists :records="records" />
</template>

<script lang="ts" setup>
import { onMounted, toRef } from "vue";

import type { ListKey } from "../types";

import GamesLists from "../components/GamesLists.vue";
import { DefaultList } from "../const";
import { useGamesStore } from "../stores/games";
import { $toast } from "../toast";

withDefaults(
  defineProps<{
    listKey?: ListKey;
  }>(),
  {
    listKey: DefaultList,
  }
);

const gamesStore = useGamesStore();
const records = toRef(gamesStore, "records");

onMounted(() => {
  const { loadGames } = useGamesStore();
  loadGames().catch((error) => {
    console.log(error);
    $toast.error("Error loading games");
  });
});
</script>
