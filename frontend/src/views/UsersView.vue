<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <div v-for="(user, index) in users" :key="index">
          <router-link :to="'/users/' + user">{{ user }}</router-link
          ><br />
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import { ref, inject, Ref, onMounted } from "vue";
import { AxiosError, AxiosStatic } from "axios";

import { $toast } from "../toast";
import { getUrl } from "../helpers";

// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const axios: AxiosStatic = inject("axios")!;

const users: Ref<string[]> = ref([]);

function loadUsers() {
  axios
    .get(getUrl("users/"))
    .then((response) => {
      users.value = response.data;
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
