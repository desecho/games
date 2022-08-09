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
import { inject, onMounted, ref } from "vue";

import type { AxiosError, AxiosStatic } from "axios";
import type { Ref} from "vue";

import { getUrl } from "../helpers";
import { $toast } from "../toast";


// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const axios: AxiosStatic = inject("axios")!;

const users: Ref<string[]> = ref([]);

function loadUsers() {
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
