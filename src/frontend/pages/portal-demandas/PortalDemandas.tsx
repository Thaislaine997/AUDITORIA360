import React from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  Button,
} from "@mui/material";
import {
  Assignment,
  Add,
  FilterList,
  Search,
} from "@mui/icons-material";

const PortalDemandas: React.FC = () => {
  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Portal de Demandas
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Gerencie solicitações, tickets e demandas dos clientes de forma centralizada e eficiente.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
              <Typography variant="h6">
                Lista de Demandas
              </Typography>
              <Button
                variant="contained"
                startIcon={<Add />}
                color="primary"
              >
                Nova Demanda
              </Button>
            </Box>
            
            <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
              <Button
                variant="outlined"
                startIcon={<Search />}
              >
                Buscar
              </Button>
              <Button
                variant="outlined"
                startIcon={<FilterList />}
              >
                Filtros
              </Button>
            </Box>

            <Card>
              <CardContent>
                <Box sx={{ display: "flex", alignItems: "center", gap: 2 }}>
                  <Assignment color="primary" />
                  <Box>
                    <Typography variant="h6">
                      Interface em Desenvolvimento
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      O Portal de Demandas está sendo desenvolvido como um componente React para substituir o documento de texto atual.
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default PortalDemandas;