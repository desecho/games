<template>
  <GamesLists v-model:records="records" />
</template>

<script lang="ts" setup>
import { toRef } from "vue";

import type { ListKey } from "../types";

import GamesLists from "../components/GamesLists.vue";
import { DEFAULT_LIST } from "../const";
import { useGamesStore } from "../stores/games";

withDefaults(
  defineProps<{
    listKey?: ListKey;
  }>(),
  {
    listKey: DEFAULT_LIST,
  },
);

const gamesStore = useGamesStore();
const records = toRef(gamesStore, "records");
</script>
