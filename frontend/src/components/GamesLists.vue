<template>
  <v-card variant="flat" color="primary">
    <slot></slot>
    <GamesToolbar />
    <v-tabs v-model="tab" background-color="primary" centered stacked>
      <v-tab v-for="list in lists" :key="list.id" :value="list.key" :to="getPath(list.key)" :title="list.name">
        <v-icon>mdi-{{ list.icon }}</v-icon>
        <span v-if="!isPhone">{{ list.name }}</span>
      </v-tab>
    </v-tabs>
    <GamesSettings />
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
import { ref } from "vue";

import type { RecordType } from "../types";

import { useMobile } from "../composables/mobile";
import { Lists } from "../const";


import GamesList from "./GamesList.vue";
import GamesSettings from "./GamesSettings.vue";
import GamesToolbar from "./GamesToolbar.vue";


interface Props {
  records: RecordType[];
  username?: string;
}

const props = defineProps<Props>();

const lists = Lists;
const tab = ref("want-to-play");

function getPath(listKey: string): string {
  if (props.username) {
    return `/users/${props.username}/${listKey}`;
  }
  return `/games/${listKey}`;
}

const { isPhone } = useMobile();
</script>
