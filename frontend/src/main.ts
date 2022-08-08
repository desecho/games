// Styles
import "x-axios-progress-bar/dist/nprogress.css";
import "./styles/styles.scss";

import axios from "axios";
import { createPinia } from "pinia";
import { createApp } from "vue";
import VueAxios from "vue-axios";
import VueGtag from "vue-gtag";
import { loadProgressBar } from "x-axios-progress-bar";

import App from "./App.vue";
import { initAxios } from "./axios";
import vuetify from "./plugins/vuetify";
import { loadFonts } from "./plugins/webfontloader";
import { router } from "./router";

await loadFonts().catch(() => {
  throw new Error("Failed to load fonts");
});

loadProgressBar();

const app = createApp(App);
app
  // eslint-disable-next-line @typescript-eslint/no-unsafe-argument
  .use(vuetify)
  .use(createPinia())
  .use(router)
  .use(VueGtag, { config: { id: import.meta.env.VITE_GOOGLE_ANALYTICS_ID as string } }, router)
  .use(VueAxios, axios);

app.provide("axios", app.config.globalProperties.axios).mount("#app");

initAxios();
