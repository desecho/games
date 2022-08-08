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
            :autofocus="true"
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

<script lang="ts" setup>
import { AxiosError, AxiosStatic } from "axios";
import { inject, Ref, ref } from "vue";

import GameSearchResultCard from "../components/GameSearchResultCard.vue";
import { useFormValidation } from "../composables/formValidation";
import { getUrl, rulesHelper } from "../helpers";
import { $toast } from "../toast";
import { Game } from "../types";

// eslint-disable-next-line @typescript-eslint/no-non-null-assertion
const axios: AxiosStatic = inject("axios")!;

const rules = rulesHelper;

const valid = ref(false);
const games: Ref<Game[]> = ref([]);
const query = ref("");

const { form, isValid } = useFormValidation();

async function search() {
  if (!(await isValid())) {
    return;
  }
  axios
    .get(getUrl("search/"), { params: { query: query.value } })
    .then((response) => {
      games.value = response.data as Game[];
    })
    .catch((error: AxiosError) => {
      console.log(error);
      $toast.error("Search error");
    });
}
</script>
