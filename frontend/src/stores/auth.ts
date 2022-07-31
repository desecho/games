import { defineStore } from "pinia";
import jwt_decode from "jwt-decode";
import axios from "axios";

import { UserStore, JWTDecoded } from "../types";
import { router } from "../router";
import { getUrl } from "../helpers";
import { initAxios } from "../axios";

const userDefault: UserStore = {
  isLoggedIn: false,
};

function getUser(): UserStore {
  const userLocalStorageData = localStorage.getItem("user");
  if (userLocalStorageData) {
    const user: UserStore = JSON.parse(userLocalStorageData);
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
    user: getUser(),
  }),
  actions: {
    async login(username: string, password: string) {
      const response = await axios.post(getUrl("token/"), { username: username, password: password });
      this.user = {
        refreshToken: response.data.refresh,
        accessToken: response.data.access,
        isLoggedIn: true,
        username: username,
      };
      saveUser(this.user);
      initAxios();
      router.push("/").catch(() => {});
    },
    async refreshToken() {
      const decodedToken: JWTDecoded = jwt_decode(this.user.refreshToken!);
      // If refresh token expired we log the user out
      if (decodedToken.exp < Date.now() / 1000) {
        this.logout();
        return;
      }

      const response = await axios.post(getUrl("token/refresh/"), { refresh: this.user.refreshToken });
      this.user.accessToken = response.data.access;
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
