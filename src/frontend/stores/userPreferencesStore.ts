import { create } from 'zustand';
import { persist } from 'zustand/middleware';

interface UserPreferences {
  theme: 'light' | 'dark' | 'auto';
  accentColor: string;
  language: 'pt-BR' | 'en' | 'es';
  timezone: string;
  dashboardLayout: string;
  sidebarCollapsed: boolean;
  notificationsEnabled: boolean;
  
  // Actions
  setTheme: (theme: UserPreferences['theme']) => void;
  setAccentColor: (color: string) => void;
  setLanguage: (language: UserPreferences['language']) => void;
  setTimezone: (timezone: string) => void;
  setDashboardLayout: (layout: string) => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  setNotificationsEnabled: (enabled: boolean) => void;
  resetToDefaults: () => void;
}

const defaultPreferences = {
  theme: 'light' as const,
  accentColor: '#1976d2',
  language: 'pt-BR' as const,
  timezone: 'America/Sao_Paulo',
  dashboardLayout: 'default',
  sidebarCollapsed: false,
  notificationsEnabled: true,
};

export const useUserPreferencesStore = create<UserPreferences>()(
  persist(
    (set, get) => ({
      ...defaultPreferences,

      setTheme: (theme) => {
        set({ theme });
      },

      setAccentColor: (accentColor) => {
        set({ accentColor });
      },

      setLanguage: (language) => {
        set({ language });
      },

      setTimezone: (timezone) => {
        set({ timezone });
      },

      setDashboardLayout: (dashboardLayout) => {
        set({ dashboardLayout });
      },

      setSidebarCollapsed: (sidebarCollapsed) => {
        set({ sidebarCollapsed });
      },

      setNotificationsEnabled: (notificationsEnabled) => {
        set({ notificationsEnabled });
      },

      resetToDefaults: () => {
        set(defaultPreferences);
      },
    }),
    {
      name: 'user-preferences',
    }
  )
);