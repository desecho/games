<template>
  <v-card-subtitle v-if="name != 'Main Game'" class="game-category font-weight-black text-white text-caption">
    {{ name }}
  </v-card-subtitle>
</template>

<script lang="ts" setup>
interface Props {
  name: string;
}
defineProps<Props>();
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
