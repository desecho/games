<template>
  <v-card variant="flat" color="deep-purple-accent-4">
    <slot></slot>
    <v-toolbar color="deep-purple-accent-4" height="40">
      <v-spacer></v-spacer>
      <v-btn icon>
        <v-icon :color="settingsIconColor" @click="toggleSettings()">mdi-cog</v-icon>
      </v-btn>
    </v-toolbar>

    <v-tabs v-model="tab" background-color="deep-purple-accent-4" centered stacked>
      <v-tab v-for="list in lists" :key="list.id" :value="list.key" :to="getPath(list.key)" :title="list.name">
        <v-icon>mdi-{{ list.icon }}</v-icon>
        <span v-if="!isPhone">{{ list.name }}</span>
      </v-tab>
    </v-tabs>
    <v-sheet v-if="isSettingsActive" class="pl-5">
      <v-row>
        <v-col cols="12" sm="4" md="2">
          <v-switch
            v-model="settings.areActionButtonsHidden"
            label="Hide action buttons"
            hide-details
            @change="saveSettings()"
          ></v-switch>
        </v-col>
        <v-col cols="12" sm="4" md="2">
          <v-switch
            v-model="settings.areUnreleasedGamesHidden"
            label="Hide unreleased games"
            hide-details
            @change="saveSettings()"
          ></v-switch>
        </v-col>
      </v-row>
    </v-sheet>
    <v-window v-model="tab">
      <ListWindowItem
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

import { mobileMixin } from "../mixins/mobile";
import { Lists } from "../const";
import ListWindowItem from "../components/ListWindowItem.vue";
import { RecordType } from "../types";
import { useSettingsStore } from "../stores/settings";

export default defineComponent({
  name: "GamesListView",
  components: {
    ListWindowItem,
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
    const { settings } = useSettingsStore();
    return {
      lists: Lists,
      tab: "want-to-play",
      isSettingsActive: false,
      settings: settings.games,
      areActionButtonsHidden: false,
      areUnreleasedGamesHidden: false,
    };
  },
  computed: {
    settingsIconColor(): string {
      if (this.isSettingsActive) {
        return "grey";
      }
      return "white";
    },
  },
  methods: {
    getPath(listKey: string): string {
      if (this.username) {
        return `/users/${this.username}/${listKey}`;
      }
      return `/games/${listKey}`;
    },
    toggleSettings() {
      this.isSettingsActive = !this.isSettingsActive;
    },
    saveSettings() {
      const { saveGamesSettings } = useSettingsStore();
      saveGamesSettings(this.settings);
    },
  },
});
</script>
