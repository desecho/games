<template>
  <v-app>
    <v-main>
      <MenuView />
      <RouterView />
    </v-main>
    <FooterView />
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

import MenuView from "./components/MenuView.vue";
import FooterView from "./components/FooterView.vue";

export default defineComponent({
  name: "App",
  components: {
    RouterView,
    MenuView,
    FooterView,
  },
});
</script>
