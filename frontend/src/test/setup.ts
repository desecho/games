import { config } from "@vue/test-utils";
import { vi } from "vitest";

// Mock Vuetify components to avoid CSS loading issues
vi.mock("vuetify/components", () => ({
  VCard: { template: '<div class="v-card"><slot /></div>' },
  VCardActions: { template: '<div class="v-card-actions"><slot /></div>' },
  VSpacer: { template: '<div class="v-spacer"></div>' },
  VRating: { template: '<div class="v-rating"><slot /></div>' },
  VImg: { template: '<div class="v-img"><slot /></div>' },
  VCardSubtitle: { template: '<div class="v-card-subtitle"><slot /></div>' },
  VBtn: { template: '<button class="v-btn"><slot /></button>' },
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
  VImg: {
    template: '<div class="v-img"><slot /></div>',
    props: ["src", "title", "alt", "height", "class"],
  },
  VCardSubtitle: {
    template: '<div class="v-card-subtitle"><slot /></div>',
  },
  VBtn: {
    template: '<button class="v-btn" :title="title" :disabled="disabled"><slot /></button>',
    props: ["size", "color", "density", "variant", "icon", "title", "disabled", "active", "width"],
  },
  VRating: {
    name: "VRating",
    template: [
      '<div class="v-rating"',
      ' :data-model-value="modelValue"',
      ' :data-readonly="readonly"',
      ' :data-clearable="clearable"',
      ' :title="title"',
      " @click=\"$emit('update:modelValue', 5)\"",
      "><slot /></div>",
    ].join(""),
    props: [
      "modelValue",
      "readonly",
      "clearable",
      "hover",
      "title",
      "color",
      "activeColor",
      "density",
      "size",
      "length",
      "ripple",
    ],
    emits: ["update:modelValue"],
  },
};

// Configure Vue Test Utils globally
config.global.stubs = VuetifyStubs;
