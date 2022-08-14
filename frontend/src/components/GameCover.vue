<template>
  <v-img :src="src" :title="game.name" :alt="game.name" height="225" :class="{ 'no-img': !game.cover }">
    <GameCategory v-if="game.category != 'Main Game'" :name="game.category" />
  </v-img>
</template>

<script lang="ts" setup>
import { computed } from "vue";

import type { Game } from "../types";

import GameCategory from "./GameCategory.vue";

const props = defineProps<{
  game: Game;
}>();

const src = computed(() => {
  if (props.game.cover !== null) {
    return props.game.cover;
  }
  return "/img/image-not-found.svg";
});
</script>

<style>
/* This needs to be unscoped for this to work */
.no-img img {
  filter: invert(45%) sepia(0%) saturate(0) hue-rotate(0deg) brightness(69%) contrast(100%);
  padding: 20px;
}
</style>
