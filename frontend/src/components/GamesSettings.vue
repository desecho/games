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

<script lang="ts" setup>
import { toRef } from "vue";

import type { Switch } from "./types";

import { useAuthStore } from "../stores/auth";
import { useSettingsStore } from "../stores/settings";

import SettingsSwitch from "./SettingsSwitch.vue";

const props = defineProps<{
  username?: string;
}>();

const { user } = useAuthStore();
const isProfile = props.username !== undefined;
const isOwnProfile = isProfile && props.username === user.username;

function getSwitches(): Switch[] {
  const switches: Switch[] = [];
  /* Don't show "Hide action buttons" switch for unauthenticated users because action buttons are always
     hidden for them. Same if the user is on their own profile page. */
  if (user.isLoggedIn && !isOwnProfile) {
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
    },
  );
  return switches;
}

const settingsStore = useSettingsStore();
const settings = toRef(settingsStore, "settings");
const switches = getSwitches();
</script>
