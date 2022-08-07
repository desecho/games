// Styles
import "x-axios-progress-bar/dist/nprogress.css";
import "./styles/styles.scss";

import axios from "axios";
import VueAxios from "vue-axios";
import { createApp } from "vue";
import { loadProgressBar } from "x-axios-progress-bar";
import { createPinia } from "pinia";
import VueGtag from "vue-gtag";

import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import { initAxios } from "./axios";
import { router } from "./router";
import App from "./App.vue";

await loadFonts().catch(() => {
  throw new Error("Failed to load fonts");
});

loadProgressBar();

const app = createApp(App);
app
  .use(vuetify)
  .use(createPinia())
  .use(router)
  .use(VueGtag, { config: { id: import.meta.env.VITE_GOOGLE_ANALYTICS_ID } }, router)
  .use(VueAxios, axios);

app.provide("axios", app.config.globalProperties.axios).mount("#app");

initAxios();
