<template>
  <v-navigation-drawer width="170" elevation="2">
    <v-list>
      <MenuItem title="Search" icon="magnify" to="/" />
      <MenuItem title="Games" icon="google-controller" to="/games" />
      <MenuItem v-if="!isLoggedIn" title="Login" icon="login" to="/login" />
      <MenuItem v-if="isLoggedIn" title="Logout" icon="logout" to="/logout" />
    </v-list>
  </v-navigation-drawer>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import { useAuthStore } from "../stores/auth";
import MenuItem from "./MenuItem.vue";

export default defineComponent({
  name: "MenuView",
  components: {
    MenuItem,
  },
  computed: {
    isLoggedIn() {
      const { user } = useAuthStore();
      return user.isLoggedIn;
    },
  },
});
</script>
