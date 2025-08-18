

import React, { useState } from 'react';
import { useTickets } from '../lib/hooks/useTickets';
import { Ticket } from '../lib/portalDemandasTypes';
import { Box, Card, CardContent, Typography, Chip, Button } from '@mui/material';
import Grid from '@mui/material/Grid';
import { TicketDetailModal } from './TicketDetailModal';
import { PriorityHigh, CheckCircle, Label } from '@mui/icons-material';

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


export const TicketCard: React.FC<{ ticket: Ticket; onOpen: (ticket: Ticket) => void }> = ({ ticket, onOpen }) => (
  <Card sx={{ minWidth: 260, borderRadius: 2, boxShadow: 2, mb: 2, position: 'relative', background: '#fafbfc' }}>
    <CardContent>
      <Box display="flex" alignItems="center" gap={1} mb={1}>
        <Chip label={ticket.status.toUpperCase()} color={statusColor(ticket.status)} size="small" icon={<CheckCircle />} />
        <Chip label={ticket.prioridade.toUpperCase()} color={prioridadeColor(ticket.prioridade)} size="small" icon={<PriorityHigh />} />
        <Chip label={ticket.categoria.toUpperCase()} size="small" icon={<Label />} />
      </Box>
      <Typography variant="h6" fontWeight={600} gutterBottom>{ticket.titulo}</Typography>
      <Typography variant="body2" color="text.secondary" gutterBottom>
        <b>Responsável:</b> {ticket.responsavel} | <b>Prazo:</b> {new Date(ticket.prazo).toLocaleDateString()}
      </Typography>
      {ticket.descricao && <Typography variant="body2" sx={{ mb: 1 }}>{ticket.descricao}</Typography>}
      {ticket.tags && <Chip label={ticket.tags} size="small" sx={{ mr: 1 }} />}
      <Typography variant="caption" color="text.disabled">
        Criado em: {new Date(ticket.criado_em).toLocaleString()} | Atualizado em: {new Date(ticket.atualizado_em).toLocaleString()}
      </Typography>
      <Box mt={2} display="flex" justifyContent="flex-end">
        <Button size="small" variant="outlined" onClick={() => onOpen(ticket)}>Detalhes</Button>
      </Box>
    </CardContent>
  </Card>
);

export const TicketsList: React.FC = () => {
  const { tickets, loading, error } = useTickets();
  const [modalTicket, setModalTicket] = useState<Ticket | null>(null);

  if (loading) return <div>Carregando tickets...</div>;
  if (error) return <div>Erro: {error}</div>;
  if (!tickets.length) return <div>Nenhum ticket encontrado.</div>;

  return (
    <Box>
      <Typography variant="h5" fontWeight={700} mb={2}>Tickets</Typography>
      <Grid container spacing={2}>
        {tickets.map(ticket => (
          <Grid size={{ xs: 12, sm: 6, md: 4 }} key={ticket.id}>
            <TicketCard ticket={ticket} onOpen={setModalTicket} />
          </Grid>
        ))}
      </Grid>
      <TicketDetailModal ticket={modalTicket} onClose={() => setModalTicket(null)} />
    </Box>
  );
};
