import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Breadcrumbs, Typography, Box, Paper, Chip, Button } from '@mui/material';
import { Home, Business, ArrowBack } from '@mui/icons-material';
import { useEmpresas } from '../lib/hooks/usePortalDemandasDomain';
import { IAAnalysisButton } from '../components/IAAnalysisButton';
import { useIASuggestionStore } from '../stores/iaSuggestionStore';

const EmpresaDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const empresas = useEmpresas();
  const empresa = empresas.find(e => String(e.id) === id);
  const { suggestions, addSuggestion, clearSuggestions } = useIASuggestionStore();
  const [showSuggestion, setShowSuggestion] = useState(true);

  useEffect(() => {
    if (empresa) {
      // Simulação: chamada IA para sugestão automática
      const context = `Empresa: ${empresa.nome} (ID: ${empresa.id})`;
      // Só sugere se ainda não houver sugestão para este contexto
      if (!suggestions.some(s => s.context === context)) {
        // Aqui poderia ser um fetch real para endpoint de sugestão IA
        const suggestion = `Sugestão IA: Criar tarefa de auditoria inicial para a empresa "${empresa.nome}".`;
        addSuggestion(context, suggestion);
      }
    }
    // eslint-disable-next-line
  }, [empresa]);

  if (!empresa) {
    return <Box p={4}><Typography>Empresa não encontrada.</Typography></Box>;
  }

  const currentSuggestion = suggestions.find(s => s.context === `Empresa: ${empresa.nome} (ID: ${empresa.id})`);

  return (
    <Box maxWidth={700} mx="auto" mt={4}>
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
        <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}><Home fontSize="small" /> Dashboard</Link>
        <Link to="/demandas/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>Portal Demandas</Link>
        <Typography color="text.primary">Empresa #{empresa.id}</Typography>
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
          <Business color="primary" fontSize="large" />
          <Typography variant="h5" fontWeight={700}>{empresa.nome}</Typography>
        </Box>
        <Chip label={`ID: ${empresa.id}`} sx={{ mr: 1 }} />
        {empresa.sindicato_id && <Chip label={`Sindicato: ${empresa.sindicato_id}`} sx={{ mr: 1 }} />}
        <Typography variant="body1" mt={2}>Criada em: {empresa.criado_em ? new Date(empresa.criado_em).toLocaleDateString() : '-'}</Typography>
        <Box mt={3}>
          <IAAnalysisButton context={`Empresa: ${empresa.nome} (ID: ${empresa.id})`} label="Analisar esta empresa com IA" />
        </Box>
      </Paper>
      <Button component={Link} to="/demandas/dashboard" startIcon={<ArrowBack />}>Voltar ao Dashboard</Button>
    </Box>
  );
};

export default EmpresaDetailPage;
