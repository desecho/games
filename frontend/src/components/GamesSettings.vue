<template>
  <v-sheet v-if="settings.isGamesSettingsActive" class="pl-5 pt-3">
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
import { useAuthStore } from "../stores/auth";

import SettingsSwitch from "./SettingsSwitch.vue";

export default defineComponent({
  name: "GamesSettings",
  components: {
    SettingsSwitch,
  },
  data() {
    function getSwitches() {
      const switches = [];
      const { user } = useAuthStore();
      // Don't show "Hide action buttons" switch for unauthenticated users because action buttons are always
      // hidden for them.
      if (user.isLoggedIn) {
        switches.push({
          name: "areActionButtonsHidden",
          label: "Hide action buttons",
        });
      }
      switches.push(
        {
          name: "areUnreleasedGamesHidden",
          label: "Hide unreleased games",
        },
        {
          name: "areDLCsHidden",
          label: "Hide DLCs",
        }
      );
      return switches;
    }

    return {
      switches: getSwitches(),
    };
  },
  computed: {
    ...mapState(useSettingsStore, ["settings"]),
  },
});
</script>
