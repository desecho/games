<template>
  <v-sheet v-if="settings.isGamesSettingsActive" class="pl-5 pt-1">
    <v-row>
      <v-col cols="12" sm="4" md="2" class="py-0">
        <v-switch
          v-model="settings.games.areActionButtonsHidden"
          label="Hide action buttons"
          hide-details
          @change="saveSettings()"
        ></v-switch>
      </v-col>
      <v-col cols="12" sm="4" md="2" class="py-0">
        <v-switch
          v-model="settings.games.areUnreleasedGamesHidden"
          label="Hide unreleased games"
          hide-details
          @change="saveSettings()"
        ></v-switch>
      </v-col>
      <v-col cols="12" sm="4" md="2" class="py-0">
        <v-switch v-model="settings.games.areDLCsHidden" label="Hide DLCs" hide-details @change="saveSettings()">
        </v-switch>
      </v-col>
    </v-row>
  </v-sheet>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapState } from "pinia";

import { useSettingsStore } from "../stores/settings";

export default defineComponent({
  name: "GamesSettings",
  computed: {
    ...mapState(useSettingsStore, ["settings"]),
  },
  methods: {
    saveSettings() {
      const { saveGamesSettings } = useSettingsStore();
      saveGamesSettings(this.settings.games);
    },
  },
});
</script>
