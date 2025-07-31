import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
} from "@mui/material";
import {
  Psychology,
  Send,
  History,
  TrendingUp,
  Warning,
  CheckCircle,
} from "@mui/icons-material";

const ConsultorRiscos: React.FC = () => {
  const [query, setQuery] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    // Simulate AI analysis
    setTimeout(() => {
      setIsAnalyzing(false);
    }, 3000);
  };

  const riskCategories = [
    { name: "Riscos Trabalhistas", level: "Alto", count: 12, color: "error" },
    { name: "Conformidade Fiscal", level: "Médio", count: 8, color: "warning" },
    { name: "Cálculos de Folha", level: "Baixo", count: 3, color: "success" },
    { name: "Documentação", level: "Médio", count: 5, color: "warning" },
  ];

  const recentAnalyses = [
    "Análise de horas extras irregulares",
    "Verificação de adicional noturno",
    "Conformidade com CCT 2024",
    "Auditoria de benefícios",
  ];

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Consultor de Riscos
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          IA avançada para identificação e análise de riscos na folha de pagamento.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Análise Inteligente de Riscos
            </Typography>
            
            <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
              <TextField
                fullWidth
                multiline
                rows={4}
                placeholder="Descreva a situação ou faça uma pergunta sobre riscos trabalhistas..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                variant="outlined"
              />
            </Box>

            <Button
              variant="contained"
              startIcon={<Psychology />}
              onClick={handleAnalyze}
              disabled={!query.trim() || isAnalyzing}
              size="large"
            >
              {isAnalyzing ? "Analisando..." : "Analisar Riscos"}
            </Button>

            {isAnalyzing && (
              <Box sx={{ mt: 3, p: 2, bgcolor: "grey.50", borderRadius: 1 }}>
                <Typography variant="body2">
                  🤖 IA processando análise de riscos...
                </Typography>
              </Box>
            )}
          </Paper>

          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Análises Recentes
            </Typography>
            <List>
              {recentAnalyses.map((analysis, index) => (
                <React.Fragment key={index}>
                  <ListItem>
                    <ListItemText 
                      primary={analysis}
                      secondary={`${new Date().toLocaleDateString()} - Análise completa`}
                    />
                    <Button size="small" startIcon={<History />}>
                      Ver Detalhes
                    </Button>
                  </ListItem>
                  {index < recentAnalyses.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Categorias de Risco
            </Typography>
            
            {riskCategories.map((category, index) => (
              <Card key={index} sx={{ mb: 2 }}>
                <CardContent sx={{ p: 2, "&:last-child": { pb: 2 } }}>
                  <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 1 }}>
                    <Typography variant="subtitle2">
                      {category.name}
                    </Typography>
                    <Chip 
                      label={category.level}
                      color={category.color as any}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary">
                    {category.count} itens identificados
                  </Typography>
                  <Box sx={{ display: "flex", alignItems: "center", mt: 1 }}>
                    {category.level === "Alto" && <Warning color="error" fontSize="small" />}
                    {category.level === "Médio" && <TrendingUp color="warning" fontSize="small" />}
                    {category.level === "Baixo" && <CheckCircle color="success" fontSize="small" />}
                    <Typography variant="caption" sx={{ ml: 1 }}>
                      Prioridade {category.level.toLowerCase()}
                    </Typography>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

export default ConsultorRiscos;