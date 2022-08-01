<template>
  <v-sheet v-if="settings.isGamesSettingsActive" class="pl-5 pt-1">
    <v-row>
      <SettingsSwitch
        v-for="settingsSwitch in switches"
        :key="settingsSwitch.name"
        type="games"
        :name="settingsSwitch.name"
        :label="settingsSwitch.label"
      />
    </v-row>
  </v-sheet>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapState } from "pinia";

import { useSettingsStore } from "../stores/settings";

import SettingsSwitch from "./SettingsSwitch.vue";

export default defineComponent({
  name: "GamesSettings",
  components: {
    SettingsSwitch,
  },
  data() {
    return {
      switches: [
        {
          name: "areActionButtonsHidden",
          label: "Hide action buttons",
        },
        {
          name: "areUnreleasedGamesHidden",
          label: "Hide unreleased games",
        },
        {
          name: "areDLCsHidden",
          label: "Hide DLCs",
        },
      ],
    };
  },
  computed: {
    ...mapState(useSettingsStore, ["settings"]),
  },
});
</script>
