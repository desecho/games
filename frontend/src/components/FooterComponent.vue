<template>
  <v-window>
    <v-window-item>
      <v-footer class="text-right float-right mt-5"
        ><div>
          Powered by <a href="https://www.igdb.com/" target="_blank">IGDB</a><br />
          <router-link to="/about">About Games</router-link><br />
          © 2022 - {{ new Date().getFullYear() }} {{ email }}. All rights reserved.
        </div>
      </v-footer>
    </v-window-item>
  </v-window>
</template>

<script lang="ts" setup>
import { ADMIN_EMAIL } from "../const";

const email = ADMIN_EMAIL;
</script>
