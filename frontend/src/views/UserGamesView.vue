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

<script lang="ts">
import { AxiosError } from "axios";
import { defineComponent } from "vue";

import { Lists } from "../const";
import { RecordType } from "../types";
import { getUrl } from "../helpers";

import GamesLists from "../components/GamesLists.vue";

export default defineComponent({
  name: "UserGamesView",
  components: {
    GamesLists,
  },
  props: {
    listKey: {
      type: String,
      default: "want-to-play",
      required: false,
    },
    username: {
      type: String,
      required: true,
    },
  },
  data() {
    const records: RecordType[] = [];
    return {
      tab: null,
      lists: Lists,
      records: records,
      userNotFound: false,
      userIsHidden: false,
      isLoaded: false,
    };
  },
  mounted() {
    this.axios
      .get(getUrl(`records/users/${this.username}/`))
      .then((response) => {
        this.records = response.data;
        this.isLoaded = true;
      })
      .catch((error: AxiosError) => {
        if (error.response.status == 404) {
          this.userNotFound = true;
          this.isLoaded = true;
        } else if (error.response.status == 403) {
          this.userIsHidden = true;
          this.isLoaded = true;
        } else {
          console.log(error);
          this.$toast.error("Error loading games");
        }
      });
  },
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
