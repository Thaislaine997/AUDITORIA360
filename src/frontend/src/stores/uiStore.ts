import { create } from 'zustand';

interface UIState {
  sidebarOpen: boolean;
  currentPage: string;
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
  addNotification: (notification: Omit<UIState['notifications'][0], 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
}

export const useUIStore = create<UIState>((set, get) => ({
  sidebarOpen: true,
  currentPage: '/dashboard',
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