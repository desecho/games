<template>
  <v-card class="mb-5 mr-5" width="168" :height="height">
    <GameCover :game="record.game" />
    <v-card-actions v-if="areActionsVisible">
      <v-spacer></v-spacer>
      <ActionButton
        v-for="list in getLists(record.game)"
        :key="list.id"
        :title="list.name"
        :icon="list.icon"
        @click="action(list.id)"
      />
      <ActionButton v-if="!username" title="Delete Game" icon="delete" @click="deleteGame(record.id, index)" />
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { mapWritableState, mapState } from "pinia";

import { RecordType, Game, List } from "../types";
import { getUrl, requireAuthenticated } from "../helpers";
import { ListKeys, Lists, ListIDs } from "../const";
import { useGamesStore } from "../stores/games";
import { useSettingsStore } from "../stores/settings";
import { useAuthStore } from "../stores/auth";
import { addToListMixin } from "../mixins/addToList";

import ActionButton from "./ActionButton.vue";
import GameCover from "./GameCover.vue";

export default defineComponent({
  name: "GameCard",
  components: {
    ActionButton,
    GameCover,
  },
  mixins: [addToListMixin],
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
    username: {
      type: String,
      required: false,
      default: null,
    },
  },
  data() {
    return {
      action: (listId: number) => {
        if (this.username) {
          this.addToList(this.record.game.id, listId, this.index, true);
        } else {
          this.changeList(this.record.id, listId, this.index);
        }
      },
    };
  },
  computed: {
    isLoggedIn() {
      const { user } = useAuthStore();
      return user.isLoggedIn;
    },
    height() {
      return this.areActionsVisible ? 275 : 224;
    },
    isOwnProfile() {
      const { user } = useAuthStore();
      return this.username && this.username == user.username;
    },
    areActionsVisible() {
      return this.isLoggedIn && !this.isOwnProfile && !this.settings.games.areActionButtonsHidden;
    },
    ...mapWritableState(useGamesStore, ["records"]),
    ...mapState(useSettingsStore, ["settings"]),
  },
  methods: {
    changeList(recordId: number, listId: number, index: number) {
      requireAuthenticated();
      this.axios
        .put(getUrl(`records/${recordId}/change-list/`), { listId: listId })
        .then(() => {
          this.records[index].listKey = ListKeys[listId];
        })
        .catch((error) => {
          console.log(error);
          this.$toast.error("Error changing list");
        });
    },
    deleteGame(recordId: number, index: number) {
      requireAuthenticated();
      this.axios
        .delete(getUrl(`records/${recordId}/delete/`))
        .then(() => {
          this.records.splice(index, 1);
        })
        .catch((error) => {
          console.log(error);
          this.$toast.error("Error deleting game");
        });
    },
    getLists(game: Game): List[] {
      const lists = Lists.filter((list) => {
        return list.key != this.listKey;
      });
      // Don't show action buttons for lists other than "Want to Play" if the game has not been released yet.
      return lists.filter((list) => {
        if (list.id == ListIDs.WantToPlay) {
          return true;
        }
        return game.isReleased;
      });
    },
  },
});
</script>
