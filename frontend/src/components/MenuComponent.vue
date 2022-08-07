<template>
  <div>
    <v-app-bar v-if="isMobile">
      <v-app-bar-nav-icon variant="text" @click="toggleDrawer()"></v-app-bar-nav-icon>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" width="170" elevation="2" touchless>
      <v-list>
        <MenuItem title="Search" icon="magnify" to="/" />
        <MenuItem title="Games" icon="controller" to="/games" />
        <MenuItem title="Users" icon="account-group" to="/users" />
      </v-list>
      <template #append>
        <v-list>
          <MenuItem v-if="!isLoggedIn" title="Login" icon="login" to="/login" />
          <MenuItem v-if="isLoggedIn" title="Settings" icon="cog" to="/preferences" />
          <MenuItem v-if="isLoggedIn" title="Logout" icon="logout" to="/logout" />
        </v-list>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from "vue";

import { useAuthStore } from "../stores/auth";
import { useMobile } from "../composables/mobile";

import MenuItem from "./MenuItem.vue";

const drawer = ref(false);
const { user } = useAuthStore();
const isLoggedIn = user.isLoggedIn;

function toggleDrawer() {
  drawer.value = !drawer.value;
}

const { isMobile } = useMobile();

onMounted(() => {
  if (!isMobile.value) {
    drawer.value = true;
  }
});
</script>
