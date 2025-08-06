import { create } from 'zustand';

type LayoutMode = 'comfortable' | 'compact';

interface UIState {
  sidebarOpen: boolean;
  currentPage: string;
  layoutMode: LayoutMode; // Fluxo Layout Mode
  notifications: Array<{
    id: string;
    message: string;
    type: 'info' | 'success' | 'warning' | 'error';
    timestamp: Date;
  }>;
  
  // Actions
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setCurrentPage: (page: string) => void;
  setLayoutMode: (mode: LayoutMode) => void; // Fluxo Layout Mode setter
  toggleLayoutMode: () => void; // Fluxo Layout Mode toggle
  addNotification: (notification: Omit<UIState['notifications'][0], 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
}

export const useUIStore = create<UIState>((set, get) => ({
  sidebarOpen: true,
  currentPage: '/dashboard',
  layoutMode: 'comfortable', // Fluxo default layout mode
  notifications: [],

  toggleSidebar: () => {
    const { sidebarOpen } = get();
    set({ sidebarOpen: !sidebarOpen });
  },

  setSidebarOpen: (open) => {
    set({ sidebarOpen: open });
  },

  setCurrentPage: (page) => {
    set({ currentPage: page });
  },

  // Fluxo Layout Mode management
  setLayoutMode: (mode) => {
    set({ layoutMode: mode });
    // Apply layout mode class to body for global CSS effects
    document.body.className = document.body.className.replace(/fluxo-layout-\w+/g, '');
    document.body.classList.add(`fluxo-layout-${mode}`);
  },

  toggleLayoutMode: () => {
    const { layoutMode, setLayoutMode } = get();
    const newMode = layoutMode === 'comfortable' ? 'compact' : 'comfortable';
    setLayoutMode(newMode);
  },

  addNotification: (notification) => {
    const id = Math.random().toString(36).substr(2, 9);
    const newNotification = {
      ...notification,
      id,
      timestamp: new Date(),
    };
    
    set((state) => ({
      notifications: [...state.notifications, newNotification],
    }));
  },

  removeNotification: (id) => {
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    }));
  },

  clearNotifications: () => {
    set({ notifications: [] });
  },
}));