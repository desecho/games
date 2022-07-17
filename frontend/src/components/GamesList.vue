<template>
  <v-card variant="flat">
    <slot></slot>
    <v-tabs v-model="tab" background-color="deep-purple-accent-4" centered stacked>
      <v-tab v-for="list in lists" :key="list.id" :value="list.key" :to="getPath(list.key)">
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
  name: "GamesListView",
  components: {
    ListWindowItem,
  },
  props: {
    records: {
      type: Object as PropType<RecordType[]>,
      required: true,
    },
    username: {
      type: String,
      required: false,
      default: null,
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
      tab: "want-to-play",
    };
  },
  computed: {
    isProfile(): boolean {
      if (this.username) {
        return true;
      }
      return false;
    },
  },
  methods: {
    getPath(listKey: string): string {
      if (this.isProfile) {
        return `/user/${this.username}/${listKey}`;
      }
      return `/games/${listKey}`;
    },
  },
});
</script>