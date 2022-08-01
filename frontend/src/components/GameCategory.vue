<template>
  <v-card-subtitle
    v-if="name != 'Main Game'"
    class="game-category font-weight-black"
    :class="{ 'text-white': color == 'white' }"
    :title="name"
  >
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
    color: {
      type: String,
      default: "",
    },
  },
});
</script>

<style scoped>
.game-category {
  position: absolute;
  bottom: 0;
  right: 5px;
}
</style>
