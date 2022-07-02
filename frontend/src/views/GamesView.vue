<template>
  <v-card variant="flat">
    <v-tabs v-model="tab" background-color="deep-purple-accent-4" centered stacked>
      <v-tab v-for="list in lists" :key="list.id" :value="list.key" :to="'/games/' + list.key">
        <v-icon>mdi-{{ list.icon }}</v-icon>
        {{ list.name }}
      </v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <ListWindowItem v-for="list in lists" :key="list.id" :records-prop="games.records" :list-key="list.key" />
    </v-window>
  </v-card>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useGamesStore } from "../stores/games";
import { mapState } from "pinia";
import { Lists } from "../const";
import ListWindowItem from "../components/ListWindowItem.vue";

export default defineComponent({
  name: "GamesView",
  components: {
    ListWindowItem,
  },
  props: {
    listKey: {
      type: String,
      default: "want-to-play",
      required: false,
    },
  },
  data() {
    return {
      tab: null,
      lists: Lists,
    };
  },
  computed: {
    ...mapState(useGamesStore, ["games"]),
  },
  mounted() {
    const { loadGames } = useGamesStore();
    loadGames().catch(() => {
      this.$toast.error("Error loading games");
    });
  },
});
</script>
