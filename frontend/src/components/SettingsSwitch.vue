<template>
  <v-col cols="12" sm="4" md="3" class="py-0 settings-switches">
    <v-switch v-model="value" :label="label" color="primary" hide-details @change="saveSettings()"></v-switch>
  </v-col>
</template>

<script lang="ts" setup>
import { onMounted, ref, toRef } from "vue";

import { useSettingsStore } from "../stores/settings";

const props = defineProps<{
  type: string;
  name: string;
  label: string;
}>();

const value = ref(false);
const settingsStore = useSettingsStore();
const settings = toRef(settingsStore, "settings");

// eslint-disable-next-line @typescript-eslint/no-explicit-any
type AnyRecord = Record<string, Record<string, any>>;

function getSection(): Record<string, boolean> {
  return (settings.value as unknown as AnyRecord)[props.type];
}

function saveSettings(): void {
  getSection()[props.name] = value.value;
}

onMounted(() => {
  value.value = getSection()[props.name];
});
</script>

<style>
/* This needs to be unscoped for this to work */
.settings-switches div.v-selection-control {
  height: 62px;
}
</style>
