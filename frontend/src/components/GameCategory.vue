<template>
  <v-card-subtitle class="game-category font-weight-black text-white text-caption">
    {{ name }}
  </v-card-subtitle>
</template>

<script lang="ts" setup>
defineProps<{
  name: string;
}>();
</script>

<style scoped>
.game-category {
  position: absolute;
  bottom: 2px;
  right: 5px;
  background-color: #000000a6;
  border-radius: 5px;
}
</style>
