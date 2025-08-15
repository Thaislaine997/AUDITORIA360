import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, Chip, Box } from '@mui/material';
import { Notificacao } from '../lib/portalDemandasTypes';
import { Notifications, PriorityHigh, Done } from '@mui/icons-material';

interface NotificacaoDetailModalProps {
  notif: Notificacao | null;
  onClose: () => void;
}

const prioridadeColor = (prioridade: string): "error" | "warning" | "info" | "success" | "default" => {
  switch (prioridade) {
    case 'CRITICA': return 'error';
    case 'ALTA': return 'warning';
    case 'MEDIA': return 'info';
    case 'BAIXA': return 'success';
    default: return 'default';
  }
};

export const NotificacaoDetailModal: React.FC<NotificacaoDetailModalProps> = ({ notif, onClose }) => {
  if (!notif) return null;
  return (
    <Dialog open={!!notif} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Detalhes da Notificação</DialogTitle>
      <DialogContent>
        <Box display="flex" alignItems="center" gap={1} mb={2}>
          <Chip label={notif.prioridade.toUpperCase()} color={prioridadeColor(notif.prioridade)} size="small" icon={<PriorityHigh />} />
          <Chip label={notif.tipo_notificacao} size="small" icon={<Notifications />} />
          {notif.lida && <Chip label="LIDA" color="success" size="small" icon={<Done />} />}
        </Box>
        <Typography variant="h6" fontWeight={700}>{notif.titulo}</Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          <b>Data:</b> {new Date(notif.criado_em).toLocaleString()}
        </Typography>
        <Typography variant="body1" sx={{ mb: 2 }}>{notif.mensagem}</Typography>
        {notif.link_acao && (
          <Button href={notif.link_acao} target="_blank" rel="noopener noreferrer" size="small" color="primary" sx={{ mr: 1 }}>Acessar ação</Button>
        )}
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">Fechar</Button>
      </DialogActions>
    </Dialog>
  );
};
