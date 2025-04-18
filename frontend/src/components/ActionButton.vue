<template>
  <v-btn
    size="default"
    color="surface-variant"
    density="compact"
    variant="text"
    :icon="`mdi-${icon}`"
    :title="title"
    :disabled="disabled"
    :active="active"
    width="30"
  >
  </v-btn>
</template>

<script lang="ts" setup>
withDefaults(
  defineProps<{
    icon: string;
    title: string;
    disabled?: boolean;
    active?: boolean;
  }>(),
  {
    disabled: false,
    active: false,
  },
);
</script>
