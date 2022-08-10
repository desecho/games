<template>
  <v-btn icon>
    <v-icon :color="color">mdi-{{ icon }}</v-icon>
  </v-btn>
</template>

<script lang="ts" setup>
import { computed } from "vue";

const props = withDefaults(
  defineProps<{
    active?: boolean;
    icon: string;
  }>(),
  {
    active: false,
  }
);

const color = computed(() => (props.active ? "grey" : "white"));
</script>
