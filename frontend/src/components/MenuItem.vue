<template>
  <router-link v-slot="{ href, isActive }" :to="to" custom>
    <v-list-item link :href="href" :active="isActive" :to="to">
      <v-list-item-avatar start>
        <v-list-item-icon :icon="'mdi-' + icon"> </v-list-item-icon>
      </v-list-item-avatar>
      <v-list-item-title>{{ title }}</v-list-item-title>
    </v-list-item>
  </router-link>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { RouterLink } from "vue-router";

export default defineComponent({
  name: "MenuItem",
  components: {
    RouterLink,
  },
  props: {
    title: {
      type: String,
      required: true,
    },
    icon: {
      type: String,
      required: true,
    },
    to: {
      type: String,
      required: true,
    },
  },
});
</script>
