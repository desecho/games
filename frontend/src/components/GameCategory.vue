<template>
  <v-card-subtitle v-if="name != 'Main Game'" class="game-category font-weight-black text-white" :title="name">
    {{ name }}
  </v-card-subtitle>
</template>

<script lang="ts">
import { defineComponent } from "vue";

export default defineComponent({
  name: "GameCategory",
  props: {
    name: {
      type: String,
      required: true,
    },
  },
});
</script>

<style scoped>
.game-category {
  position: absolute;
  bottom: 2px;
  right: 5px;
  background-color: #000000a6;
  border-radius: 5px;
}
</style>
