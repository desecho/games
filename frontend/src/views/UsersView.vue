<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <v-card elevation="2" class="mb-4">
          <v-card-title class="bg-primary text-white">
            <v-icon start>mdi-account-group</v-icon>
            Users
            <v-spacer></v-spacer>
            <v-chip color="white" text-color="primary" size="small"> {{ users.length }} users </v-chip>
          </v-card-title>
        </v-card>

        <v-row v-if="users.length > 0">
          <v-col v-for="(user, index) in users" :key="index" cols="12" sm="6" md="4" lg="3" xl="2">
            <v-card elevation="2" hover class="user-card" :to="`/users/${user}`" router>
              <v-card-text class="text-center pa-4">
                <v-avatar size="64" color="primary" class="mb-3">
                  <v-icon size="32" color="white">mdi-account</v-icon>
                </v-avatar>
                <div class="text-h6 text-truncate">{{ user }}</div>
                <div class="text-caption text-medium-emphasis">User Profile</div>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>

        <v-card v-else elevation="1" class="text-center pa-8">
          <v-icon size="64" color="grey-lighten-1" class="mb-4">mdi-account-off</v-icon>
          <div class="text-h6 text-medium-emphasis mb-2">No Users Found</div>
          <div class="text-body-2 text-disabled">There are currently no users to display.</div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import axios from "axios";
import { onMounted, ref } from "vue";

import type { AxiosError } from "axios";
import type { Ref } from "vue";

import { getUrl } from "../helpers";
import { $toast } from "../toast";

const users: Ref<string[]> = ref([]);

function loadUsers(): void {
  axios
    .get(getUrl("users/"))
    .then((response) => {
      users.value = response.data as string[];
    })
    .catch((error: AxiosError) => {
      console.log(error);
      $toast.error("Error loading users");
    });
}

onMounted(() => {
  loadUsers();
});
</script>

<style scoped>
.user-card {
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.5, 1);
  cursor: pointer;
}

.user-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15) !important;
}

.user-card .v-card-text {
  position: relative;
  overflow: hidden;
}

.user-card .v-card-text::before {
  content: "";
  position: absolute;
  top: 0;
  left: 50%;
  width: 0;
  height: 2px;
  background: rgb(var(--v-theme-primary));
  transition: all 0.3s ease;
  transform: translateX(-50%);
}

.user-card:hover .v-card-text::before {
  width: 80%;
}

.text-truncate {
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
</style>
