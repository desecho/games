<template>
  <v-card variant="flat" color="primary">
    <GamesUserBar v-if="username" :username="username" />
    <GamesToolbar />
    <v-tabs v-model="tab" background-color="primary" centered stacked>
      <GamesTabs :username="username" />
    </v-tabs>
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
import { ref } from "vue";

import type { RecordType } from "../types";

import { Lists } from "../const";

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
const tab = ref("want-to-play");
</script>
