import React, { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import { Breadcrumbs, Typography, Box, Paper, Chip, Button } from '@mui/material';
import { CloudUpload, ArrowBack, Home } from '@mui/icons-material';
import { useUploads } from '../lib/hooks/usePortalDemandasAuditoria';
import { IAAnalysisButton } from '../components/IAAnalysisButton';
import { useIASuggestionStore } from '../stores/iaSuggestionStore';

const UploadDetailPage: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const uploads = useUploads();
  const upload = uploads.find(u => String(u.id) === id);
  const { suggestions, addSuggestion } = useIASuggestionStore();
  const [showSuggestion, setShowSuggestion] = useState(true);

  useEffect(() => {
    if (upload) {
      const context = `Upload: ${upload.nome_arquivo} (ID: ${upload.id})`;
      if (!suggestions.some(s => s.context === context)) {
        const suggestion = `Sugestão IA: Certifique-se de que o arquivo está nomeado corretamente e compartilhe apenas com usuários autorizados.`;
        addSuggestion(context, suggestion);
      }
    }
    // eslint-disable-next-line
  }, [upload]);

  if (!upload) {
    return <Box p={4}><Typography>Upload não encontrado.</Typography></Box>;
  }

  const currentSuggestion = suggestions.find(s => s.context === `Upload: ${upload.nome_arquivo} (ID: ${upload.id})`);

  return (
    <Box maxWidth={700} mx="auto" mt={4}>
      <Breadcrumbs aria-label="breadcrumb" sx={{ mb: 2 }}>
        <Link to="/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}><Home fontSize="small" /> Dashboard</Link>
        <Link to="/demandas/dashboard" style={{ textDecoration: 'none', color: 'inherit' }}>Portal Demandas</Link>
        <Typography color="text.primary">Upload #{upload.id}</Typography>
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
          <CloudUpload color="primary" fontSize="large" />
          <Typography variant="h5" fontWeight={700}>{upload.nome_arquivo || `Upload #${upload.id}`}</Typography>
        </Box>
        <Chip label={`ID: ${upload.id}`} sx={{ mr: 1 }} />
        <Typography variant="body1" mt={2}>Empresa: {upload.empresa_id}</Typography>
        <Typography variant="body1">Data: {upload.data_upload || '-'}</Typography>
        <Typography variant="body1">Usuário: {upload.usuario_upload}</Typography>
        <Box mt={3}>
          <IAAnalysisButton context={`Upload: ${upload.nome_arquivo} (ID: ${upload.id})`} label="Analisar este upload com IA" />
        </Box>
      </Paper>
      <Button component={Link} to="/demandas/dashboard" startIcon={<ArrowBack />}>Voltar ao Dashboard</Button>
    </Box>
  );
};

export default UploadDetailPage;
