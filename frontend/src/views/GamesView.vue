<template>
  <GamesLists :records="records" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { mapState } from "pinia";

import { useGamesStore } from "../stores/games";

import GamesLists from "../components/GamesLists.vue";

export default defineComponent({
  name: "GamesView",
  components: {
    GamesLists,
  },
  props: {
    listKey: {
      type: String,
      default: "want-to-play",
      required: false,
    },
  },
  computed: {
    ...mapState(useGamesStore, ["records"]),
  },
  mounted() {
    const { loadGames } = useGamesStore();
    loadGames().catch((error) => {
      console.log(error);
      this.$toast.error("Error loading games");
    });
  },
});
</script>
