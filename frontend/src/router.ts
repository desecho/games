import { jwtDecode } from "jwt-decode";
import { createRouter, createWebHistory } from "vue-router";

import type { AuthProps, JWTDecoded } from "./types";
import type { RouteLocationNormalized } from "vue-router";

import { useAuthStore } from "./stores/auth";
import AboutView from "./views/AboutView.vue";
import ChangePasswordView from "./views/ChangePasswordView.vue";
import GamesView from "./views/GamesView.vue";
import LoginView from "./views/LoginView.vue";
import LogoutView from "./views/LogoutView.vue";
import RegistrationView from "./views/RegistrationView.vue";
import ResetPasswordRequestView from "./views/ResetPasswordRequestView.vue";
import ResetPasswordView from "./views/ResetPasswordView.vue";
import SearchView from "./views/SearchView.vue";
import UserGamesView from "./views/UserGamesView.vue";
import UserPreferencesView from "./views/UserPreferencesView.vue";
import UsersView from "./views/UsersView.vue";
import VerifyUserView from "./views/VerifyUserView.vue";

function authProps(route: RouteLocationNormalized): AuthProps {
  return {
    userId: route.query.user_id as unknown as number,
    timestamp: route.query.timestamp as unknown as number,
    signature: route.query.signature as unknown as string,
  };
}

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
    { path: "/register", component: RegistrationView },
    {
      path: "/verify-user",
      component: VerifyUserView,
      props: authProps,
    },
    {
      path: "/reset-password",
      component: ResetPasswordView,
      props: authProps,
    },
    { path: "/reset-password-request", component: ResetPasswordRequestView },
    { path: "/change-password", component: ChangePasswordView },
  ],
});

router.beforeEach(async (to) => {
  const privatePages = ["/games", "/preferences", "/change-password"];
  const authRequired = privatePages.includes(to.path);
  const { user, refreshToken } = useAuthStore();

  if (authRequired && !user.isLoggedIn) {
    return "/login";
  }

  if (user.isLoggedIn) {
    // Use `!` because we know that access token is not null when user is logged in
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    const decodedToken: JWTDecoded = jwtDecode(user.accessToken!);
    // If token expired or is about to expire (in 30 minutes) we refresh it
    if (decodedToken.exp - Date.now() / 1000 < 30 * 60) {
      await refreshToken();
    }
  }
});
