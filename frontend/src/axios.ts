import axios, { AxiosError, AxiosRequestHeaders } from "axios";

import { router } from "./router";
import { useAuthStore } from "./stores/auth";

export function initAxios() {
  const headers: AxiosRequestHeaders = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
  };

  const { user, refreshToken } = useAuthStore();
  if (user.isLoggedIn) {
    // Use `!` because we know that access token is not null when user is logged in
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    headers.Authorization = `Bearer ${user.accessToken!}`;
  }

  axios.defaults.headers.common = headers;
  axios.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error: AxiosError) => {
      if (error.response.status === 401) {
        if (user.isLoggedIn) {
          if (error.response.code === "token_not_valid") {
            try {
              await refreshToken();
            } catch (err) {
              return Promise.reject(err);
            }
          }
          return Promise.reject(error);
        }
        void router.push("/login");
      }
      return Promise.reject(error);
    }
  );
}
