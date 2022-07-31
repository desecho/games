import { createRouter, createWebHistory } from "vue-router";
import jwt_decode from "jwt-decode";

import { useAuthStore } from "./stores/auth";
import { JWTDecoded } from "./types";
import LoginView from "./views/LoginView.vue";
import LogoutView from "./views/LogoutView.vue";
import GamesView from "./views/GamesView.vue";
import UsersView from "./views/UsersView.vue";
import UserGamesView from "./views/UserGamesView.vue";
import UserPreferencesView from "./views/UserPreferencesView.vue";
import SearchView from "./views/SearchView.vue";
import AboutView from "./views/AboutView.vue";

export const router = createRouter({
  history: createWebHistory(),
  linkActiveClass: "active",
  routes: [
    { path: "/", component: SearchView },
    { path: "/games", component: GamesView },
    { path: "/games/:listKey", component: GamesView, props: true },
    { path: "/about", component: AboutView },
    { path: "/users/:username", component: UserGamesView, props: true },
    { path: "/users/:username/:listKey", component: UserGamesView, props: true },
    { path: "/users", component: UsersView },
    { path: "/preferences", component: UserPreferencesView },
    { path: "/login", component: LoginView },
    { path: "/logout", component: LogoutView },
  ],
});

router.beforeEach(async (to) => {
  const privatePages = ["/games", "/preferences"];
  const authRequired = privatePages.includes(to.path);
  const { user, refreshToken } = useAuthStore();

  if (authRequired && !user.isLoggedIn) {
    return "/login";
  }

  if (user.isLoggedIn) {
    const decodedToken: JWTDecoded = jwt_decode(user.accessToken!);
    // If token expired or is about to expire (in 30 minutes) we refresh it
    if (decodedToken.exp - Date.now() / 1000 < 30 * 60) {
      await refreshToken();
    }
  }
});
