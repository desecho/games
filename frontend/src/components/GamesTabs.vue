<template>
  <v-tabs v-model="tab" bg-color="primary" align-tabs="center" stacked>
    <v-tab v-for="list in lists" :key="list.id" :value="list.key" :to="getPath(list.key)" :title="list.name">
      <v-icon>mdi-{{ list.icon }}</v-icon>
      <span v-if="!isPhone">{{ list.name }}</span>
    </v-tab>
  </v-tabs>
</template>

<script lang="ts" setup>
import { toRef } from "vue";

import type { ListKey } from "../types";

import { useMobile } from "../composables/mobile";
import { LISTS } from "../const";
import { useGamesStore } from "../stores/games";

const props = defineProps<{
  username?: string;
}>();

const lists = LISTS;
const gamesStore = useGamesStore();
const tab = toRef(gamesStore, "tab");
const isProfile = props.username !== undefined;
const { isPhone } = useMobile();

function getPath(listKey: ListKey): string {
  if (isProfile) {
    return `/users/${props.username}/${listKey}`;
  }
  return `/games/${listKey}`;
}
</script>
