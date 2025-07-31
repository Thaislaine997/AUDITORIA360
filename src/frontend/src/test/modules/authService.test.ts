import { describe, it, expect, beforeEach, vi } from "vitest";
import { authService } from "../../modules/auth/authService";

// Mock sessionStorage for testing
const sessionStorageMock = (() => {
  let store: Record<string, string> = {};

  return {
    getItem: (key: string) => {
      return store[key] || null;
    },
    setItem: (key: string, value: string) => {
      store[key] = value.toString();
    },
    removeItem: (key: string) => {
      delete store[key];
    },
    clear: () => {
      store = {};
    }
  };
})();

Object.defineProperty(window, 'sessionStorage', {
  value: sessionStorageMock
});

describe("AuthService sessionStorage behavior", () => {
  beforeEach(() => {
    // Clear sessionStorage before each test
    sessionStorageMock.clear();
    
    // Reset authService internal state
    authService.logout();
  });

  it("stores authentication data in sessionStorage on login", async () => {
    const credentials = { email: "test@example.com", password: "password" };
    
    await authService.login(credentials.email, credentials.password);
    
    // Verify data is stored in sessionStorage
    const storedTokens = sessionStorageMock.getItem("authTokens");
    const storedUser = sessionStorageMock.getItem("user");
    
    expect(storedTokens).toBeTruthy();
    expect(storedUser).toBeTruthy();
    
    const parsedTokens = JSON.parse(storedTokens!);
    const parsedUser = JSON.parse(storedUser!);
    
    expect(parsedTokens.accessToken).toBe("mock-access-token");
    expect(parsedUser.email).toBe("demo@auditoria360.com");
  });

  it("removes authentication data from sessionStorage on logout", async () => {
    // First login to store data
    await authService.login("test@example.com", "password");
    
    // Verify data exists
    expect(sessionStorageMock.getItem("authTokens")).toBeTruthy();
    expect(sessionStorageMock.getItem("user")).toBeTruthy();
    
    // Logout
    authService.logout();
    
    // Verify data is removed
    expect(sessionStorageMock.getItem("authTokens")).toBeNull();
    expect(sessionStorageMock.getItem("user")).toBeNull();
  });

  it("loads authentication data from sessionStorage", async () => {
    // Manually store data in sessionStorage
    const mockTokens = {
      accessToken: "stored-token",
      refreshToken: "stored-refresh-token",
      expiresAt: Date.now() + 3600000
    };
    const mockUser = {
      id: "stored-user-id",
      name: "Stored User",
      email: "stored@example.com",
      role: "admin" as const
    };
    
    sessionStorageMock.setItem("authTokens", JSON.stringify(mockTokens));
    sessionStorageMock.setItem("user", JSON.stringify(mockUser));
    
    // Check if user is authenticated (this triggers loading from storage)
    const isAuthenticated = authService.isAuthenticated();
    const currentUser = authService.getCurrentUser();
    
    expect(isAuthenticated).toBe(true);
    expect(currentUser).toEqual(mockUser);
    expect(authService.getAccessToken()).toBe("stored-token");
  });

  it("handles expired tokens correctly", () => {
    // Store expired token
    const expiredTokens = {
      accessToken: "expired-token",
      refreshToken: "expired-refresh-token",
      expiresAt: Date.now() - 1000 // Expired 1 second ago
    };
    
    sessionStorageMock.setItem("authTokens", JSON.stringify(expiredTokens));
    sessionStorageMock.setItem("user", JSON.stringify({ id: "1", name: "User" }));
    
    // Check authentication with expired token
    const isAuthenticated = authService.isAuthenticated();
    
    expect(isAuthenticated).toBe(false);
    // Verify logout was called and data was cleaned up
    expect(sessionStorageMock.getItem("authTokens")).toBeNull();
    expect(sessionStorageMock.getItem("user")).toBeNull();
  });

  it("handles corrupted storage data gracefully", () => {
    // Store invalid JSON
    sessionStorageMock.setItem("authTokens", "invalid-json");
    sessionStorageMock.setItem("user", "also-invalid");
    
    const consoleSpy = vi.spyOn(console, "error").mockImplementation(() => {});
    
    // This should not throw and should handle the error gracefully
    const isAuthenticated = authService.isAuthenticated();
    const currentUser = authService.getCurrentUser();
    
    expect(isAuthenticated).toBe(false);
    expect(currentUser).toBeNull();
    expect(consoleSpy).toHaveBeenCalledWith(
      "Error loading auth data from storage:",
      expect.any(Error)
    );
    
    consoleSpy.mockRestore();
  });

  it("confirms sessionStorage (not localStorage) is being used", async () => {
    // Mock localStorage to ensure it's not being used
    const localStorageSpy = vi.spyOn(Storage.prototype, 'setItem');
    
    await authService.login("test@example.com", "password");
    
    // Verify localStorage was not called
    expect(localStorageSpy).not.toHaveBeenCalled();
    
    // Verify sessionStorage has the data
    expect(sessionStorageMock.getItem("authTokens")).toBeTruthy();
    expect(sessionStorageMock.getItem("user")).toBeTruthy();
    
    localStorageSpy.mockRestore();
  });
});