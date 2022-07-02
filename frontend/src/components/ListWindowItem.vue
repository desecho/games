<template>
  <v-window-item :value="listKey">
    <v-card>
      <v-card-text>
        <div class="d-flex align-content-space-around flex-wrap">
          <draggable v-model="records" item-key="id" class="d-flex flex-wrap" @sort="saveRecordsOrder">
            <template #item="{ element, index }">
              <GameCard v-if="element.listKey == listKey" :record="element" :index="index" :list-key="listKey" />
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
import { getUrl, rewriteArray, requireAuthenticated } from "../helpers";
import { RecordType, SortData } from "../types";
import GameCard from "./GameCard.vue";

export default defineComponent({
  name: "ListWindowItem",
  components: {
    GameCard,
    Draggable,
  },
  props: {
    recordsProp: {
      type: Object as PropType<RecordType[]>,
      required: true,
    },
    listKey: {
      type: String,
      required: true,
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
      this.axios.put(getUrl("records/save-order/"), { records: getSortData() }).catch(() => {
        this.$toast.error("Error saving games order");
      });
    },
  },
});
</script>
