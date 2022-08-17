<template>
  <v-container>
    <v-row>
      <v-col cols="9">
        <v-form ref="form" v-model="isFormValid" lazy-validation @submit.prevent="search">
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
        <v-btn color="primary" :disabled="!isFormValid" @click="search"> Search </v-btn>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12">
        <v-sheet class="d-flex align-content-space-around flex-wrap">
          <TransitionGroup name="list" tag="div" class="d-flex flex-wrap">
            <v-sheet v-for="(game, index) in games" :key="game.id">
              <GameSearchResultCard :game="game" @add-to-list="(listId) => addGame(game.id, listId, index)" />
            </v-sheet>
          </TransitionGroup>
        </v-sheet>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts" setup>
import axios from "axios";
import { ref } from "vue";

import type { Game } from "../types";
import type { AxiosError } from "axios";
import type { Ref } from "vue";

import GameSearchResultCard from "../components/GameSearchResultCard.vue";
import { useAddToList } from "../composables/addToList";
import { useFormValidation } from "../composables/formValidation";
import { getUrl, rulesHelper } from "../helpers";
import { $toast } from "../toast";

const rules = rulesHelper;

const isFormValid = ref(false);
const games: Ref<Game[]> = ref([]);
const query = ref("");

const { form, isValid } = useFormValidation();

async function search(): Promise<void> {
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
const { addToList } = useAddToList();

function addGame(gameId: number, listId: number, index: number): void {
  addToList(gameId, listId)
    .then(() => {
      console.log("Game added");
      games.value.splice(index, 1);
    })
    .catch((error: AxiosError) => {
      console.log(error);
      $toast.error("Error adding a game");
    });
}
</script>
