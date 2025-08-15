import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Breadcrumbs, Typography, Box, Paper, Chip, Button } from '@mui/material';
import { Assignment, ArrowBack, Home } from '@mui/icons-material';
import { useAuditorias } from '../lib/hooks/usePortalDemandasAuditoria';
import { IAAnalysisButton } from '../components/IAAnalysisButton';
import { useIASuggestionStore } from '../stores/iaSuggestionStore';

const AuditoriaDetailPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query as { id?: string };
  const auditorias = useAuditorias();
  const auditoria = auditorias.find(a => String(a.id) === id);
  const { suggestions, addSuggestion } = useIASuggestionStore();
  const [showSuggestion, setShowSuggestion] = useState(true);

  useEffect(() => {
    if (auditoria) {
      const context = `Auditoria: ${auditoria.descricao} (ID: ${auditoria.id})`;
      if (!suggestions.some(s => s.context === context)) {
        const suggestion = `Sugestão IA: Certifique-se de registrar todas as evidências e pendências encontradas nesta auditoria.`;
        addSuggestion(context, suggestion);
      }
    }
    // eslint-disable-next-line
  }, [auditoria]);

  if (!auditoria) {
    return <Box p={4}><Typography>Auditoria não encontrada.</Typography></Box>;
  }

  const currentSuggestion = suggestions.find(s => s.context === `Auditoria: ${auditoria.descricao} (ID: ${auditoria.id})`);

  return (
    <Box maxWidth={700} mx="auto" mt={4}>
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
        <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}><Home fontSize="small" /> Dashboard</Link>
        <Link to="/demandas/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>Portal Demandas</Link>
        <Typography color="text.primary">Auditoria #{auditoria.id}</Typography>
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
          <Typography variant="h5" fontWeight={700}>{auditoria.descricao}</Typography>
        </Box>
        <Chip label={`ID: ${auditoria.id}`} sx={{ mr: 1 }} />
        <Typography variant="body1" mt={2}>Status: {auditoria.status || '-'}</Typography>
        <Typography variant="body1">Início: {auditoria.data_inicio || '-'}</Typography>
        {auditoria.data_fim && <Typography variant="body1">Fim: {auditoria.data_fim}</Typography>}
        <Typography variant="body1">Responsável: {auditoria.responsavel}</Typography>
        <Box mt={3}>
          <IAAnalysisButton context={`Auditoria: ${auditoria.descricao} (ID: ${auditoria.id})`} label="Analisar esta auditoria com IA" />
        </Box>
      </Paper>
      <Button component={Link} to="/demandas/dashboard" startIcon={<ArrowBack />}>Voltar ao Dashboard</Button>
    </Box>
  );
};

export default AuditoriaDetailPage;
