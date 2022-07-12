<template>
  <v-card class="mb-5 mr-5" width="168" :height="height">
    <GameCover :game="record.game" />
    <v-card-actions v-if="areActionsVisible">
      <v-spacer></v-spacer>
      <ActionButton
        v-for="list in lists"
        :key="list.id"
        :title="list.name"
        :icon="list.icon"
        @click="action(list.id)"
      />
      <ActionButton v-if="!isProfile" title="Delete Game" icon="delete" @click="deleteGame(record.id, index)" />
    </v-card-actions>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { mapWritableState } from "pinia";

import { RecordType } from "../types";
import { getUrl } from "../helpers";
import { ListKeys, Lists } from "../const";
import { useGamesStore } from "../stores/games";
import { useAuthStore } from "../stores/auth";
import { requireAuthenticated } from "../helpers";
import { addToList } from "./common";
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
    isProfile: {
      type: Boolean,
      required: false,
      default: false,
    },
    isOwnProfile: {
      type: Boolean,
      required: false,
      default: false,
    },
  },
  data() {
    return {
      action: (listId: number) => {
        if (this.isProfile) {
          this.addToList(this.record.game.id, listId, this.index, true);
        } else {
          this.changeList(this.record.id, listId, this.index);
        }
      },
    };
  },
  computed: {
    lists() {
      return Lists.filter((list) => {
        return list.key != this.listKey;
      });
    },
    isLoggedIn() {
      const { user } = useAuthStore();
      return user.isLoggedIn;
    },
    height() {
      return this.areActionsVisible ? 275 : 224;
    },
    areActionsVisible() {
      return this.isLoggedIn && !this.isOwnProfile;
    },
    ...mapWritableState(useGamesStore, ["records"]),
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
    addToList: addToList,
  },
});
</script>
