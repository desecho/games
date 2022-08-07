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
import MenuComponent from "./components/MenuComponent.vue";
import FooterComponent from "./components/FooterComponent.vue";
</script>
