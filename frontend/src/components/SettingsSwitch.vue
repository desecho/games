<template>
  <v-col cols="12" sm="4" md="3" class="py-0">
    <v-switch v-model="value" :label="label" color="primary" hide-details @change="saveSettings()"></v-switch>
  </v-col>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapWritableState } from "pinia";

import { useSettingsStore } from "../stores/settings";

export default defineComponent({
  name: "SettingsSwitch",
  props: {
    type: {
      type: String,
      required: true,
    },
    name: {
      type: String,
      required: true,
    },
    label: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      value: false,
    };
  },
  computed: {
    ...mapWritableState(useSettingsStore, ["settings"]),
  },
  mounted() {
    this.value = this.settings[this.type][this.name];
  },
  methods: {
    saveSettings() {
      this.settings[this.type][this.name] = this.value;
      const { persistSettings } = useSettingsStore();
      persistSettings();
    },
  },
});
</script>
