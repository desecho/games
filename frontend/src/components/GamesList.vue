<template>
  <v-window-item :value="listKey">
    <v-card class="wrapper">
      <v-card-text>
        <div class="d-flex align-content-space-around flex-wrap">
          <draggable
            v-model="records"
            item-key="id"
            class="d-flex flex-wrap"
            :disabled="!isDraggable"
            @sort="saveRecordsOrder"
          >
            <template #item="{ element, index }">
              <GameCard
                v-if="element.listKey == listKey && isShowGame(element.game)"
                :record="element"
                :index="index"
                :list-key="listKey"
                :username="username"
                :class="{ draggable: isDraggable }"
              />
            </template>
          </draggable>
        </div>
      </v-card-text>
    </v-card>
  </v-window-item>
</template>

<script lang="ts" setup>
import Draggable from "vuedraggable";
import { AxiosError, AxiosStatic } from "axios";
import { inject, computed, toRef } from "vue";

import { $toast } from "../toast";
import { RecordType, SortData, Game } from "../types";
import { DLCKindCategories } from "../const";
import { getUrl, rewriteArray, requireAuthenticated } from "../helpers";
import { useSettingsStore } from "../stores/settings";
import { useMobile } from "../composables/mobile";

import GameCard from "./GameCard.vue";

const axios: AxiosStatic = inject("axios")!;

interface Props {
  recordsProp: RecordType[];
  listKey: string;
  username?: string;
}

const props = defineProps<Props>();
const records = computed({
  get: () => props.recordsProp,
  set: (records: RecordType[]) => {
    rewriteArray(props.recordsProp, records);
  },
});
const isDraggable = computed(() => {
  // This is not working on mobile with v-window. Disabling for now.
  return !props.username && !isMobile.value;
});
const settingsStore = useSettingsStore();
const settings = toRef(settingsStore, "settings");

function saveRecordsOrder() {
  requireAuthenticated();
  const getSortData = () => {
    const data: SortData[] = [];
    records.value.forEach((record, index) => {
      const sortData = { id: record.id, order: index + 1 };
      data.push(sortData);
    });
    return data;
  };
  axios.put(getUrl("records/save-order/"), { records: getSortData() }).catch((error: AxiosError) => {
    console.log(error);
    $toast.error("Error saving games order");
  });
}

function isShowGame(game: Game) {
  if (settings.value.games.areUnreleasedGamesHidden && !game.isReleased) {
    return false;
  }
  if (settings.value.games.areDLCsHidden && DLCKindCategories.includes(game.category)) {
    return false;
  }
  return true;
}

const { isMobile } = useMobile();
</script>

<style scoped>
/* This is needed for the swipe to work */
.wrapper {
  min-height: 500px;
}
</style>
