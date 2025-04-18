<template>
  <div v-if="isLoaded">
    <GamesLists v-if="!userNotFound && !userIsHidden" :username="username" :records="records" />
    <v-alert v-if="userNotFound || userIsHidden" prominent type="error" variant="text" class="ma-5">
      <span v-if="userNotFound"> User {{ username }} not found. </span>
      <span v-if="userIsHidden"> {{ username }}'s profile is hidden. </span>
    </v-alert>
  </div>
</template>

<script lang="ts" setup>
import axios from "axios";
import { onMounted, ref } from "vue";

import type { ListKey, RecordType } from "../types";
import type { AxiosError } from "axios";
import type { Ref } from "vue";

import GamesLists from "../components/GamesLists.vue";
import { DEFAULT_LIST } from "../const";
import { getUrl } from "../helpers";
import { $toast } from "../toast";

const props = withDefaults(
  defineProps<{
    listKey?: ListKey;
    username: string;
  }>(),
  {
    listKey: DEFAULT_LIST,
  },
);

const records: Ref<RecordType[]> = ref([]);
const userNotFound = ref(false);
const userIsHidden = ref(false);
const isLoaded = ref(false);

onMounted(() => {
  axios
    .get(getUrl(`records/users/${props.username}/`))
    .then((response) => {
      records.value = response.data as RecordType[];
      isLoaded.value = true;
    })
    .catch((error: AxiosError) => {
      if (error.response.status === 404) {
        userNotFound.value = true;
        isLoaded.value = true;
      } else if (error.response.status === 403) {
        userIsHidden.value = true;
        isLoaded.value = true;
      } else {
        console.log(error);
        $toast.error("Error loading games");
      }
    });
});
</script>
