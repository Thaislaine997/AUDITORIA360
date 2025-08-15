import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Grid,
  Card,
  CardContent,
  CardActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
} from "@mui/material";
import {
  Add,
  BarChart,
  FilterList,
  GetApp,
  DateRange,
  TrendingUp,
  Assessment,
  PieChart,
  Edit,
  Delete,
} from "@mui/icons-material";

interface Relatorio {
  id: string;
  nome: string;
  descricao: string;
  tipo: "dashboard" | "tabela" | "grafico";
  categoria: "folha" | "auditoria" | "compliance" | "financeiro";
  ultimaGeracao: string;
  status: "ativo" | "rascunho";
}

const RelatoriosAvancados: React.FC = () => {
  const [openDialog, setOpenDialog] = useState(false);
  const [selectedPeriod, setSelectedPeriod] = useState("mes_atual");
  const [selectedCategory, setSelectedCategory] = useState("todos");

  const [relatorios, setRelatorios] = useState<Relatorio[]>([
    {
      id: "1",
      nome: "Análise de Folha Mensal",
      descricao: "Relatório detalhado dos custos de folha por departamento",
      tipo: "dashboard",
      categoria: "folha",
      ultimaGeracao: "2024-01-15",
      status: "ativo",
    },
    {
      id: "2",
      nome: "Conformidade Trabalhista",
      descricao: "Auditoria de conformidade com legislação trabalhista",
      tipo: "tabela",
      categoria: "compliance",
      ultimaGeracao: "2024-01-14",
      status: "ativo",
    },
    {
      id: "3",
      nome: "KPIs de Auditoria",
      descricao: "Indicadores de performance das auditorias realizadas",
      tipo: "grafico",
      categoria: "auditoria",
      ultimaGeracao: "2024-01-13",
      status: "rascunho",
    },
  ]);

  const handleGenerate = (relatorioId: string) => {
    console.log(`Gerando relatório ${relatorioId}...`);
    // Simulate report generation
  };

  const getTypeIcon = (tipo: string) => {
    switch (tipo) {
      case "dashboard": return <Assessment color="primary" />;
      case "tabela": return <BarChart color="secondary" />;
      case "grafico": return <PieChart color="success" />;
      default: return <BarChart />;
    }
  };

  const getTypeColor = (tipo: string) => {
    switch (tipo) {
      case "dashboard": return "primary";
      case "tabela": return "secondary";
      case "grafico": return "success";
      default: return "default";
    }
  };

  const getCategoryLabel = (categoria: string) => {
    switch (categoria) {
      case "folha": return "Folha de Pagamento";
      case "auditoria": return "Auditoria";
      case "compliance": return "Compliance";
      case "financeiro": return "Financeiro";
      default: return categoria;
    }
  };

  const quickReports = [
    {
      nome: "Folha Atual vs Anterior",
      descricao: "Comparativo mensal de folha",
      icon: <TrendingUp />,
    },
    {
      nome: "Riscos Identificados",
      descricao: "Relatório de riscos em aberto",
      icon: <Assessment />,
    },
    {
      nome: "Conformidade Mensal",
      descricao: "Status de conformidade atual",
      icon: <BarChart />,
    },
  ];

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Relatórios Avançados
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Construa e visualize relatórios personalizados para análises profundas.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        {/* Quick Reports */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Relatórios Rápidos
            </Typography>
            <Grid container spacing={2}>
              {quickReports.map((report, index) => (
                <Grid item xs={12} md={4} key={index}>
                  <Card>
                    <CardContent>
                      <Box sx={{ display: "flex", alignItems: "center", gap: 2, mb: 2 }}>
                        {report.icon}
                        <Typography variant="h6" component="div">
                          {report.nome}
                        </Typography>
                      </Box>
                      <Typography variant="body2" color="text.secondary">
                        {report.descricao}
                      </Typography>
                    </CardContent>
                    <CardActions>
                      <Button size="small" startIcon={<GetApp />}>
                        Gerar
                      </Button>
                    </CardActions>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Filters */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: "flex", gap: 2, mb: 3, alignItems: "center" }}>
              <FormControl size="small" sx={{ minWidth: 200 }}>
                <InputLabel>Período</InputLabel>
                <Select
                  value={selectedPeriod}
                  label="Período"
                  onChange={(e) => setSelectedPeriod(e.target.value)}
                >
                  <MenuItem value="mes_atual">Mês Atual</MenuItem>
                  <MenuItem value="mes_anterior">Mês Anterior</MenuItem>
                  <MenuItem value="trimestre">Trimestre</MenuItem>
                  <MenuItem value="ano">Ano</MenuItem>
                  <MenuItem value="personalizado">Personalizado</MenuItem>
                </Select>
              </FormControl>

              <FormControl size="small" sx={{ minWidth: 200 }}>
                <InputLabel>Categoria</InputLabel>
                <Select
                  value={selectedCategory}
                  label="Categoria"
                  onChange={(e) => setSelectedCategory(e.target.value)}
                >
                  <MenuItem value="todos">Todos</MenuItem>
                  <MenuItem value="folha">Folha de Pagamento</MenuItem>
                  <MenuItem value="auditoria">Auditoria</MenuItem>
                  <MenuItem value="compliance">Compliance</MenuItem>
                  <MenuItem value="financeiro">Financeiro</MenuItem>
                </Select>
              </FormControl>

              <Button
                variant="outlined"
                startIcon={<FilterList />}
                sx={{ ml: "auto" }}
              >
                Mais Filtros
              </Button>

              <Button
                variant="contained"
                startIcon={<Add />}
                onClick={() => setOpenDialog(true)}
              >
                Novo Relatório
              </Button>
            </Box>

            {/* Custom Reports List */}
            <Typography variant="h6" gutterBottom>
              Relatórios Personalizados
            </Typography>
            
            <List>
              {relatorios.map((relatorio) => (
                <ListItem key={relatorio.id} divider>
                  <Box sx={{ display: "flex", alignItems: "center", gap: 2, flex: 1 }}>
                    {getTypeIcon(relatorio.tipo)}
                    <Box sx={{ flex: 1 }}>
                      <ListItemText
                        primary={relatorio.nome}
                        secondary={relatorio.descricao}
                      />
                      <Box sx={{ display: "flex", gap: 1, mt: 1 }}>
                        <Chip 
                          label={relatorio.tipo}
                          color={getTypeColor(relatorio.tipo) as any}
                          size="small"
                        />
                        <Chip 
                          label={getCategoryLabel(relatorio.categoria)}
                          variant="outlined"
                          size="small"
                        />
                        <Chip 
                          label={relatorio.status}
                          color={relatorio.status === "ativo" ? "success" : "warning"}
                          size="small"
                        />
                      </Box>
                    </Box>
                  </Box>
                  
                  <ListItemSecondaryAction>
                    <Box sx={{ display: "flex", gap: 1 }}>
                      <Button
                        size="small"
                        variant="contained"
                        startIcon={<GetApp />}
                        onClick={() => handleGenerate(relatorio.id)}
                      >
                        Gerar
                      </Button>
                      <IconButton size="small" color="primary">
                        <Edit />
                      </IconButton>
                      <IconButton size="small" color="error">
                        <Delete />
                      </IconButton>
                    </Box>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Dialog for creating new report */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>Novo Relatório Personalizado</DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Nome do Relatório"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Descrição"
                multiline
                rows={3}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Tipo de Visualização</InputLabel>
                <Select
                  label="Tipo de Visualização"
                  defaultValue=""
                >
                  <MenuItem value="dashboard">Dashboard</MenuItem>
                  <MenuItem value="tabela">Tabela</MenuItem>
                  <MenuItem value="grafico">Gráfico</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Categoria</InputLabel>
                <Select
                  label="Categoria"
                  defaultValue=""
                >
                  <MenuItem value="folha">Folha de Pagamento</MenuItem>
                  <MenuItem value="auditoria">Auditoria</MenuItem>
                  <MenuItem value="compliance">Compliance</MenuItem>
                  <MenuItem value="financeiro">Financeiro</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>
            Cancelar
          </Button>
          <Button variant="contained" onClick={() => setOpenDialog(false)}>
            Criar Relatório
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default RelatoriosAvancados;