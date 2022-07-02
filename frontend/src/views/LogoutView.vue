<template>
  <v-container>
    <v-row class="text-center">
      <v-col class="mb-4" cols="12">
        <p>Logging out...</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { useAuthStore } from "../stores/auth";

export default defineComponent({
  name: "LogoutView",
  mounted() {
    const { logout } = useAuthStore();
    logout();
  },
});
</script>
