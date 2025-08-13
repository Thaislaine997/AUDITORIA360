import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Breadcrumbs, Typography, Box, Paper, Chip, Button } from '@mui/material';
import { Description, ArrowBack, Home } from '@mui/icons-material';
import { useRelatorios } from '../lib/hooks/usePortalDemandasAuditoria';
import { IAAnalysisButton } from '../components/IAAnalysisButton';
import { useIASuggestionStore } from '../stores/iaSuggestionStore';

const RelatorioDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const relatorios = useRelatorios();
  const relatorio = relatorios.find(r => String(r.id) === id);
  const { suggestions, addSuggestion } = useIASuggestionStore();
  const [showSuggestion, setShowSuggestion] = useState(true);

  useEffect(() => {
    if (relatorio) {
      const context = `Relatório: ${relatorio.titulo} (ID: ${relatorio.id})`;
      if (!suggestions.some(s => s.context === context)) {
        const suggestion = `Sugestão IA: Compartilhe este relatório com os responsáveis e registre feedbacks para melhoria contínua.`;
        addSuggestion(context, suggestion);
      }
    }
    // eslint-disable-next-line
  }, [relatorio]);

  if (!relatorio) {
    return <Box p={4}><Typography>Relatório não encontrado.</Typography></Box>;
  }

  const currentSuggestion = suggestions.find(s => s.context === `Relatório: ${relatorio.titulo} (ID: ${relatorio.id})`);

  return (
    <Box maxWidth={700} mx="auto" mt={4}>
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
        <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}><Home fontSize="small" /> Dashboard</Link>
        <Link to="/demandas/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>Portal Demandas</Link>
        <Typography color="text.primary">Relatório #{relatorio.id}</Typography>
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
          <Description color="primary" fontSize="large" />
          <Typography variant="h5" fontWeight={700}>{relatorio.titulo || `Relatório #${relatorio.id}`}</Typography>
        </Box>
        <Chip label={`ID: ${relatorio.id}`} sx={{ mr: 1 }} />
        <Typography variant="body1" mt={2}>Empresa: {relatorio.empresa_id}</Typography>
        <Typography variant="body1">Emissão: {relatorio.data_emissao || '-'}</Typography>
        <Box mt={3}>
          <IAAnalysisButton context={`Relatório: ${relatorio.titulo} (ID: ${relatorio.id})`} label="Analisar este relatório com IA" />
        </Box>
      </Paper>
      <Button component={Link} to="/demandas/dashboard" startIcon={<ArrowBack />}>Voltar ao Dashboard</Button>
    </Box>
  );
};

export default RelatorioDetailPage;
