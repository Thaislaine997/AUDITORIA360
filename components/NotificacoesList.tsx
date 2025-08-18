
import React, { useState } from 'react';
import { useNotificacoes } from '../lib/hooks/useNotificacoes';
import { Notificacao } from '../lib/portalDemandasTypes';
import { Box, Card, CardContent, Typography, Chip, Grid, Button } from '@mui/material';
import { NotificacaoDetailModal } from './NotificacaoDetailModal';
import { Notifications, PriorityHigh, Done } from '@mui/icons-material';

const prioridadeColor = (prioridade: string): "error" | "warning" | "info" | "success" | "default" => {
  switch (prioridade) {
    case 'CRITICA': return 'error';
    case 'ALTA': return 'warning';
    case 'MEDIA': return 'info';
    case 'BAIXA': return 'success';
    default: return 'default';
  }
};

export const NotificacaoCard: React.FC<{ notif: Notificacao; marcarComoLida: (id: number) => void; onOpen: (notif: Notificacao) => void }> = ({ notif, marcarComoLida, onOpen }) => (
  <Card sx={{ minWidth: 260, borderRadius: 2, boxShadow: 2, mb: 2, position: 'relative', background: notif.lida ? '#f5f5f5' : '#fff8e1', opacity: notif.lida ? 0.6 : 1 }}>
    <CardContent>
      <Box display="flex" alignItems="center" gap={1} mb={1}>
        <Chip label={notif.prioridade.toUpperCase()} color={prioridadeColor(notif.prioridade)} size="small" icon={<PriorityHigh />} />
        <Chip label={notif.tipo_notificacao} size="small" icon={<Notifications />} />
        {notif.lida && <Chip label="LIDA" color="success" size="small" icon={<Done />} />}
      </Box>
      <Typography variant="h6" fontWeight={600} gutterBottom>{notif.titulo}</Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        <b>Data:</b> {new Date(notif.criado_em).toLocaleString()}
      </Typography>
      <Typography variant="body2" sx={{ mb: 1 }}>{notif.mensagem}</Typography>
      {notif.link_acao && (
        <Button href={notif.link_acao} target="_blank" rel="noopener noreferrer" size="small" color="primary" sx={{ mr: 1 }}>Acessar ação</Button>
      )}
      {!notif.lida && (
        <Button variant="outlined" color="success" size="small" onClick={() => marcarComoLida(notif.id)} sx={{ position: 'absolute', top: 16, right: 16 }}>Marcar como lida</Button>
      )}
      <Box mt={2} display="flex" justifyContent="flex-end">
        <Button size="small" variant="outlined" onClick={() => onOpen(notif)}>Detalhes</Button>
      </Box>
    </CardContent>
  </Card>
);

export const NotificacoesList: React.FC = () => {
  const { notificacoes, loading, error, marcarComoLida } = useNotificacoes();
  const [modalNotif, setModalNotif] = useState<Notificacao | null>(null);

  if (loading) return <div>Carregando notificações...</div>;
  if (error) return <div>Erro: {error}</div>;
  if (!notificacoes.length) return <div>Nenhuma notificação encontrada.</div>;

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} mb={2}>Notificações</Typography>
      <Grid container spacing={2}>
        {notificacoes.map(notif => (
          <Grid item xs={12} sm={6} md={4} key={notif.id}>
            <NotificacaoCard notif={notif} marcarComoLida={marcarComoLida} onOpen={setModalNotif} />
          </Grid>
        ))}
      </Grid>
      <NotificacaoDetailModal notif={modalNotif} onClose={() => setModalNotif(null)} />
    </Box>
  );
};
