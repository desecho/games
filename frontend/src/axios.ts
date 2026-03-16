import axios from "axios";

import type { AxiosError } from "axios";

import { router } from "./router";
import { useAuthStore } from "./stores/auth";

export function initAxios(): void {
  axios.defaults.headers.common["Content-Type"] = "application/json; charset=UTF-8";
  axios.defaults.headers.common["X-Requested-With"] = "XMLHttpRequest";

  const { user, refreshToken } = useAuthStore();
  if (user.isLoggedIn) {
    // Use `!` because we know that access token is not null when user is logged in
    // eslint-disable-next-line @typescript-eslint/no-non-null-assertion
    axios.defaults.headers.common.Authorization = `Bearer ${user.accessToken!}`;
  }

  axios.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error: AxiosError) => {
      if (error.response?.status === 401) {
        if (user.isLoggedIn) {
          if ((error.response.data as { code?: string })?.code === "token_not_valid") {
            try {
              await refreshToken();
            } catch (err) {
              // eslint-disable-next-line @typescript-eslint/prefer-promise-reject-errors
              return Promise.reject(err);
            }
          }
          return Promise.reject(error);
        }
        void router.push("/login");
      }
      return Promise.reject(error);
    },
  );
}
