import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Breadcrumbs, Typography, Box, Paper, Chip, Button } from '@mui/material';
import { TaskAlt, ArrowBack, Home, CheckCircle } from '@mui/icons-material';
import { useTarefas } from '../lib/hooks/usePortalDemandasDomain';
import { IAAnalysisButton } from '../components/IAAnalysisButton';
import { useIASuggestionStore } from '../stores/iaSuggestionStore';

const TarefaDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const tarefas = useTarefas();
  const tarefa = tarefas.find(t => String(t.id) === id);
  const { suggestions, addSuggestion } = useIASuggestionStore();
  const [showSuggestion, setShowSuggestion] = useState(true);

  useEffect(() => {
    if (tarefa) {
      const context = `Tarefa: ${tarefa.nome_tarefa} (ID: ${tarefa.id})`;
      if (!suggestions.some(s => s.context === context)) {
        const suggestion = `Sugestão IA: Marque como concluída assim que finalizar a tarefa para manter o controle atualizado.`;
        addSuggestion(context, suggestion);
      }
    }
    // eslint-disable-next-line
  }, [tarefa]);

  if (!tarefa) {
    return <Box p={4}><Typography>Tarefa não encontrada.</Typography></Box>;
  }

  const currentSuggestion = suggestions.find(s => s.context === `Tarefa: ${tarefa.nome_tarefa} (ID: ${tarefa.id})`);

  return (
    <Box maxWidth={700} mx="auto" mt={4}>
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
        <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}><Home fontSize="small" /> Dashboard</Link>
        <Link to="/demandas/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>Portal Demandas</Link>
        <Typography color="text.primary">Tarefa #{tarefa.id}</Typography>
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
          <TaskAlt color="primary" fontSize="large" />
          <Typography variant="h5" fontWeight={700}>{tarefa.nome_tarefa}</Typography>
        </Box>
        <Chip label={`ID: ${tarefa.id}`} sx={{ mr: 1 }} />
        {tarefa.concluido && <Chip label="Concluída" color="success" icon={<CheckCircle />} sx={{ mr: 1 }} />}
        {tarefa.data_conclusao && <Typography variant="body2" color="text.secondary">Concluída em: {new Date(tarefa.data_conclusao).toLocaleDateString()}</Typography>}
        <Box mt={3}>
          <IAAnalysisButton context={`Tarefa: ${tarefa.nome_tarefa} (ID: ${tarefa.id})`} label="Analisar esta tarefa com IA" />
        </Box>
      </Paper>
      <Button component={Link} to="/demandas/dashboard" startIcon={<ArrowBack />}>Voltar ao Dashboard</Button>
    </Box>
  );
};

export default TarefaDetailPage;
