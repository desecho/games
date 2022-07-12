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

import { GameSearchResult } from "../types";
import { getUrl, requireAuthenticated } from "../helpers";
import { Lists } from "../const";
import { useGamesStore } from "../stores/games";
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
      type: Object as PropType<GameSearchResult>,
      required: true,
    },
    games: {
      type: Object as PropType<GameSearchResult[]>,
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
    addToList(gameId: number, listId: number, index: number) {
      requireAuthenticated();
      this.axios
        .post(getUrl("records/add/"), { listId: listId, gameId: gameId })
        .then(async () => {
          // eslint-disable-next-line vue/no-mutating-props
          this.games.splice(index, 1);
          const { reloadGames } = useGamesStore();
          await reloadGames().catch(() => {
            this.$toast.error("Error reloading games");
          });
        })
        .catch(() => {
          this.$toast.error("Error adding a game");
        });
    },
  },
});
</script>

<style scoped>
.game-title {
  font-size: 1rem;
  padding-bottom: 0;
}
</style>
