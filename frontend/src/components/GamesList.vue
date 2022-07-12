<template>
  <v-card variant="flat">
    <slot></slot>
    <v-tabs v-model="tab" background-color="deep-purple-accent-4" centered stacked>
      <v-tab v-for="list in lists" :key="list.id" :value="list.key" :to="to">
        <v-icon>mdi-{{ list.icon }}</v-icon>
        {{ list.name }}
      </v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <ListWindowItem
        v-for="list in lists"
        :key="list.id"
        :records-prop="records"
        :list-key="list.key"
        :is-profile="isProfile"
        :is-own-profile="isOwnProfile"
      />
    </v-window>
  </v-card>
</template>

<script lang="ts">
import { defineComponent, PropType } from "vue";
import { Lists } from "../const";
import ListWindowItem from "../components/ListWindowItem.vue";
import { RecordType } from "../types";

export default defineComponent({
  name: "GamesView",
  components: {
    ListWindowItem,
  },
  props: {
    to: {
      type: String,
      required: true,
    },
    records: {
      type: Object as PropType<RecordType[]>,
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
      lists: Lists,
      tab: null,
    };
  },
});
</script>
