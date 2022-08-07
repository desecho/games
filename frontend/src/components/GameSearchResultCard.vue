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
        @click="addToList(game.id, list.id, index, gamesRef)"
      />
    </v-card-actions>
  </v-card>
</template>

<script lang="ts" setup>
import { computed, toRef } from "vue";
import { Game } from "../types";
import { Lists, ListIDs } from "../const";
import { useAddToList } from "../composables/addToList";

import ActionButton from "./ActionButton.vue";
import GameCover from "./GameCover.vue";

interface Props {
  game: Game;
  games: Game[];
  index: number;
}

const props = defineProps<Props>();

const lists = computed(() => {
  // Don't show action buttons for lists other than "Want to Play" if the game has not been released yet.
  return Lists.filter((list) => {
    if (list.id == ListIDs.WantToPlay) {
      return true;
    }
    return props.game.isReleased;
  });
});
const gamesRef = computed(() => {
  return toRef(props, "games");
});

const { addToList } = useAddToList();
</script>

<style scoped>
.game-title {
  font-size: 1rem;
  padding-bottom: 0;
}
</style>
