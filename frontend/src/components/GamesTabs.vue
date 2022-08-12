<template>
  <v-tab v-for="list in lists" :key="list.id" :value="list.key" :to="getPath(list.key)" :title="list.name">
    <v-icon>mdi-{{ list.icon }}</v-icon>
    <span v-if="!isPhone">{{ list.name }}</span>
  </v-tab>
</template>

<script lang="ts" setup>
import { useMobile } from "../composables/mobile";
import { Lists } from "../const";

const props = defineProps<{
  username?: string;
}>();

const lists = Lists;

function getPath(listKey: string): string {
  if (props.username !== undefined) {
    return `/users/${props.username}/${listKey}`;
  }
  return `/games/${listKey}`;
}

const { isPhone } = useMobile();
</script>
