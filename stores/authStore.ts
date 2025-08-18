import { create } from 'zustand';
import { authService, type User } from '../modules/auth/authService';

interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  loading: boolean;
  permissions: string[];
  
  // Actions
  login: (credentials: { email: string; password: string }) => Promise<void>;
  logout: () => void;
  checkAuth: () => Promise<void>;
  setUser: (user: User | null) => void;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  isAuthenticated: false,
  loading: true,
  permissions: [],

  login: async (credentials) => {
    set({ loading: true });
    try {
      const user = await authService.login(credentials);
      // Persistência do usuário no sessionStorage
  sessionStorage.setItem("user", JSON.stringify(user));
  // Salva timestamp de login para expiração automática
  sessionStorage.setItem("loginTime", Date.now().toString());
      set({ 
        user, 
        isAuthenticated: true, 
        loading: false,
        permissions: user?.permissions || []
      });
    } catch (error) {
      set({ loading: false });
      throw error;
    }
  },

  logout: () => {
    authService.logout();
  sessionStorage.removeItem("user");
  sessionStorage.removeItem("authTokens");
  sessionStorage.removeItem("loginTime");
    set({ 
      user: null, 
      isAuthenticated: false, 
      loading: false,
      permissions: []
    });
  },

  checkAuth: async () => {
    set({ loading: true });
    try {
  const userJson = sessionStorage.getItem("user");
  const loginTime = sessionStorage.getItem("loginTime");
      const EXPIRATION_MINUTES = 30;
      if (userJson && loginTime) {
        const user = JSON.parse(userJson);
        const now = Date.now();
        const loginTimestamp = parseInt(loginTime, 10);
        if (now - loginTimestamp > EXPIRATION_MINUTES * 60 * 1000) {
          // Sessão expirada
          sessionStorage.removeItem("user");
          sessionStorage.removeItem("authTokens");
          sessionStorage.removeItem("loginTime");
          set({
            isAuthenticated: false,
            user: null,
            loading: false,
            permissions: []
          });
          // Sinaliza expiração para o app
          window.dispatchEvent(new Event("sessionExpired"));
        } else {
          set({
            isAuthenticated: true,
            user,
            loading: false,
            permissions: user.permissions || []
          });
        }
      } else {
        set({
          isAuthenticated: false,
          user: null,
          loading: false,
          permissions: []
        });
      }
    } catch (error) {
      set({
        isAuthenticated: false,
        user: null,
        loading: false,
        permissions: []
      });
    }
  },

  setUser: (user) => {
    set({ 
      user, 
      isAuthenticated: !!user,
      permissions: user?.permissions || []
    });
  },
}));