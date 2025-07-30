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

export const useAuthStore = create<AuthState>((set, get) => ({
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
      const isAuthenticated = authService.isAuthenticated();
      const user = authService.getCurrentUser();
      
      set({
        isAuthenticated,
        user: user || null,
        loading: false,
        permissions: user?.permissions || []
      });
    } catch (error) {
      console.error('Auth check failed:', error);
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