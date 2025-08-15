import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Breadcrumbs, Typography, Box, Paper, Chip, Button } from '@mui/material';
import { Assignment, ArrowBack, Home } from '@mui/icons-material';
import { useTickets } from '../lib/hooks/useTickets';
import { IAAnalysisButton } from '../components/IAAnalysisButton';
import { useIASuggestionStore } from '../stores/iaSuggestionStore';

const TicketDetailPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query as { id?: string };
  const { tickets } = useTickets();
  const ticket = tickets.find(t => String(t.id) === id);
  const { suggestions, addSuggestion } = useIASuggestionStore();
  const [showSuggestion, setShowSuggestion] = useState(true);

  useEffect(() => {
    if (ticket) {
      const context = `Ticket: ${ticket.titulo} (ID: ${ticket.id})`;
      if (!suggestions.some(s => s.context === context)) {
        const suggestion = `Sugestão IA: Priorize este ticket se a prioridade for alta ou crítica.`;
        addSuggestion(context, suggestion);
      }
    }
    // eslint-disable-next-line
  }, [ticket]);

  if (!ticket) {
    return <Box p={4}><Typography>Ticket não encontrado.</Typography></Box>;
  }

  const currentSuggestion = suggestions.find(s => s.context === `Ticket: ${ticket.titulo} (ID: ${ticket.id})`);

  return (
    <Box maxWidth={700} mx="auto" mt={4}>
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
        <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}><Home fontSize="small" /> Dashboard</Link>
        <Link to="/demandas/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>Portal Demandas</Link>
        <Typography color="text.primary">Ticket #{ticket.id}</Typography>
      </Breadcrumbs>
      {currentSuggestion && showSuggestion && (
        <Paper sx={{ p: 2, mb: 2, bgcolor: '#e3f2fd', borderLeft: '6px solid #1976d2' }}>
          <Typography variant="subtitle1" color="primary.main" fontWeight={700} mb={1}>Sugestão Inteligente</Typography>
          <Typography variant="body2" mb={2}>{currentSuggestion.suggestion}</Typography>
          <Button size="small" variant="contained" color="primary" sx={{ mr: 1 }} onClick={() => setShowSuggestion(false)}>Aceitar</Button>
          <Button size="small" color="inherit" onClick={() => setShowSuggestion(false)}>Ignorar</Button>
        </Paper>
      )}
      <Paper sx={{ p: 4, mb: 2 }}>
        <Box display="flex" alignItems="center" gap={2} mb={2}>
          <Assignment color="primary" fontSize="large" />
          <Typography variant="h5" fontWeight={700}>{ticket.titulo}</Typography>
        </Box>
        <Chip label={`ID: ${ticket.id}`} sx={{ mr: 1 }} />
        <Chip label={`Status: ${ticket.status}`} sx={{ mr: 1 }} />
        <Chip label={`Prioridade: ${ticket.prioridade}`} sx={{ mr: 1 }} />
        <Typography variant="body1" mt={2}>{ticket.descricao}</Typography>
        <Typography variant="body2" color="text.secondary" mt={1}>Responsável: {ticket.responsavel}</Typography>
        <Typography variant="body2" color="text.secondary">Prazo: {new Date(ticket.prazo).toLocaleDateString()}</Typography>
        <Box mt={3}>
          <IAAnalysisButton context={`Ticket: ${ticket.titulo} (ID: ${ticket.id})`} label="Analisar este ticket com IA" />
        </Box>
      </Paper>
      <Button component={Link} to="/demandas/dashboard" startIcon={<ArrowBack />}>Voltar ao Dashboard</Button>
    </Box>
  );
};

export default TicketDetailPage;
