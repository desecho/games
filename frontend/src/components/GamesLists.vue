<template>
  <v-card variant="flat" color="deep-purple-accent-4">
    <slot></slot>
    <GamesToolbar />
    <v-tabs v-model="tab" background-color="deep-purple-accent-4" centered stacked>
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

<script lang="ts">
import { defineComponent, PropType } from "vue";

import { Lists } from "../const";
import { RecordType } from "../types";
import { mobileMixin } from "../mixins/mobile";

import GamesList from "./GamesList.vue";
import GamesSettings from "./GamesSettings.vue";
import GamesToolbar from "./GamesToolbar.vue";

export default defineComponent({
  name: "GamesListView",
  components: {
    GamesList,
    GamesSettings,
    GamesToolbar,
  },
  mixins: [mobileMixin],
  props: {
    records: {
      type: Object as PropType<RecordType[]>,
      required: true,
    },
    username: {
      type: String,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      lists: Lists,
      tab: "want-to-play",
      isSettingsActive: false,
    };
  },
  methods: {
    getPath(listKey: string): string {
      if (this.username) {
        return `/users/${this.username}/${listKey}`;
      }
      return `/games/${listKey}`;
    },
  },
});
</script>
