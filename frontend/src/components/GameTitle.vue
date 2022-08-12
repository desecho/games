<template>
  <v-card-title class="game-title" :title="game">
    {{ game }}
  </v-card-title>
</template>

<script lang="ts" setup>
defineProps<{
  game: string;
}>();
</script>

<style scoped>
.game-title {
  font-size: 1rem;
  padding-bottom: 0;
}
</style>
