<template>
  <v-btn icon>
    <v-icon :color="color">mdi-{{ icon }}</v-icon>
  </v-btn>
</template>

<script lang="ts" setup>
import { computed } from "vue";

interface Props {
  active?: boolean;
  icon: string;
}
const props = withDefaults(defineProps<Props>(), {
  active: false,
});

const color = computed(() => (props.active ? "grey" : "white"));
</script>
