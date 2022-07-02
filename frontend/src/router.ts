import { createRouter, createWebHistory } from "vue-router";
import LoginView from "./views/LoginView.vue";
import LogoutView from "./views/LogoutView.vue";
import GamesView from "./views/GamesView.vue";
import SearchView from "./views/SearchView.vue";
import AboutView from "./views/AboutView.vue";
import { useAuthStore } from "./stores/auth";
import jwt_decode from "jwt-decode";
import { JWTDecoded } from "./types";

export const router = createRouter({
  history: createWebHistory(),
  linkActiveClass: "active",
  routes: [
    { path: "/", component: SearchView },
    { path: "/games", component: GamesView },
    { path: "/games/:listKey", component: GamesView, props: true },
    { path: "/about", component: AboutView },
    { path: "/login", component: LoginView },
    { path: "/logout", component: LogoutView },
  ],
});

router.beforeEach(async (to) => {
  const privatePages = ["/games"];
  const authRequired = privatePages.includes(to.path);
  const { user, refreshToken } = useAuthStore();

  if (authRequired && !user.isLoggedIn) {
    return "/login";
  }

  if (user.isLoggedIn) {
    const decodedToken: JWTDecoded = jwt_decode(user.accessToken!);
    // If token expired or about to expire (in 30 minutes) we refresh it
    if (decodedToken.exp - Date.now() / 1000 < 30 * 60) {
      await refreshToken();
    }
  }
});
