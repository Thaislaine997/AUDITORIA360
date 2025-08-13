import { create } from 'zustand';

export interface IASuggestion {
  id: string;
  context: string;
  suggestion: string;
  date: string;
}

interface IASuggestionState {
  suggestions: IASuggestion[];
  addSuggestion: (context: string, suggestion: string) => void;
  clearSuggestions: () => void;
}

export const useIASuggestionStore = create<IASuggestionState>((set) => ({
  suggestions: [],
  addSuggestion: (context, suggestion) => set((state) => ({
    suggestions: [
      {
        id: `${Date.now()}_${Math.random().toString(36).substr(2, 6)}`,
        context,
        suggestion,
        date: new Date().toISOString(),
      },
      ...state.suggestions,
    ],
  })),
  clearSuggestions: () => set({ suggestions: [] }),
}));
