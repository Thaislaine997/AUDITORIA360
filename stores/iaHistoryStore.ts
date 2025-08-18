import { create } from 'zustand';

export interface IAInteraction {
  id: string;
  context: string;
  result: string;
  date: string;
}

interface IAHistoryState {
  history: IAInteraction[];
  addInteraction: (context: string, result: string) => void;
  clearHistory: () => void;
}

export const useIAHistoryStore = create<IAHistoryState>((set) => ({
  history: [],
  addInteraction: (context, result) =>
    set((state) => ({
      history: [
        {
          id: `${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
          context,
          result,
          date: new Date().toISOString(),
        },
        ...state.history,
      ],
    })),
  clearHistory: () => set({ history: [] }),
}));
