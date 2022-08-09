<template>
  <div v-if="isLoaded">
    <GamesLists v-if="!userNotFound && !userIsHidden" :username="username" :records="records">
      <v-card-title v-if="username" class="username-bar">
        <v-img src="/img/cover.png" width="100%" cover
          ><div class="username">{{ username }}</div></v-img
        >
      </v-card-title>
    </GamesLists>
    <v-alert v-if="userNotFound || userIsHidden" prominent type="error" variant="outlined" class="ma-5">
      <span v-if="userNotFound"> User {{ username }} not found. </span>
      <span v-if="userIsHidden"> {{ username }}'s profile is hidden. </span>
    </v-alert>
  </div>
</template>

<script lang="ts" setup>
import { AxiosError, AxiosStatic } from "axios";
import { inject, onMounted, Ref, ref } from "vue";

import GamesLists from "../components/GamesLists.vue";
import { getUrl } from "../helpers";
import { $toast } from "../toast";
import { RecordType } from "../types";

// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const axios: AxiosStatic = inject("axios")!;

interface Props {
  listKey?: string;
  username: string;
}

const props = withDefaults(defineProps<Props>(), {
  listKey: "want-to-play",
});

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
      if (error.response.status == 404) {
        userNotFound.value = true;
        isLoaded.value = true;
      } else if (error.response.status == 403) {
        userIsHidden.value = true;
        isLoaded.value = true;
      } else {
        console.log(error);
        $toast.error("Error loading games");
      }
    });
});
</script>

<style scoped>
.username-bar {
  padding: 0 !important;
  height: 75px;
}

.username {
  color: white;
  padding-left: 15px;
  margin-top: 15px;
  font-size: 1.6em;
}
</style>
