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
        :disabled="isGameinGames"
        :active="isGameinGames"
        @click="action(list.id)"
      />
      <ActionButton v-if="!isProfile" title="Delete Game" icon="delete" @click="deleteGame(record.id)" />
    </v-card-actions>
  </v-card>
</template>

<script lang="ts" setup>
import axios from "axios";
import { computed, toRef } from "vue";

import type { List, ListKey, RecordType } from "../types";
import type { GameIdsWithListKeys } from "./types";
import type { AxiosError } from "axios";

import { useAddToList } from "../composables/addToList";
import { ListIds, ListKeys, Lists } from "../const";
import { getUrl, requireAuthenticated } from "../helpers";
import { useAuthStore } from "../stores/auth";
import { useGamesStore } from "../stores/games";
import { useSettingsStore } from "../stores/settings";
import { $toast } from "../toast";

import ActionButton from "./ActionButton.vue";
import GameCover from "./GameCover.vue";

const props = defineProps<{
  record: RecordType;
  index: number;
  listKey: ListKey;
  username?: string;
}>();

const { user } = useAuthStore();
const isLoggedIn = user.isLoggedIn;
const gamesStore = useGamesStore();
const records = toRef(gamesStore, "records");
const gameIdsWithListKeys = computed(() => {
  const games: GameIdsWithListKeys = {};
  for (const record of records.value) {
    games[record.game.id] = record.listKey;
  }
  return games;
});
const settingsStore = useSettingsStore();
const settings = toRef(settingsStore, "settings");
const isProfile = props.username !== undefined;
const isOwnProfile = isProfile && props.username === user.username;
const areActionsVisible = computed(() => {
  return isLoggedIn && !isOwnProfile && !settings.value.games.areActionButtonsHidden;
});
const height = computed(() => {
  return areActionsVisible.value ? 275 : 224;
});

function changeList(recordId: number, listId: number): void {
  requireAuthenticated();
  axios
    .put(getUrl(`records/${recordId}/change-list/`), { listId })
    .then(() => {
      console.log("Game list changed");
      records.value[props.index].listKey = ListKeys[listId];
    })
    .catch((error: AxiosError) => {
      console.log(error);
      $toast.error("Error changing list");
    });
}

function deleteGame(recordId: number): void {
  requireAuthenticated();
  axios
    .delete(getUrl(`records/${recordId}/delete/`))
    .then(() => {
      console.log("Game deleted");
      records.value.splice(props.index, 1);
    })
    .catch((error) => {
      console.log(error);
      $toast.error("Error deleting game");
    });
}

function getIsGameinGames(): boolean {
  if (isProfile) {
    return props.record.game.id in gameIdsWithListKeys.value;
  }
  return false;
}

const isGameinGames = getIsGameinGames();

function getListsForActions(): List[] {
  let lists = Lists;
  const game = props.record.game;
  if (isGameinGames) {
    lists = lists.filter((list) => list.key === gameIdsWithListKeys.value[game.id]);
  }
  if (!isProfile) {
    // Don't show action buttons for current list
    lists = lists.filter((list) => {
      return list.key !== props.listKey;
    });
  }
  // Don't show action buttons for lists other than "Want to Play" if the game has not been released yet
  return lists.filter((list) => {
    if (list.id === ListIds.WantToPlay) {
      return true;
    }
    return game.isReleased;
  });
}

const { addToList } = useAddToList();
const lists = getListsForActions();

function action(listId: number): void {
  if (isProfile) {
    addToList(props.record.game.id, listId).catch((error: AxiosError) => {
      console.log(error);
      $toast.error("Error adding a game");
    });
  } else {
    changeList(props.record.id, listId);
  }
}
</script>
