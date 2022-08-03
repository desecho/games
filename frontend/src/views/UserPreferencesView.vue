<template>
  <v-container>
    <v-row>
      <v-col v-cloak cols="12">
        <v-checkbox v-model="hidden" label="Hide profile" hide-details @change="savePreferences()"></v-checkbox>
        Profile link: <router-link :to="profileLink">{{ profileLink }}</router-link>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from "vue";

import { UserPreferencesViewComponentData } from "../types";
import { getUrl } from "../helpers";
import { useAuthStore } from "../stores/auth";

const url = getUrl("user/preferences/");

export default defineComponent({
  name: "UserPreferencesView",
  data(): UserPreferencesViewComponentData {
    return {
      hidden: false,
    };
  },
  computed: {
    profileLink() {
      const { user } = useAuthStore();
      return `/users/${user.username!}`;
    },
  },
  mounted() {
    this.loadPreferences();
  },
  methods: {
    loadPreferences() {
      this.axios
        .get(url)
        .then((response) => {
          this.hidden = response.data.hidden;
        })
        .catch((error) => {
          console.log(error);
          this.$toast.error("Error loading preferences");
        });
    },
    savePreferences() {
      this.axios.put(url, { hidden: this.hidden }).catch((error) => {
        console.log(error);
        this.$toast.error("Error saving preferences");
      });
    },
  },
});
</script>
