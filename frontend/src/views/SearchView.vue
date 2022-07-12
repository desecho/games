<template>
  <v-container>
    <v-row>
      <v-col cols="9">
        <v-form ref="form" v-model="valid" lazy-validation @submit.prevent="search">
          <v-text-field
            v-model="query"
            label="Search"
            variant="solo"
            :hide-details="true"
            :rules="[rules.required]"
            class="mr-5"
          ></v-text-field>
        </v-form>
      </v-col>
      <v-col cols="3" class="mt-2">
        <v-btn color="primary" :disabled="!valid" @click="search"> Search </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-sheet class="d-flex align-content-space-around flex-wrap">
          <TransitionGroup name="list" tag="div" class="d-flex flex-wrap">
            <v-sheet v-for="(game, index) in games" :key="game.id">
              <GameSearchResultCard :game="game" :index="index" :games="games" />
            </v-sheet>
          </TransitionGroup>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from "vue";
import { rules } from "../helpers";
import GameSearchResultCard from "../components/GameSearchResultCard.vue";
import { getUrl } from "../helpers";
import { SearchViewComponentData } from "../types";

export default defineComponent({
  name: "SearchView",
  components: {
    GameSearchResultCard,
  },
  data(): SearchViewComponentData {
    return {
      valid: false,
      games: [],
      rules: rules,
      query: "",
    };
  },
  methods: {
    async isValid() {
      const result = await this.$refs.form.validate();
      const valid: boolean = result.valid;
      return valid;
    },
    async search() {
      if (!(await this.isValid())) {
        return;
      }
      this.axios
        .get(getUrl("search/"), { params: { query: this.query } })
        .then((response) => {
          this.games = response.data;
        })
        .catch((error) => {
          console.log(error);
          this.$toast.error("Search error");
        });
    },
  },
});
</script>
