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
import axios from "axios";
import { computed, toRef } from "vue";
import Draggable from "vuedraggable";

import type { Game, ListKey, RecordType } from "../types";
import type { SortData } from "./types";
import type { AxiosError } from "axios";

import { useMobile } from "../composables/mobile";
import { DlcKindCategories } from "../const";
import { getUrl, requireAuthenticated, rewriteArray } from "../helpers";
import { useSettingsStore } from "../stores/settings";
import { $toast } from "../toast";

import GameCard from "./GameCard.vue";

const props = defineProps<{
  recordsProp: RecordType[];
  listKey: ListKey;
  username?: string;
}>();

const records = computed({
  get: () => props.recordsProp,
  set: (recordsNew: RecordType[]) => {
    rewriteArray(props.recordsProp, recordsNew);
  },
});
const isProfile = props.username !== undefined;
const isDraggable = computed(() => {
  const { isMobile } = useMobile();
  // This is not working on mobile with v-window. Disabling for now
  return !isProfile && !isMobile.value;
});
const settingsStore = useSettingsStore();
const settings = toRef(settingsStore, "settings");

function saveRecordsOrder(): void {
  function getSortData(): SortData[] {
    const data: SortData[] = [];
    records.value.forEach((record, index) => {
      const sortData = { id: record.id, order: index + 1 };
      data.push(sortData);
    });
    return data;
  }

  requireAuthenticated();
  axios.put(getUrl("records/save-order/"), { records: getSortData() }).catch((error: AxiosError) => {
    console.log(error);
    $toast.error("Error saving games order");
  });
}

function isShowGame(game: Game): boolean {
  if (settings.value.games.areUnreleasedGamesHidden && !game.isReleased) {
    return false;
  }
  if (settings.value.games.areDLCsHidden && DlcKindCategories.includes(game.category)) {
    return false;
  }
  return true;
}
</script>

<style scoped>
/* This is needed for the swipe to work */
.wrapper {
  min-height: 500px;
}
</style>
