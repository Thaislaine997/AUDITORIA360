import React from 'react';
import { Container, Typography, Paper, Box } from '@mui/material';

const PayrollPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Folha de Pagamento
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          Sistema de gestão de folha de pagamento em desenvolvimento.
        </Typography>
      </Paper>
    </Container>
  );
};

export default PayrollPage;