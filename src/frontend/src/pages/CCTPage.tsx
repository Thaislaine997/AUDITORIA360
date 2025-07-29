import React from 'react';
import { Container, Typography, Paper } from '@mui/material';

const CCTPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        CCT - Convenção Coletiva de Trabalho
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          Sistema de gestão de CCT em desenvolvimento.
        </Typography>
      </Paper>
    </Container>
  );
};

export default CCTPage;