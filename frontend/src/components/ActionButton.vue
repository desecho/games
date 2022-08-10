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

<script lang="ts" setup>
defineProps<{
  icon: string;
  title: string;
}>();
</script>
