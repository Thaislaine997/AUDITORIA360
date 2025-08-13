import { useEffect, useState } from 'react';
import { Ticket } from './portalDemandasTypes';
import { portalDemandasService } from './portalDemandasService';

export function useTickets() {
  const [tickets, setTickets] = useState<Ticket[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    portalDemandasService.listarTickets()
      .then(setTickets)
      .catch(e => setError(e.message || 'Erro ao carregar tickets'))
      .finally(() => setLoading(false));
  }, []);

  return { tickets, loading, error };
}
