import { defineStore } from "pinia";
import jwt_decode from "jwt-decode";
import axios from "axios";

import { JWTDecoded } from "../types";
import { router } from "../router";
import { getUrl } from "../helpers";
import { initAxios } from "../axios";
import { UserStore, TokenData, TokenRefreshData } from "./types";

const userDefault: UserStore = {
  isLoggedIn: false,
};

function getUser(): UserStore {
  const userLocalStorageData = localStorage.getItem("user");
  if (userLocalStorageData) {
    const user = JSON.parse(userLocalStorageData) as UserStore;
    return user;
  }
  return userDefault;
}

function saveUser(user: UserStore) {
  localStorage.setItem("user", JSON.stringify(user));
}

export const useAuthStore = defineStore({
  id: "auth",
  state: () => ({
    // TODO - maybe refactor this and have isLoggedIn be separate from user
    user: getUser(),
  }),
  actions: {
    async login(username: string, password: string) {
      const response = await axios.post(getUrl("token/"), { username: username, password: password });
      const data = response.data as TokenData;
      this.user = {
        refreshToken: data.refresh,
        accessToken: data.access,
        isLoggedIn: true,
        username: username,
      };
      saveUser(this.user);
      initAxios();
      router.push("/").catch(() => {});
    },
    // This function needs to be called only when user is logged in
    async refreshToken() {
      // Use `!` because we know that refresh token is not null when user is logged in
      // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
      const decodedToken: JWTDecoded = jwt_decode(this.user.refreshToken!);
      // If refresh token expired we log the user out
      if (decodedToken.exp < Date.now() / 1000) {
        this.logout();
        return;
      }

      const response = await axios.post(getUrl("token/refresh/"), { refresh: this.user.refreshToken });
      const data = response.data as TokenRefreshData;
      this.user.accessToken = data.access;
      saveUser(this.user);
      initAxios();
    },
    logout() {
      this.user = userDefault;
      localStorage.removeItem("user");
      initAxios();
      router.push("/").catch(() => {});
    },
  },
});
