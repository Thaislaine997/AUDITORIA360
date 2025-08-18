import React from 'react';
import { Typography, Container, Box } from '@mui/material';

export default function Home() {
  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          AUDITORIA360
        </Typography>
        <Typography variant="h6" color="text.secondary">
          Plataforma Moderna de Terceirização de Departamento Pessoal
        </Typography>
      </Box>
    </Container>
  );
}