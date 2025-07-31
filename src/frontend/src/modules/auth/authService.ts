/*
 * ===================================================================
 * AUTH MODULE - AUDITORIA 360
 * ===================================================================
 * Descrição: Módulo para funcionalidades de autenticação
 * ===================================================================
 */

export interface User {
  id: string;
  name: string;
  email: string;
  role: "super_admin" | "contabilidade" | "cliente_final";
  permissions?: string[];
}

export interface AuthTokens {
  accessToken: string;
  refreshToken: string;
  expiresAt: number;
}

export class AuthService {
  private static instance: AuthService;
  private user: User | null = null;
  private tokens: AuthTokens | null = null;

  private constructor() {}

  static getInstance(): AuthService {
    if (!AuthService.instance) {
      AuthService.instance = new AuthService();
    }
    return AuthService.instance;
  }

  // Login
  async login(credentials: { email: string; password: string }): Promise<User> {
    try {
      // In a real app, this would make an API call
      const mockResponse = {
        user: {
          id: "1",
          name: "Demo User",
          email: credentials.email,
          role: "super_admin" as const,
          permissions: ["read", "write", "admin"],
        },
        tokens: {
          accessToken: "mock-access-token",
          refreshToken: "mock-refresh-token",
          expiresAt: Date.now() + 3600000, // 1 hour
        },
      };

      this.user = mockResponse.user;
      this.tokens = mockResponse.tokens;

      // Store in sessionStorage
      sessionStorage.setItem("authTokens", JSON.stringify(this.tokens));
      sessionStorage.setItem("user", JSON.stringify(this.user));

      return mockResponse.user;
    } catch (error) {
      console.error("Login error:", error);
      throw error;
    }
  }

  // Logout
  logout(): void {
    this.user = null;
    this.tokens = null;
    sessionStorage.removeItem("authTokens");
    sessionStorage.removeItem("user");
  }

  // Check if user is authenticated
  isAuthenticated(): boolean {
    if (!this.tokens) {
      this.loadFromStorage();
    }

    if (!this.tokens) {
      return false;
    }

    // Check if token is expired
    if (Date.now() > this.tokens.expiresAt) {
      this.logout();
      return false;
    }

    return true;
  }

  // Get current user
  getCurrentUser(): User | null {
    if (!this.user) {
      this.loadFromStorage();
    }
    return this.user;
  }

  // Get access token
  getAccessToken(): string | null {
    if (!this.tokens) {
      this.loadFromStorage();
    }
    return this.tokens?.accessToken || null;
  }

  // Load auth data from sessionStorage
  private loadFromStorage(): void {
    try {
      const tokensJson = sessionStorage.getItem("authTokens");
      const userJson = sessionStorage.getItem("user");

      if (tokensJson && userJson) {
        this.tokens = JSON.parse(tokensJson);
        this.user = JSON.parse(userJson);
      }
    } catch (error) {
      console.error("Error loading auth data from storage:", error);
      this.logout();
    }
  }
}

export const authService = AuthService.getInstance();
