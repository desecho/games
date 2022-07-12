<template>
  <GamesList :records="records" />
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useGamesStore } from "../stores/games";
import { mapState } from "pinia";
import GamesList from "../components/GamesList.vue";

export default defineComponent({
  name: "GamesView",
  components: {
    GamesList,
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
