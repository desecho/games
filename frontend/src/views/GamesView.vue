<template>
  <GamesLists :records="records" />
</template>

<script lang="ts" setup>
import { onMounted, toRef } from "vue";

import GamesLists from "../components/GamesLists.vue";
import { useGamesStore } from "../stores/games";
import { $toast } from "../toast";



interface Props {
  listKey?: string;
}
withDefaults(defineProps<Props>(), {
  listKey: "want-to-play",
});

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
