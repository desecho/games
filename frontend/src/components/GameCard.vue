<template>
  <v-card class="mb-5 mr-5" width="168" height="275">
    <GameCover :game="record.game" />
    <v-card-actions>
      <v-spacer></v-spacer>
      <ActionButton
        v-for="list in lists"
        :key="list.id"
        :title="list.name"
        :icon="list.icon"
        @click="changeList(record.id, list.id, index)"
      />
      <ActionButton title="Delete Game" icon="delete" @click="deleteGame(record.id, index)" />
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";

import { RecordType } from "../types";
import { getUrl } from "../helpers";
import { ListKeys, Lists } from "../const";
import { useGamesStore } from "../stores/games";
import { requireAuthenticated } from "../helpers";
import ActionButton from "./ActionButton.vue";
import GameCover from "./GameCover.vue";

export default defineComponent({
  name: "GameCard",
  components: {
    ActionButton,
    GameCover,
  },
  props: {
    record: {
      type: Object as PropType<RecordType>,
      required: true,
    },
    index: {
      type: Number,
      required: true,
    },
    listKey: {
      type: String,
      required: true,
    },
  },
  computed: {
    lists() {
      return Lists.filter((list) => {
        return list.key != this.listKey;
      });
    },
  },
  methods: {
    changeList(recordId: number, listId: number, index: number) {
      requireAuthenticated();
      this.axios
        .put(getUrl(`records/${recordId}/change-list/`), { listId: listId })
        .then(() => {
          const { games } = useGamesStore();
          const record = games.records[index];
          record.listKey = ListKeys[listId];
        })
        .catch(() => {
          this.$toast.error("Error changing list");
        });
    },
    deleteGame(recordId: number, index: number) {
      requireAuthenticated();
      this.axios
        .delete(getUrl(`records/${recordId}/delete/`))
        .then(() => {
          const { games } = useGamesStore();
          games.records.splice(index, 1);
        })
        .catch(() => {
          this.$toast.error("Error deleting game");
        });
    },
  },
});
</script>
