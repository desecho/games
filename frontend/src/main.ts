// Styles
import "vue-toast-notification/dist/theme-default.css";
import "x-axios-progress-bar/dist/nprogress.css";
import "./styles/styles.scss";

import axios from "axios";
import VueAxios from "vue-axios";
import { createApp } from "vue";
import { loadProgressBar } from "x-axios-progress-bar";
import { createPinia } from "pinia";
import VueToast from "vue-toast-notification";
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

createApp(App)
  .use(vuetify)
  .use(createPinia())
  .use(router)
  .use(VueGtag, { config: { id: import.meta.env.VITE_GOOGLE_ANALYTICS_ID } }, router)
  .use(VueAxios, axios)
  .use(VueToast, {
    position: "bottom-right",
    duration: 1500,
  })
  .mount("#app");

initAxios();
