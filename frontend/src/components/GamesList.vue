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

<script lang="ts">
import { defineComponent, PropType } from "vue";
import Draggable from "vuedraggable";
import { mapState } from "pinia";

import { RecordType, SortData, Game } from "../types";
import { DLCKindCategories } from "../const";
import { getUrl, rewriteArray, requireAuthenticated } from "../helpers";
import { useSettingsStore } from "../stores/settings";
import { mobileMixin } from "../mixins/mobile";

import GameCard from "./GameCard.vue";

export default defineComponent({
  name: "GamesList",
  components: {
    GameCard,
    Draggable,
  },
  mixins: [mobileMixin],
  props: {
    recordsProp: {
      type: Object as PropType<RecordType[]>,
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
  computed: {
    records: {
      get(): RecordType[] {
        return this.recordsProp;
      },
      set(records: RecordType[]) {
        rewriteArray(this.recordsProp, records);
      },
    },
    isDraggable() {
      // This is not working on mobile with v-window. Disabling for now.
      return !this.username && !this.isMobile;
    },
    ...mapState(useSettingsStore, ["settings"]),
  },
  methods: {
    saveRecordsOrder() {
      requireAuthenticated();
      const getSortData = () => {
        const data: SortData[] = [];
        this.records.forEach((record, index) => {
          const sortData = { id: record.id, order: index + 1 };
          data.push(sortData);
        });
        return data;
      };
      this.axios.put(getUrl("records/save-order/"), { records: getSortData() }).catch((error) => {
        console.log(error);
        this.$toast.error("Error saving games order");
      });
    },
    isShowGame(game: Game) {
      if (this.settings.games.areUnreleasedGamesHidden && !game.isReleased) {
        return false;
      }
      if (this.settings.games.areDLCsHidden && DLCKindCategories.includes(game.category)) {
        return false;
      }
      return true;
    },
  },
});
</script>

<style scoped>
/* This is needed for the swipe to work */
.wrapper {
  min-height: 500px;
}
</style>
