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
  role: 'super_admin' | 'contabilidade' | 'cliente_final'; // Updated roles to match backend
  permissions?: string[];
  contabilidadeId?: string; // For hierarchy access control
  userType?: string; // Map from backend user_type
  fullName?: string; // From backend full_name
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
      // Make real API call to backend
  const response = await fetch('http://localhost:8001/api/login', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          username: credentials.email,
          password: credentials.password,
        }),
      });

      if (!response.ok) {
        throw new Error('Login failed');
      }

      const data = await response.json();
      
      // Map backend response to our User interface
      const user: User = {
        id: data.user.id.toString(),
        name: data.user.full_name || data.user.username,
        email: data.user.email,
        role: data.user.role, // Maps directly from backend
        permissions: [], // TODO: Get from backend when implemented
        contabilidadeId: data.user.contabilidadeId,
        userType: data.user.role,
        fullName: data.user.full_name,
      };

      // Store tokens
      this.tokens = {
        accessToken: data.token.access_token,
        refreshToken: '', // TODO: Implement refresh tokens
        expiresAt: Date.now() + (data.token.expires_in * 1000),
      };

      this.user = user;

      // Store in sessionStorage
      sessionStorage.setItem("authTokens", JSON.stringify(this.tokens));
      sessionStorage.setItem("user", JSON.stringify(this.user));

      return user;
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
