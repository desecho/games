<template>
  <v-container>
    <v-row>
      <v-col v-cloak cols="12">
        <v-checkbox v-model="hidden" label="Hide profile" hide-details @change="savePreferences()"></v-checkbox>
        Profile link: <router-link :to="profileLink">{{ absoluteProfileLink }}</router-link>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, inject, computed, onMounted } from "vue";
import { AxiosError, AxiosStatic } from "axios";

import { $toast } from "../toast";
import { GetUserPreferencesData } from "../types";
import { getUrl } from "../helpers";
import { useAuthStore } from "../stores/auth";

// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const axios: AxiosStatic = inject("axios")!;

const url = getUrl("user/preferences/");

const hidden = ref(false);
const profileLink = computed(() => {
  const { user } = useAuthStore();
  // username is always not null when user is logged in
  // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
  return `/users/${user.username!}`;
});
const absoluteProfileLink = computed(() => {
  return `${location.origin}${profileLink.value}`;
});

function loadPreferences() {
  axios
    .get(url)
    .then((response) => {
      const data = response.data as GetUserPreferencesData;
      hidden.value = data.hidden;
    })
    .catch((error: AxiosError) => {
      console.log(error);
      $toast.error("Error loading preferences");
    });
}
function savePreferences() {
  axios.put(url, { hidden: hidden.value }).catch((error: AxiosError) => {
    console.log(error);
    $toast.error("Error saving preferences");
  });
}
onMounted(() => {
  loadPreferences();
});
</script>
