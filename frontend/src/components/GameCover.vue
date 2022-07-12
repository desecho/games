<template>
  <v-img v-if="game.cover" :src="game.cover" title="game.name" :alt="game.name" height="225">
    <GameCategory :name="game.category" color="white" />
  </v-img>
  <v-img v-else src="/img/image-not-found.svg" class="no-img" :title="game.name" :alt="game.name" height="225">
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
