<template>
  <v-card class="mb-5 mr-5" width="168" height="310">
    <GameCover :game="game" />
    <v-card-title class="game-title" :title="game.name">
      {{ game.name }}
    </v-card-title>
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButton
        v-for="list in lists"
        :key="list.id"
        :title="list.name"
        :icon="list.icon"
        @click="addToList(game.id, list.id, index)"
      />
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

import { Game } from "../types";
import { Lists } from "../const";
import { addToList } from "./common";

import ActionButton from "./ActionButton.vue";
import GameCover from "./GameCover.vue";

export default defineComponent({
  name: "GameSearchResultCard",
  components: {
    ActionButton,
    GameCover,
  },
  props: {
    game: {
      type: Object as PropType<Game>,
      required: true,
    },
    games: {
      type: Object as PropType<Game[]>,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    },
  },
  data() {
    return {
      lists: Lists,
    };
  },
  methods: {
    addToList: addToList,
  },
});
</script>

<style scoped>
.game-title {
  font-size: 1rem;
  padding-bottom: 0;
}
</style>
