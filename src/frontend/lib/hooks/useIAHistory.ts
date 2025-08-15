import { useIAHistoryStore } from '../../stores/iaHistoryStore';

export function useIAHistory() {
  const history = useIAHistoryStore(state => state.history);
  const addInteraction = useIAHistoryStore(state => state.addInteraction);
  const clearHistory = useIAHistoryStore(state => state.clearHistory);
  return { history, addInteraction, clearHistory };
}
