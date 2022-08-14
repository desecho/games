<template>
  <GamesLists :records="records" />
</template>

<script lang="ts" setup>
import { toRef } from "vue";

import type { ListKey } from "../types";

import GamesLists from "../components/GamesLists.vue";
import { DefaultList } from "../const";
import { useGamesStore } from "../stores/games";

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
</script>
