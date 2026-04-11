<template>
  <v-container class="recommendations-page">
    <div class="page-header">
      <div>
        <h1 class="text-h4 font-weight-bold mb-2">AI Recommendations</h1>
        <p class="text-body-1 text-medium-emphasis mb-0">Find games that match your ratings and preferences.</p>
      </div>
      <v-chip color="primary" variant="tonal" size="large">
        <v-icon start icon="mdi-robot"></v-icon>
        AI
      </v-chip>
    </div>

    <v-card class="preferences-card mb-6" elevation="2">
      <v-card-title class="d-flex align-center">
        <v-icon icon="mdi-tune" class="mr-2"></v-icon>
        Preferences
      </v-card-title>
      <v-card-text>
        <v-form @submit.prevent="getRecommendations">
          <v-row>
            <v-col cols="12" md="6">
              <v-select
                v-model="preferences.preferredGenre"
                :items="GAME_GENRES"
                label="Preferred Genre"
                prepend-inner-icon="mdi-controller"
                clearable
                variant="outlined"
                density="comfortable"
              ></v-select>
            </v-col>

            <v-col cols="12" md="6">
              <label class="field-label">Desired Number of Recommendations</label>
              <v-slider
                v-model="preferences.recommendationsNumber"
                :min="AI_MIN_RECOMMENDATIONS"
                :max="AI_MAX_RECOMMENDATIONS"
                :step="1"
                thumb-label
                color="primary"
                class="mt-2"
              ></v-slider>
            </v-col>

            <v-col cols="12" md="6">
              <label class="field-label">Minimum Rating</label>
              <v-rating
                v-model="preferences.minRating"
                :length="AI_MAX_RATING"
                color="amber"
                size="large"
                class="mt-2"
                clearable
              ></v-rating>
              <div class="field-help">
                {{ preferences.minRating ? `${preferences.minRating} stars` : "Any rating" }}
              </div>
            </v-col>

            <v-col cols="12" md="6">
              <label class="field-label">Release Year Range</label>
              <v-range-slider
                v-model="yearRange"
                :min="AI_MIN_YEAR"
                :max="currentYear"
                :step="1"
                thumb-label
                color="primary"
                class="mt-2"
              ></v-range-slider>
              <div class="field-help">{{ yearRange[0] }} - {{ yearRange[1] }}</div>
            </v-col>
          </v-row>

          <div class="actions-row">
            <v-btn
              type="submit"
              color="primary"
              size="large"
              :loading="isLoading"
              :disabled="isLoading"
              prepend-icon="mdi-magic-staff"
            >
              Get Recommendations
            </v-btn>
          </div>
        </v-form>
      </v-card-text>
    </v-card>

    <div v-if="games.length > 0" class="results-section">
      <div class="section-header">
        <h2 class="text-h5 font-weight-bold mb-0">Recommended Games</h2>
        <v-chip color="success" variant="outlined">{{ games.length }} games</v-chip>
      </div>
      <TransitionGroup name="list" tag="div" class="games-grid">
        <v-sheet v-for="(game, index) in games" :key="game.id" class="game-result">
          <GameSearchResultCard :game="game" @add-to-list="(listId) => addGame(game.id, listId, index)" />
        </v-sheet>
      </TransitionGroup>
    </div>

    <div v-else-if="isLoading" class="state-panel">
      <v-progress-circular indeterminate color="primary" size="48"></v-progress-circular>
      <p class="text-body-1 mt-4 mb-0">Finding games for you...</p>
    </div>

    <div v-else-if="hasSearched" class="state-panel">
      <v-icon icon="mdi-controller-off" size="56" color="grey"></v-icon>
      <h2 class="text-h6 mt-3 mb-2">No recommendations found</h2>
      <p class="text-body-2 text-medium-emphasis mb-0">Try a wider year range or a different genre.</p>
    </div>

    <div v-else class="state-panel">
      <v-icon icon="mdi-lightbulb-on-outline" size="56" color="primary"></v-icon>
      <h2 class="text-h6 mt-3 mb-2">Ready when you are</h2>
      <p class="text-body-2 text-medium-emphasis mb-0">Set your preferences and get games to add to your lists.</p>
    </div>
  </v-container>
</template>

<script lang="ts" setup>
import axios from "axios";
import { computed, ref } from "vue";

import type { Game } from "../types";
import type { AxiosError } from "axios";
import type { Ref } from "vue";

import GameSearchResultCard from "../components/GameSearchResultCard.vue";
import { useAddToList } from "../composables/addToList";
import { AI_MAX_RATING, AI_MAX_RECOMMENDATIONS, AI_MIN_RECOMMENDATIONS, AI_MIN_YEAR, GAME_GENRES } from "../const";
import { getUrl } from "../helpers";
import { $toast } from "../toast";

type GameGenre = (typeof GAME_GENRES)[number];

interface RecommendationPreferences {
  preferredGenre: GameGenre | null;
  recommendationsNumber: number;
  minRating: number | undefined;
}

const games: Ref<Game[]> = ref([]);
const isLoading = ref(false);
const hasSearched = ref(false);
const currentYear = computed(() => new Date().getFullYear());
const yearRange = ref([2000, currentYear.value]);

const preferences: Ref<RecommendationPreferences> = ref({
  preferredGenre: null,
  recommendationsNumber: AI_MAX_RECOMMENDATIONS,
  minRating: undefined,
});

const { addToList } = useAddToList();

async function getRecommendations(): Promise<void> {
  hasSearched.value = true;
  isLoading.value = true;
  games.value = [];

  const params = new URLSearchParams();

  if (preferences.value.preferredGenre) {
    params.append("preferredGenre", preferences.value.preferredGenre);
  }

  if (preferences.value.minRating !== undefined && preferences.value.minRating > 0) {
    params.append("minRating", preferences.value.minRating.toString());
  }

  params.append("recommendationsNumber", preferences.value.recommendationsNumber.toString());
  params.append("yearStart", yearRange.value[0].toString());
  params.append("yearEnd", yearRange.value[1].toString());

  try {
    const response = await axios.get<Game[]>(getUrl("recommendations/"), { params });
    games.value = response.data;

    if (games.value.length === 0) {
      $toast.info("No recommendations found");
    } else {
      $toast.success(`Found ${games.value.length} recommendations`);
    }
  } catch (error) {
    console.log(error as AxiosError);
    $toast.error("Error getting recommendations");
  } finally {
    isLoading.value = false;
  }
}

function addGame(gameId: number, listId: number, index: number): void {
  addToList(gameId, listId)
    .then(() => {
      games.value.splice(index, 1);
      $toast.success("Game added");
    })
    .catch((error: AxiosError) => {
      console.log(error);
      $toast.error("Error adding a game");
    });
}
</script>

<style scoped>
.recommendations-page {
  max-width: 1180px;
}

.page-header {
  align-items: center;
  display: flex;
  gap: 1rem;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.preferences-card {
  border: 1px solid rgba(var(--v-border-color), var(--v-border-opacity));
  border-radius: 8px;
}

.field-label {
  color: rgba(var(--v-theme-on-surface), 0.78);
  display: block;
  font-size: 0.875rem;
  font-weight: 600;
  margin-bottom: 0.25rem;
}

.field-help {
  color: rgba(var(--v-theme-on-surface), 0.65);
  font-size: 0.875rem;
  margin-top: 0.25rem;
  text-align: center;
}

.actions-row {
  display: flex;
  justify-content: center;
  margin-top: 1rem;
}

.section-header {
  align-items: center;
  display: flex;
  flex-wrap: wrap;
  gap: 1rem;
  justify-content: space-between;
  margin-bottom: 1.5rem;
}

.games-grid {
  display: flex;
  flex-wrap: wrap;
}

.game-result {
  background: transparent;
}

.state-panel {
  align-items: center;
  display: flex;
  flex-direction: column;
  justify-content: center;
  min-height: 260px;
  padding: 2rem;
  text-align: center;
}

@media (max-width: 600px) {
  .page-header {
    align-items: flex-start;
    flex-direction: column;
  }
}
</style>
