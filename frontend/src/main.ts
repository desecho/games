// Styles
// eslint-disable-next-line import/no-unassigned-import
import "x-axios-progress-bar/dist/nprogress.css";
// eslint-disable-next-line import/no-unassigned-import
import "./styles/styles.scss";

import { createPinia } from "pinia";
import { createApp } from "vue";
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

createApp(App)
  .use(vuetify)
  .use(createPinia())
  .use(router)
  .use(VueGtag, { config: { id: import.meta.env.VITE_GOOGLE_ANALYTICS_ID as string } }, router)
  .mount("#app");

/* Not entirely sure I need to init axios here.
   This has to be after creating an app because of pinia */
initAxios();
