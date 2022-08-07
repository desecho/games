import { router } from "./router";
import { useAuthStore } from "./stores/auth";

export const rulesHelper = {
  required: (value: string) => !!value || "Required.",
};

export function getUrl(path: string): string {
  const baseUrl: string = import.meta.env.VITE_BACKEND_URL;
  return `${baseUrl}${path}`;
}

export function requireAuthenticated() {
  const { user } = useAuthStore();
  if (!user.isLoggedIn) {
    router.push("/login").catch(() => {});
    return;
  }
}

// eslint-disable-next-line @typescript-eslint/no-explicit-any
export function rewriteArray(arrayToRewrite: any[], newArray: any[]) {
  while (arrayToRewrite.length > 0) {
    arrayToRewrite.pop();
  }
  newArray.forEach((item) => {
    arrayToRewrite.push(item);
  });
}
