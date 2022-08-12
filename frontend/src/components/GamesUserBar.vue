<template>
  <v-card-title class="username-bar">
    <v-img src="/img/games-user-bar-background.png" width="100%" cover>
      <div class="username">{{ username }}</div>
    </v-img>
  </v-card-title>
</template>

<script lang="ts" setup>
defineProps<{
  username?: string;
}>();
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
