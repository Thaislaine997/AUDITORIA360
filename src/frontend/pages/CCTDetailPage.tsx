import React, { useEffect, useState } from 'react';
import { useRouter } from 'next/router';
import Link from 'next/link';
import { Breadcrumbs, Typography, Box, Paper, Chip, Button } from '@mui/material';
import { Gavel, ArrowBack, Home } from '@mui/icons-material';
import { useCCTs } from '../lib/hooks/usePortalDemandasDomain';
import { IAAnalysisButton } from '../components/IAAnalysisButton';
import { useIASuggestionStore } from '../stores/iaSuggestionStore';

const CCTDetailPage: React.FC = () => {
  const router = useRouter();
  const { id } = router.query as { id?: string };
  const ccts = useCCTs();
  const cct = ccts.find(c => String(c.id) === id);
  const { suggestions, addSuggestion } = useIASuggestionStore();
  const [showSuggestion, setShowSuggestion] = useState(true);

  useEffect(() => {
    if (cct) {
      const context = `CCT: ${cct.numero_registro_mte} (ID: ${cct.id})`;
      if (!suggestions.some(s => s.context === context)) {
        const suggestion = `Sugestão IA: Verifique a vigência e se há cláusulas novas que impactam folha ou benefícios.`;
        addSuggestion(context, suggestion);
      }
    }
    // eslint-disable-next-line
  }, [cct]);

  if (!cct) {
    return <Box p={4}><Typography>CCT não encontrada.</Typography></Box>;
  }

  const currentSuggestion = suggestions.find(s => s.context === `CCT: ${cct.numero_registro_mte} (ID: ${cct.id})`);

  return (
    <Box maxWidth={700} mx="auto" mt={4}>
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
        <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}><Home fontSize="small" /> Dashboard</Link>
        <Link to="/demandas/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>Portal Demandas</Link>
        <Typography color="text.primary">CCT #{cct.id}</Typography>
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
          <Gavel color="primary" fontSize="large" />
          <Typography variant="h5" fontWeight={700}>Registro: {cct.numero_registro_mte}</Typography>
        </Box>
        <Chip label={`ID: ${cct.id}`} sx={{ mr: 1 }} />
        <Chip label={`Sindicato: ${cct.sindicato_id}`} sx={{ mr: 1 }} />
        <Typography variant="body1" mt={2}>Vigência: {cct.vigencia_inicio} a {cct.vigencia_fim}</Typography>
        <Box mt={3}>
          <IAAnalysisButton context={`CCT: ${cct.numero_registro_mte} (ID: ${cct.id})`} label="Analisar esta CCT com IA" />
        </Box>
      </Paper>
      <Button component={Link} to="/demandas/dashboard" startIcon={<ArrowBack />}>Voltar ao Dashboard</Button>
    </Box>
  );
};

export default CCTDetailPage;
