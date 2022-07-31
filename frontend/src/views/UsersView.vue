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

<script lang="ts">
import { defineComponent } from "vue";
import { getUrl } from "../helpers";
import { UsersViewComponentData } from "../types";

export default defineComponent({
  name: "UsersView",
  data(): UsersViewComponentData {
    return {
      users: [],
    };
  },
  mounted() {
    this.loadUsers();
  },
  methods: {
    loadUsers() {
      this.axios
        .get(getUrl("users/"))
        .then((response) => {
          this.users = response.data;
        })
        .catch((error) => {
          console.log(error);
          this.$toast.error("Error loading users");
        });
    },
  },
});
</script>
