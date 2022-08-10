import jwt_decode from "jwt-decode";
import { createRouter, createWebHistory } from "vue-router";

import type { JWTDecoded } from "./types";

import { useAuthStore } from "./stores/auth";
import AboutView from "./views/AboutView.vue";
import GamesView from "./views/GamesView.vue";
import LoginView from "./views/LoginView.vue";
import LogoutView from "./views/LogoutView.vue";
import SearchView from "./views/SearchView.vue";
import UserGamesView from "./views/UserGamesView.vue";
import UserPreferencesView from "./views/UserPreferencesView.vue";
import UsersView from "./views/UsersView.vue";

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
    // Use `!` because we know that access token is not null when user is logged in
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    const decodedToken: JWTDecoded = jwt_decode(user.accessToken!);
    // If token expired or is about to expire (in 30 minutes) we refresh it
    if (decodedToken.exp - Date.now() / 1000 < 30 * 60) {
      await refreshToken();
    }
  }
});
