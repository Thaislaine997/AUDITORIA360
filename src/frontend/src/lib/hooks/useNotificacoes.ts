import { useEffect, useState } from 'react';
import { Notificacao } from './portalDemandasTypes';
import { portalDemandasService } from './portalDemandasService';

export function useNotificacoes() {
  const [notificacoes, setNotificacoes] = useState<Notificacao[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setLoading(true);
    portalDemandasService.listarNotificacoes()
      .then(setNotificacoes)
      .catch(e => setError(e.message || 'Erro ao carregar notificações'))
      .finally(() => setLoading(false));
  }, []);

  const marcarComoLida = async (id: number) => {
    await portalDemandasService.marcarNotificacaoComoLida(id);
    setNotificacoes(n => n.map(notif => notif.id === id ? { ...notif, lida: true } : notif));
  };

  return { notificacoes, loading, error, marcarComoLida };
}
