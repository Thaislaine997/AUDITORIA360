import { describe, it, expect, beforeEach, jest } from "@jest/globals";
import { renderHook, waitFor } from "@testing-library/react";
import { useAuth } from "../../hooks/useAuth";
import { useAuthStore } from "../../stores/authStore";

// Mock authService
jest.mock("../../modules/auth/authService", () => ({
  authService: {
    isAuthenticated: jest.fn(),
    getCurrentUser: jest.fn(),
    login: jest.fn(),
    logout: jest.fn(),
  },
}));

import { authService } from "../../modules/auth/authService";

const mockAuthService = authService as jest.Mocked<typeof authService>;

describe("useAuth Hook", () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Reset store state
    useAuthStore.setState({
      user: null,
      isAuthenticated: false,
      loading: true,
      permissions: [],
    });
  });

  it("returns initial loading state and completes auth check", async () => {
    mockAuthService.isAuthenticated.mockReturnValue(false);
    mockAuthService.getCurrentUser.mockReturnValue(null);

    const { result } = renderHook(() => useAuth());

    // Initially loading should be true
    expect(result.current.loading).toBe(true);

    // Trigger auth check manually
    await result.current.checkAuth();

    expect(result.current.loading).toBe(false);
    expect(result.current.isAuthenticated).toBe(false);
  });

  it("returns authenticated state when user is logged in", async () => {
    const mockUser = {
      id: "1",
      name: "Test User",
      email: "test@example.com",
      role: "admin" as const,
      permissions: ["read", "write"],
    };

    mockAuthService.isAuthenticated.mockReturnValue(true);
    mockAuthService.getCurrentUser.mockReturnValue(mockUser);

    const { result } = renderHook(() => useAuth());

    await result.current.checkAuth();

    expect(result.current.loading).toBe(false);
    expect(result.current.isAuthenticated).toBe(true);
    expect(result.current.user).toEqual(mockUser);
  });

  it("returns unauthenticated state when user is not logged in", async () => {
    mockAuthService.isAuthenticated.mockReturnValue(false);
    mockAuthService.getCurrentUser.mockReturnValue(null);

    const { result } = renderHook(() => useAuth());

    await result.current.checkAuth();

    expect(result.current.loading).toBe(false);
    expect(result.current.isAuthenticated).toBe(false);
    expect(result.current.user).toBe(null);
  });

  it("handles auth check errors gracefully", async () => {
    mockAuthService.isAuthenticated.mockImplementation(() => {
      throw new Error("Auth check failed");
    });

    const consoleSpy = jest.spyOn(console, "error").mockImplementation(() => {});

    const { result } = renderHook(() => useAuth());

    await result.current.checkAuth();

    expect(result.current.loading).toBe(false);
    expect(result.current.isAuthenticated).toBe(false);
    expect(consoleSpy).toHaveBeenCalledWith(
      "Auth check failed:",
      expect.any(Error)
    );

    consoleSpy.mockRestore();
  });
});
