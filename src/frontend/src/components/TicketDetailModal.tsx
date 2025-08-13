import React from 'react';
import { Dialog, DialogTitle, DialogContent, DialogActions, Button, Typography, Chip, Box } from '@mui/material';
import { Ticket } from '../lib/portalDemandasTypes';
import { PriorityHigh, CheckCircle, Label } from '@mui/icons-material';

interface TicketDetailModalProps {
  ticket: Ticket | null;
  onClose: () => void;
}

const statusColor = (status: string) => {
  switch (status) {
    case 'concluido': return 'success';
    case 'em_andamento': return 'primary';
    case 'pendente': return 'warning';
    case 'cancelado': return 'error';
    default: return 'default';
  }
};

const prioridadeColor = (prioridade: string): "error" | "warning" | "info" | "success" | "default" => {
  switch (prioridade) {
    case 'CRITICA': return 'error';
    case 'ALTA': return 'warning';
    case 'MEDIA': return 'info';
    case 'BAIXA': return 'success';
    default: return 'default';
  }
};

export const TicketDetailModal: React.FC<TicketDetailModalProps> = ({ ticket, onClose }) => {
  if (!ticket) return null;
  return (
    <Dialog open={!!ticket} onClose={onClose} maxWidth="sm" fullWidth>
      <DialogTitle>Detalhes do Ticket</DialogTitle>
      <DialogContent>
        <Box display="flex" alignItems="center" gap={1} mb={2}>
          <Chip label={ticket.status.toUpperCase()} color={statusColor(ticket.status)} size="small" icon={<CheckCircle />} />
          <Chip label={ticket.prioridade.toUpperCase()} color={prioridadeColor(ticket.prioridade)} size="small" icon={<PriorityHigh />} />
          <Chip label={ticket.categoria.toUpperCase()} size="small" icon={<Label />} />
        </Box>
        <Typography variant="h6" fontWeight={700}>{ticket.titulo}</Typography>
        <Typography variant="body2" color="text.secondary" gutterBottom>
          <b>Responsável:</b> {ticket.responsavel} | <b>Prazo:</b> {new Date(ticket.prazo).toLocaleDateString()}
        </Typography>
        {ticket.descricao && <Typography variant="body1" sx={{ mb: 2 }}>{ticket.descricao}</Typography>}
        {ticket.tags && <Chip label={ticket.tags} size="small" sx={{ mr: 1 }} />}
        <Typography variant="caption" color="text.disabled">
          Criado em: {new Date(ticket.criado_em).toLocaleString()} | Atualizado em: {new Date(ticket.atualizado_em).toLocaleString()}
        </Typography>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose} color="primary">Fechar</Button>
      </DialogActions>
    </Dialog>
  );
};
