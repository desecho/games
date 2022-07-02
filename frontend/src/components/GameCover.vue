<template>
  <v-img
    v-if="game.cover"
    class="mx-auto mt-3"
    :src="game.cover"
    :title="game.name"
    :alt="game.name"
    width="200"
    height="225"
  >
    <GameCategory :name="game.category" color="white" />
  </v-img>
  <v-img
    v-else
    class="mx-auto mt-3"
    src="img/image-not-found.svg"
    :title="game.name"
    :alt="game.name"
    width="100"
    height="225"
  >
    <GameCategory :name="game.category" />
  </v-img>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

import { GameSearchResult, Game } from "../types";
import GameCategory from "./GameCategory.vue";

export default defineComponent({
  name: "GameCover",
  components: {
    GameCategory,
  },
  props: {
    game: {
      // eslint-disable-next-line @typescript-eslint/ban-types
      type: Object as PropType<GameSearchResult> | Object as PropType<Game>,
      required: true,
    },
  },
});
</script>
