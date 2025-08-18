// Página dinâmica de detalhe de sindicato
import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Breadcrumbs, Typography, Box, Paper, Chip, Button } from '@mui/material';
import { Groups, ArrowBack, Home, Info } from '@mui/icons-material';
import { useSindicatos } from '../../lib/hooks/usePortalDemandasDomain';
import { IAAnalysisButton } from '../../components/IAAnalysisButton';
import { useIASuggestionStore } from '../../stores/iaSuggestionStore';
// ...existing code...

const SindicatoDetailPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query as { id?: string };
  const sindicatos = useSindicatos();
  const sindicato = sindicatos.find(s => String(s.id) === id);
  const { suggestions, addSuggestion } = useIASuggestionStore();
  const [showSuggestion, setShowSuggestion] = useState(true);

  useEffect(() => {
    if (sindicato) {
      const context = `Sindicato: ${sindicato.nome_sindicato} (ID: ${sindicato.id})`;
      if (!suggestions.some(s => s.context === context)) {
        const suggestion = `Sugestão IA: Verifique se o sindicato está atualizado com as últimas CCTs e bases territoriais.`;
        addSuggestion(context, suggestion);
      }
    }
    // eslint-disable-next-line
  }, [sindicato]);

  if (!sindicato) {
    return <Box p={4}><Typography>Sindicato não encontrado.</Typography></Box>;
  }

  const currentSuggestion = suggestions.find(s => s.context === `Sindicato: ${sindicato.nome_sindicato} (ID: ${sindicato.id})`);

  return (
    <Box maxWidth={700} mx="auto" mt={4}>
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
        <Link href="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}><Home fontSize="small" /> Dashboard</Link>
        <Link href="/demandas/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>Portal Demandas</Link>
        <Typography color="text.primary">Sindicato #{sindicato.id}</Typography>
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
          <Groups color="primary" fontSize="large" />
          <Typography variant="h5" fontWeight={700}>{sindicato.nome_sindicato}</Typography>
        </Box>
        <Chip label={`ID: ${sindicato.id}`} sx={{ mr: 1 }} />
        {sindicato.cnpj && <Chip label={`CNPJ: ${sindicato.cnpj}`} icon={<Info />} sx={{ mr: 1 }} />}
        <Typography variant="body1" mt={2}>Base: {sindicato.base_territorial || '-'}</Typography>
        <Typography variant="body1">Categoria: {sindicato.categoria_representada || '-'}</Typography>
        <Box mt={3}>
          <IAAnalysisButton context={`Sindicato: ${sindicato.nome_sindicato} (ID: ${sindicato.id})`} label="Analisar este sindicato com IA" />
        </Box>
      </Paper>
      <Button component={Link} href="/demandas/dashboard" startIcon={<ArrowBack />}>Voltar ao Dashboard</Button>
    </Box>
  );
};

export default SindicatoDetailPage;
