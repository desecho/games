<template>
  <div>
    <v-app-bar v-if="isMobile">
      <v-app-bar-nav-icon variant="text" @click="toggleDrawer()"></v-app-bar-nav-icon>
      <v-app-bar-title>Games</v-app-bar-title>
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" width="170" elevation="2" touchless>
      <v-list>
        <MenuItem title="Search" icon="magnify" to="/" />
        <MenuItem v-if="user.isLoggedIn" title="Games" icon="controller" to="/games" />
        <MenuItem title="Users" icon="account-group" to="/users" />
      </v-list>
      <template #append>
        <v-list>
          <MenuItem v-if="!user.isLoggedIn" title="Login" icon="login" to="/login" />
          <MenuItem v-if="user.isLoggedIn" title="Settings" icon="cog" to="/preferences" />
          <MenuItem v-if="user.isLoggedIn" title="Logout" icon="logout" to="/logout" />
        </v-list>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, toRef } from "vue";

import { useMobile } from "../composables/mobile";
import { useAuthStore } from "../stores/auth";

import MenuItem from "./MenuItem.vue";

const drawer = ref(false);
const userStore = useAuthStore();
const user = toRef(userStore, "user");

function toggleDrawer(): void {
  drawer.value = !drawer.value;
}

const { isMobile } = useMobile();

onMounted(() => {
  if (!isMobile.value) {
    drawer.value = true;
  }
});
</script>
