import React from "react";
import { Container, Typography, Paper } from "@mui/material";

const DocumentsPage: React.FC = () => {
  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Typography variant="h4" gutterBottom>
        Documentos
      </Typography>
      <Paper sx={{ p: 3 }}>
        <Typography variant="body1">
          Sistema de gestão de documentos em desenvolvimento.
        </Typography>
      </Paper>
    </Container>
  );
};

export default DocumentsPage;
