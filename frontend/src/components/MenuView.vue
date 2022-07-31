<template>
  <div>
    <v-app-bar v-if="isMobile">
      <v-app-bar-nav-icon variant="text" @click="drawer = !drawer"></v-app-bar-nav-icon>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" width="170" elevation="2" touchless>
      <v-list>
        <MenuItem title="Search" icon="magnify" to="/" />
        <MenuItem title="Games" icon="google-controller" to="/games" />
        <MenuItem title="Users" icon="account-group" to="/users" />
      </v-list>
      <template #append>
        <v-list>
          <MenuItem v-if="!isLoggedIn" title="Login" icon="login" to="/login" />
          <MenuItem v-if="isLoggedIn" title="Logout" icon="logout" to="/logout" />
        </v-list>
      </template>
    </v-navigation-drawer>
  </div>
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
  data() {
    return {
      drawer: false,
    };
  },
  computed: {
    isLoggedIn() {
      const { user } = useAuthStore();
      return user.isLoggedIn;
    },
    isMobile() {
      return this.$vuetify.display.xs;
    },
  },
  mounted() {
    if (!this.isMobile) {
      this.drawer = true;
    }
  },
});
</script>
