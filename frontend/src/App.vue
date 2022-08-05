<template>
  <v-app>
    <v-main>
      <MenuComponent />
      <RouterView />
    </v-main>
    <FooterComponent />
  </v-app>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterView } from "vue-router";

import MenuComponent from "./components/Menu.vue";
import FooterComponent from "./components/Footer.vue";

export default defineComponent({
  name: "App",
  components: {
    RouterView,
    MenuComponent,
    FooterComponent,
  },
});
</script>
