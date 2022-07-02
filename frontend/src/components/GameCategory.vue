<template>
  <v-card-subtitle
    v-if="name != 'Main Game'"
    class="game-subtitle font-weight-black"
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
