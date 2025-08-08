<template>
  <div>
    <v-app-bar v-if="isMobile" height="72">
      <v-app-bar-nav-icon variant="text" @click="toggleDrawer()"></v-app-bar-nav-icon>
      <v-app-bar-title class="d-flex align-center">
        <div class="d-flex align-center">
          <v-img src="/img/logo.png" alt="Games logo" width="40" height="40" class="mr-2" contain></v-img>
          <span class="text-h6 font-weight-medium">Games</span>
        </div>
      </v-app-bar-title>
      <v-spacer></v-spacer>
      <DarkModeToggle />
    </v-app-bar>
    <v-navigation-drawer v-model="drawer" width="170" elevation="2" touchless>
      <div class="app-brand pa-4 d-flex flex-column align-center">
        <v-img src="/img/logo.png" alt="Games logo" width="85" height="85" class="mb-2" contain></v-img>
        <span class="text-h6 font-weight-medium">Games</span>
      </div>
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
          <v-divider class="my-2"></v-divider>
          <v-list-item class="px-2">
            <div class="d-flex align-center justify-space-between">
              <span class="text-caption">Theme</span>
              <DarkModeToggle />
            </div>
          </v-list-item>
        </v-list>
      </template>
    </v-navigation-drawer>
  </div>
</template>

<script lang="ts" setup>
import { onMounted, ref, toRef } from "vue";

import { useMobile } from "../composables/mobile";
import { useAuthStore } from "../stores/auth";

import DarkModeToggle from "./DarkModeToggle.vue";
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
