<template>
  <v-footer class="footer-component d-flex justify-center align-center text-center px-4 py-6" app>
    <div class="footer-content">
      <div class="footer-links mb-3">
        <span class="text-body-2">
          Powered by <a href="https://www.igdb.com/" target="_blank" class="footer-link">IGDB</a>
        </span>
        <span class="mx-2">•</span>
        <router-link to="/about" class="footer-link">About Games</router-link>
      </div>
      <div class="footer-copyright text-caption">
        © 2022 - {{ new Date().getFullYear() }} {{ email }}. All rights reserved.
      </div>
    </div>
  </v-footer>
</template>

<script lang="ts" setup>
import { ADMIN_EMAIL } from "../const";

const email = ADMIN_EMAIL;
</script>

<style scoped>
.footer-component {
  border-top: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  background-color: rgb(var(--v-theme-surface));
}

.footer-content {
  max-width: 100%;
  width: 100%;
}

.footer-link {
  color: rgb(var(--v-theme-primary));
  text-decoration: none;
  transition: color 0.2s ease;
}

.footer-link:hover {
  color: rgb(var(--v-theme-primary-darken-1));
  text-decoration: underline;
}

.footer-links {
  display: flex;
  align-items: center;
  justify-content: center;
  flex-wrap: wrap;
  gap: 0.5rem;
}

.footer-copyright {
  opacity: 0.8;
}

@media (max-width: 600px) {
  .footer-links {
    flex-direction: column;
    gap: 0.25rem;
  }

  .mx-2 {
    display: none;
  }
}
</style>
