<template>
  <v-img :src="src" :title="game.name" :alt="game.name" height="225" :class="{ 'no-img': !game.cover }">
    <GameCategory :name="game.category" />
  </v-img>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

import { Game } from "../types";

import GameCategory from "./GameCategory.vue";

export default defineComponent({
  name: "GameCover",
  components: {
    GameCategory,
  },
  props: {
    game: {
      // eslint-disable-next-line @typescript-eslint/ban-types
      type: Object as PropType<Game>,
      required: true,
    },
  },
  computed: {
    src(): string {
      if (this.game.cover) {
        return this.game.cover;
      }
      return "/img/image-not-found.svg";
    },
  },
});
</script>

<style>
/* This needs to be unscoped for this to work */
.no-img img {
  filter: invert(45%) sepia(0%) saturate(0) hue-rotate(0deg) brightness(69%) contrast(100%);
  padding: 20px;
}
</style>
