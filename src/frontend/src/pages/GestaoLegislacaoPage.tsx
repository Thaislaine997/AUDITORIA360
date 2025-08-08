// src/frontend/src/pages/GestaoLegislacaoPage.tsx

import React from 'react';
import { Container, Typography, Box, Card, CardContent, Alert } from '@mui/material';
import { UploadComponent } from '../components/UploadComponent';

export const GestaoLegislacaoPage: React.FC = () => {

  const handleUploadSuccess = (fileName: string) => {
    alert(`Ficheiro "${fileName}" enviado com sucesso! A aguardar processamento.`);
    // TODO: Adicionar lógica para recarregar a lista de documentos
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Gestão de Legislação
        </Typography>
        
        <Typography variant="body1" color="text.secondary" sx={{ mb: 4 }}>
          Submeta aqui os ficheiros PDF de Leis, Decretos, Medidas Provisórias ou Convenções Coletivas para serem analisados pela IA.
        </Typography>

        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Enviar Documento
            </Typography>
            <UploadComponent onUploadSuccess={handleUploadSuccess} />
          </CardContent>
        </Card>

        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Documentos Enviados
            </Typography>
            {/* TODO: Criar uma tabela para listar os documentos da tabela `Documentos` da Supabase */}
            <Alert severity="info">
              A lista de documentos aparecerá aqui
            </Alert>
          </CardContent>
        </Card>
      </Box>
    </Container>
  );
};