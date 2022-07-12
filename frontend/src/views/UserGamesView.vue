<template>
  <div v-if="isLoaded">
    <GamesList
      v-if="!userNotFound && !userIsHidden"
      :username="username"
      :records="records"
      :is-own-profile="isOwnProfile"
    >
      <v-card-title v-if="username" class="bg-purple-darken-2">
        {{ username }}
      </v-card-title>
    </GamesList>
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
import { getUrl } from "../helpers";
import { RecordType } from "../types";
import GamesList from "../components/GamesList.vue";

export default defineComponent({
  name: "UserGamesView",
  components: {
    GamesList,
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
      isOwnProfile: false,
    };
  },
  mounted() {
    this.axios
      .get(getUrl(`records/users/${this.username}/`))
      .then((response) => {
        this.records = response.data.records;
        this.isOwnProfile = response.data.isOwnProfile;
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
