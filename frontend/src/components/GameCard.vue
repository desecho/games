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

<script lang="ts" setup>
import { AxiosError, AxiosStatic } from "axios";
import { computed, inject, toRef } from "vue";

import { useAddToList } from "../composables/addToList";
import { ListIDs, ListKeys, Lists } from "../const";
import { getUrl, requireAuthenticated } from "../helpers";
import { useAuthStore } from "../stores/auth";
import { useGamesStore } from "../stores/games";
import { useSettingsStore } from "../stores/settings";
import { $toast } from "../toast";
import { Game, List, RecordType } from "../types";

import ActionButton from "./ActionButton.vue";
import GameCover from "./GameCover.vue";

// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const axios: AxiosStatic = inject("axios")!;

interface Props {
  record: RecordType;
  index: number;
  listKey: string;
  username?: string;
}

const props = defineProps<Props>();

const action = (listId: number) => {
  if (props.username) {
    addToList(props.record.game.id, listId);
  } else {
    changeList(props.record.id, listId, props.index);
  }
};

const { user } = useAuthStore();
const isLoggedIn = user.isLoggedIn;
const gamesStore = useGamesStore();
const records = toRef(gamesStore, "records");
const settingsStore = useSettingsStore();
const settings = toRef(settingsStore, "settings");
const isOwnProfile = computed(() => {
  return props.username && props.username == user.username;
});
const areActionsVisible = computed(() => {
  return isLoggedIn && !isOwnProfile.value && !settings.value.games.areActionButtonsHidden;
});
const height = computed(() => {
  return areActionsVisible.value ? 275 : 224;
});

function changeList(recordId: number, listId: number, index: number) {
  requireAuthenticated();
  axios
    .put(getUrl(`records/${recordId}/change-list/`), { listId: listId })
    .then(() => {
      records.value[index].listKey = ListKeys[listId];
    })
    .catch((error: AxiosError) => {
      console.log(error);
      $toast.error("Error changing list");
    });
}

function deleteGame(recordId: number, index: number) {
  requireAuthenticated();
  axios
    .delete(getUrl(`records/${recordId}/delete/`))
    .then(() => {
      records.value.splice(index, 1);
    })
    .catch((error) => {
      console.log(error);
      $toast.error("Error deleting game");
    });
}

function getLists(game: Game): List[] {
  const lists = Lists.filter((list) => {
    return list.key != props.listKey;
  });
  // Don't show action buttons for lists other than "Want to Play" if the game has not been released yet.
  return lists.filter((list) => {
    if (list.id == ListIDs.WantToPlay) {
      return true;
    }
    return game.isReleased;
  });
}

const { addToList } = useAddToList();
</script>
