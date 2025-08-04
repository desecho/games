<template>
  <v-app>
    <v-main>
      <MenuComponent />
      <RouterView />
    </v-main>
    <FooterComponent />
  </v-app>
</template>

<script lang="ts" setup>
import { onMounted } from "vue";

import FooterComponent from "./components/FooterComponent.vue";
import MenuComponent from "./components/MenuComponent.vue";
import { useAppTheme } from "./composables/theme";

const { initializeTheme } = useAppTheme();

onMounted(() => {
  initializeTheme();
});
</script>
