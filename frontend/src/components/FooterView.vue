<template>
  <v-window>
    <v-window-item>
      <v-footer class="text-right float-right mt-5"
        ><div>
          Powered by <a href="https://www.igdb.com/" target="_blank">IGDB</a><br />
          <router-link to="/about">About Games</router-link><br />
          Copyright © {{ new Date().getFullYear() }} desecho@gmail.com.
        </div>
      </v-footer>
    </v-window-item>
  </v-window>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";

export default defineComponent({
  name: "FooterView",
  components: {
    RouterLink,
  },
});
</script>
