import { config } from "@vue/test-utils";
import { vi } from "vitest";

// Mock Vuetify components to avoid CSS loading issues
vi.mock("vuetify/components", () => ({
  VCard: { template: '<div class="v-card"><slot /></div>' },
  VCardActions: { template: '<div class="v-card-actions"><slot /></div>' },
  VSpacer: { template: '<div class="v-spacer"></div>' },
}));

// Mock CSS files
vi.mock("*.css", () => ({}));
vi.mock("*.scss", () => ({}));

// Create simple stubs for Vuetify components
const VuetifyStubs = {
  VCard: {
    template: '<div class="v-card" :width="width" :height="height"><slot /></div>',
    props: ["width", "height"],
  },
  VCardActions: {
    template: '<div class="v-card-actions"><slot /></div>',
  },
  VSpacer: {
    template: '<div class="v-spacer"></div>',
  },
};

// Configure Vue Test Utils globally
config.global.stubs = VuetifyStubs;
