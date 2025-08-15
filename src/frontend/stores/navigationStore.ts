import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface NavigationItem {
  path: string;
  label: string;
  icon: string;
  category?: string;
  lastAccessed?: Date;
  accessCount: number;
}

interface NavigationState {
  favorites: NavigationItem[];
  recentlyAccessed: NavigationItem[];
  sidebarCollapsed: boolean;
  
  // Actions
  addToFavorites: (item: NavigationItem) => void;
  removeFromFavorites: (path: string) => void;
  isFavorite: (path: string) => boolean;
  recordAccess: (item: NavigationItem) => void;
  setSidebarCollapsed: (collapsed: boolean) => void;
  
  // Getters
  getMostAccessed: (limit?: number) => NavigationItem[];
  getRecentlyAccessed: (limit?: number) => NavigationItem[];
}

export const useNavigationStore = create<NavigationState>()(
  persist(
    (set, get) => ({
      favorites: [],
      recentlyAccessed: [],
      sidebarCollapsed: false,

      addToFavorites: (item) => {
        const { favorites } = get();
        const exists = favorites.find(fav => fav.path === item.path);
        
        if (!exists) {
          set({
            favorites: [...favorites, { ...item, lastAccessed: new Date() }],
          });
        }
      },

      removeFromFavorites: (path) => {
        set((state) => ({
          favorites: state.favorites.filter(fav => fav.path !== path),
        }));
      },

      isFavorite: (path) => {
        return get().favorites.some(fav => fav.path === path);
      },

      recordAccess: (item) => {
        set((state) => {
          const now = new Date();
          
          // Update recently accessed
          const existingIndex = state.recentlyAccessed.findIndex(
            recent => recent.path === item.path
          );
          
          let updatedRecent = [...state.recentlyAccessed];
          
          if (existingIndex >= 0) {
            // Update existing item
            updatedRecent[existingIndex] = {
              ...updatedRecent[existingIndex],
              lastAccessed: now,
              accessCount: updatedRecent[existingIndex].accessCount + 1,
            };
            
            // Move to front
            const [updatedItem] = updatedRecent.splice(existingIndex, 1);
            updatedRecent.unshift(updatedItem);
          } else {
            // Add new item to front
            updatedRecent.unshift({
              ...item,
              lastAccessed: now,
              accessCount: 1,
            });
          }
          
          // Keep only the 10 most recent
          updatedRecent = updatedRecent.slice(0, 10);
          
          // Update favorites if item is favorited
          const updatedFavorites = state.favorites.map(fav =>
            fav.path === item.path
              ? { ...fav, lastAccessed: now, accessCount: fav.accessCount + 1 }
              : fav
          );
          
          return {
            recentlyAccessed: updatedRecent,
            favorites: updatedFavorites,
          };
        });
      },

      setSidebarCollapsed: (sidebarCollapsed) => {
        set({ sidebarCollapsed });
      },

      getMostAccessed: (limit = 5) => {
        return get().recentlyAccessed
          .sort((a, b) => b.accessCount - a.accessCount)
          .slice(0, limit);
      },

      getRecentlyAccessed: (limit = 5) => {
        return get().recentlyAccessed
          .sort((a, b) => 
            new Date(b.lastAccessed || 0).getTime() - new Date(a.lastAccessed || 0).getTime()
          )
          .slice(0, limit);
      },
    }),
    {
      name: 'navigation-state',
    }
  )
);