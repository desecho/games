<template>
  <v-btn
    size="default"
    color="surface-variant"
    density="compact"
    variant="text"
    :icon="`mdi-${icon}`"
    :title="title"
    width="33"
  >
  </v-btn>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "ActionButton",
  props: {
    title: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: true,
    },
  },
});
</script>
