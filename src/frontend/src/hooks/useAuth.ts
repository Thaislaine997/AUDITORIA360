import { useState, useEffect } from "react";
import { authService, type User } from "../modules/auth/authService";

interface AuthState {
  isAuthenticated: boolean;
  loading: boolean;
  user?: User;
}

export const useAuth = (): AuthState => {
  const [authState, setAuthState] = useState<AuthState>({
    isAuthenticated: false,
    loading: true,
  });

  useEffect(() => {
    const checkAuth = async () => {
      try {
        const isAuthenticated = authService.isAuthenticated();
        const user = authService.getCurrentUser();

        setAuthState({
          isAuthenticated,
          loading: false,
          user: user || undefined,
        });
      } catch (error) {
        console.error("Auth check failed:", error);
        setAuthState({
          isAuthenticated: false,
          loading: false,
        });
      }
    };

    checkAuth();
  }, []);

  return authState;
};
