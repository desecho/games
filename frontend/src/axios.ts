import { AxiosRequestHeaders } from "axios";
import { useAuthStore } from "./stores/auth";
import axios from "axios";
import { router } from "./router";

export function initAxios() {
  const headers: AxiosRequestHeaders = {
    "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
    "X-Requested-With": "XMLHttpRequest",
  };

  const { user, refreshToken } = useAuthStore();
  if (user.isLoggedIn) {
    headers.Authorization = `Bearer ${user.accessToken!}`;
  }

  axios.defaults.headers.common = headers;
  axios.interceptors.response.use(
    (response) => {
      return response;
    },
    async (error) => {
      if ("response" in error && "status" in error.response && error.response.status === 401) {
        if (user.isLoggedIn) {
          if ("code" in error.response && error.response.code === "token_not_valid") {
            try {
              await refreshToken();
            } catch (error) {
              return Promise.reject(error);
            }
          }
          return Promise.reject(error);
        } else {
          router.push("/login").catch(() => {});
        }
        return Promise.reject(error);
      }
      return Promise.reject(error);
    }
  );
}
