<template>
  <v-btn icon>
    <v-icon :color="color">mdi-{{ icon }}</v-icon>
  </v-btn>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "ToolbarButton",
  props: {
    active: {
      type: Boolean,
      default: false,
    },
    icon: {
      type: String,
      required: true,
    },
  },
  computed: {
    color(): string {
      if (this.active) {
        return "grey";
      }
      return "white";
    },
  },
});
</script>
