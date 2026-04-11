<template>
  <v-card class="mb-5 mr-5" width="168" :height="height">
    <div class="game-card-poster">
      <GameCover :game="record.game" />
      <div v-if="isRatingVisible" class="game-card-rating" @click.stop @mousedown.stop @touchstart.stop>
        <v-rating
          :model-value="rating"
          :readonly="!isRatingEditable"
          :clearable="isRatingEditable"
          :hover="isRatingEditable"
          :title="ratingTitle"
          color="amber-darken-2"
          active-color="amber-darken-2"
          density="compact"
          size="x-small"
          length="5"
          :ripple="false"
          @update:model-value="updateRating"
        />
      </div>
    </div>
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
import { computed, ref, toRef, watch } from "vue";

import type { ListKey, RecordType } from "../types";
import type { GameIdsWithListKeys } from "./types";
import type { AxiosError } from "axios";

import { useAddToList } from "../composables/addToList";
import { LISTS } from "../const";
import { getUrl, requireAuthenticated } from "../helpers";
import { useAuthStore } from "../stores/auth";
import { useGamesStore } from "../stores/games";
import { useSettingsStore } from "../stores/settings";
import { $toast } from "../toast";
import { LIST_IDS } from "../types";

import ActionButton from "./ActionButton.vue";
import GameCover from "./GameCover.vue";

const props = defineProps<{
  record: RecordType;
  index: number;
  listKey: ListKey;
  username?: string;
}>();
const emit = defineEmits<{
  updateRating: [recordId: number, rating: number];
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
const isRatingEditable = computed(() => {
  return isLoggedIn && (!isProfile || isOwnProfile);
});
const isRatingVisible = computed(() => {
  return settings.value.games.areRatingsHidden !== true;
});
const rating = ref(props.record.rating);
const ratingTitle = computed(() => {
  if (rating.value === 0) {
    return "Unrated";
  }
  return `${rating.value} out of 5`;
});
const height = computed(() => {
  return areActionsVisible.value ? 275 : 224;
});
const isGameinGames = computed(() => {
  if (isProfile) {
    return props.record.game.id in gameIdsWithListKeys.value;
  }
  return false;
});
const lists = computed(() => {
  let listsFiltered = LISTS;
  const game = props.record.game;
  if (isGameinGames.value) {
    listsFiltered = listsFiltered.filter((list) => list.key === gameIdsWithListKeys.value[game.id]);
  }
  if (!isProfile) {
    // Don't show action buttons for current list
    listsFiltered = listsFiltered.filter((list) => {
      return list.key !== props.listKey;
    });
  }
  // Don't show action buttons for lists other than "Want to Play" if the game has not been released yet
  return listsFiltered.filter((list) => {
    if (list.id === LIST_IDS.WantToPlay) {
      return true;
    }
    return game.isReleased;
  });
});

function changeList(recordId: number, listId: number): void {
  requireAuthenticated();
  axios
    .put(getUrl(`records/${recordId}/change-list/`), { listId })
    .then(() => {
      console.log("Game list changed");
      gamesStore
        .reloadGames()
        .then(() => {
          console.log("Games reloaded");
        })
        .catch((error: AxiosError) => {
          console.log(error);
          $toast.error("Error reloading games");
        });
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

function updateRating(value: number | string): void {
  if (!isRatingEditable.value) {
    return;
  }

  const ratingValue = Number(value);
  if (!Number.isInteger(ratingValue) || ratingValue < 0 || ratingValue > 5) {
    return;
  }

  const previousRating = rating.value;
  rating.value = ratingValue;
  requireAuthenticated();
  axios
    .put(getUrl(`records/${props.record.id}/rating/`), { rating: ratingValue })
    .then(() => {
      emit("updateRating", props.record.id, ratingValue);
    })
    .catch((error: AxiosError) => {
      console.log(error);
      rating.value = previousRating;
      $toast.error("Error updating rating");
    });
}

watch(
  () => props.record.rating,
  (value) => {
    rating.value = value;
  },
);

const { addToList } = useAddToList();

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

<style scoped>
.game-card-poster {
  height: 225px;
  position: relative;
}

.game-card-rating {
  align-items: center;
  background: rgba(0, 0, 0, 0.62);
  bottom: 0;
  display: flex;
  height: 36px;
  justify-content: center;
  left: 0;
  position: absolute;
  right: 0;
  z-index: 1;
}
</style>
