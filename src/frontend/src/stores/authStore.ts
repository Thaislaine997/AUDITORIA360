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
      // This would typically call your auth service
      const user = await authService.login(credentials);
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
      // Verifica se há usuário e token válidos no sessionStorage
      const userJson = sessionStorage.getItem("user");
      const tokensJson = sessionStorage.getItem("authTokens");
      if (userJson && tokensJson) {
        const user = JSON.parse(userJson);
        set({
          isAuthenticated: true,
          user,
          loading: false,
          permissions: user.permissions || []
        });
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