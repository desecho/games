<template>
  <v-col cols="12" sm="4" md="3" class="py-0 settings-switches">
    <v-switch v-model="value" :label="label" color="primary" hide-details @change="saveSettings()"></v-switch>
  </v-col>
</template>

<script lang="ts" setup>
import { onMounted, ref, toRef } from "vue";

import { useSettingsStore } from "../stores/settings";

interface Props {
  type: string;
  name: string;
  label: string;
}

const props = defineProps<Props>();

const value = ref(false);
const settingsStore = useSettingsStore();
const settings = toRef(settingsStore, "settings");

function saveSettings(): void {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access
  settings.value[props.type][props.name] = value.value;
  settingsStore.persistSettings();
}

onMounted(() => {
  // eslint-disable-next-line @typescript-eslint/no-unsafe-member-access,@typescript-eslint/no-unsafe-assignment
  value.value = settings.value[props.type][props.name];
});
</script>

<style>
/* This needs to be unscoped for this to work */
.settings-switches div.v-selection-control {
  height: 62px;
}
</style>
