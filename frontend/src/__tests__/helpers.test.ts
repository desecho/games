import { createPinia, setActivePinia } from "pinia";
import { beforeEach, describe, expect, it, vi } from "vitest";

import { getUrl, requireAuthenticated, rewriteArray, rulesHelper } from "../helpers";
import { useAuthStore } from "../stores/auth";

// Mock router
vi.mock("../router", () => ({
  router: {
    push: vi.fn(),
  },
}));

// Mock environment variable
vi.stubEnv("VITE_BACKEND_URL", "http://localhost:8000/api/");

describe("helpers", () => {
  beforeEach(() => {
    setActivePinia(createPinia());
    vi.clearAllMocks();
  });

  describe("rulesHelper", () => {
    it("returns true for valid non-empty string", () => {
      expect(rulesHelper.required("test")).toBe(true);
    });

    it('returns "Required" for empty string', () => {
      expect(rulesHelper.required("")).toBe("Required");
    });

    it("returns true for whitespace-only string (truthy)", () => {
      expect(rulesHelper.required("   ")).toBe(true);
    });
  });

  describe("getUrl", () => {
    it("constructs correct URL", () => {
      const result = getUrl("games/");
      expect(result).toBe("http://localhost:8000/api/games/");
    });

    it("handles path without trailing slash", () => {
      const result = getUrl("users");
      expect(result).toBe("http://localhost:8000/api/users");
    });
  });

  describe("requireAuthenticated", () => {
    it("does not redirect when user is logged in", async () => {
      const authStore = useAuthStore();
      authStore.user = { isLoggedIn: true };

      requireAuthenticated();

      const { router } = await import("../router");
      expect(router.push).not.toHaveBeenCalled();
    });

    it("redirects to login when user is not logged in", async () => {
      const authStore = useAuthStore();
      authStore.user = { isLoggedIn: false };

      requireAuthenticated();

      const { router } = await import("../router");
      expect(router.push).toHaveBeenCalledWith("/login");
    });
  });

  describe("rewriteArray", () => {
    it("replaces array contents", () => {
      const originalArray = [1, 2, 3];
      const newArray = [4, 5, 6];

      rewriteArray(originalArray, newArray);

      expect(originalArray).toEqual([4, 5, 6]);
    });

    it("handles empty new array", () => {
      const originalArray = [1, 2, 3];
      const newArray: number[] = [];

      rewriteArray(originalArray, newArray);

      expect(originalArray).toEqual([]);
    });

    it("handles empty original array", () => {
      const originalArray: number[] = [];
      const newArray = [1, 2, 3];

      rewriteArray(originalArray, newArray);

      expect(originalArray).toEqual([1, 2, 3]);
    });
  });
});
