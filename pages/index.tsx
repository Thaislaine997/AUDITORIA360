import React from "react";
import { NextPage } from "next";
import { Box, Typography, Container } from "@mui/material";

const HomePage: NextPage = () => {
  return (
    <Container maxWidth="lg">
      <Box sx={{ my: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          AUDITORIA360
        </Typography>
        <Typography variant="h6" component="h2" gutterBottom>
          Plataforma Moderna de Terceirização de Departamento Pessoal
        </Typography>
        <Typography variant="body1">
          Sistema de auditoria e gestão em funcionamento.
        </Typography>
      </Box>
    </Container>
  );
};

export default HomePage;
