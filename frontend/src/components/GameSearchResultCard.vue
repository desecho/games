<template>
  <v-card class="mb-5 mr-5" width="168" height="310">
    <GameCover :game="game" />
    <GameTitle :game="game.name" />
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButton
        v-for="list in lists"
        :key="list.id"
        :title="list.name"
        :icon="list.icon"
        @click="$emit('addToList', list.id)"
      />
    </v-card-actions>
  </v-card>
</template>

<script lang="ts" setup>
import type { Game } from "../types";

import { ListIds, Lists } from "../const";

import ActionButton from "./ActionButton.vue";
import GameCover from "./GameCover.vue";
import GameTitle from "./GameTitle.vue";

const props = defineProps<{
  game: Game;
}>();

defineEmits<(e: "addToList", listId: number) => void>();

// Don't show action buttons for lists other than "Want to Play" if the game has not been released yet
const lists = Lists.filter((list) => {
  if (list.id === ListIds.WantToPlay) {
    return true;
  }
  return props.game.isReleased;
});
</script>
