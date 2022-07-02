<template>
  <v-btn size="small" color="surface-variant" variant="text" :icon="'mdi-' + icon" :title="title"> </v-btn>
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
