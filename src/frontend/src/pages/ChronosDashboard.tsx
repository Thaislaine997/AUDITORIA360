import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  CircularProgress,
  Fab,
  Tooltip,
  Zoom,
} from "@mui/material";
import { 
  RocketLaunch, 
  Dashboard as DashboardIcon,
  Psychology 
} from "@mui/icons-material";
import {
  dashboardService,
  type DashboardMetric,
} from "../modules/dashboard/dashboardService";
import ChronosGalaxyView from "../components/chronos/ChronosGalaxyView";
import ChronosAIPanteao from "../components/chronos/ChronosAIPanteao";

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [chronosMode, setChronosMode] = useState(false);
  const [showAIPanteao, setShowAIPanteao] = useState(false);

  useEffect(() => {
    const loadMetrics = async () => {
      try {
        const data = await dashboardService.getMetrics();
        setMetrics(data);
      } catch (error) {
        console.error("Error loading dashboard metrics:", error);
      } finally {
        setLoading(false);
      }
    };

    loadMetrics();
  }, []);

  const getMetricColor = (type: string) => {
    switch (type) {
      case "success":
        return "success.main";
      case "warning":
        return "warning.main";
      case "danger":
        return "error.main";
      case "info":
        return "info.main";
      default:
        return "primary.main";
    }
  };

  // If Chronos mode is active, render the 3D galaxy view
  if (chronosMode) {
    return (
      <>
        <ChronosGalaxyView onBackToTraditional={() => setChronosMode(false)} />
        
        {/* AI Panteão floating action button in 3D mode */}
        <Tooltip title="Abrir Panteão IA" placement="left">
          <Fab
            color="secondary"
            onClick={() => setShowAIPanteao(true)}
            sx={{
              position: 'fixed',
              bottom: 32,
              right: 32,
              zIndex: 1001,
              background: 'linear-gradient(45deg, #ff6b6b, #4ecdc4)',
              '&:hover': {
                background: 'linear-gradient(45deg, #ff5252, #26a69a)',
                transform: 'scale(1.1)'
              }
            }}
          >
            <Psychology />
          </Fab>
        </Tooltip>

        <ChronosAIPanteao
          open={showAIPanteao}
          onClose={() => setShowAIPanteao(false)}
        />
      </>
    );
  }

  // Traditional dashboard view with Chronos activation option
  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, textAlign: "center" }}>
        <CircularProgress />
        <Typography variant="h6" sx={{ mt: 2 }}>
          Carregando dashboard...
        </Typography>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header with Chronos activation */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
        </Typography>
        
        <Box sx={{ display: 'flex', gap: 2 }}>
          <Tooltip title="Ativar Panteão IA">
            <Fab
              size="small"
              color="secondary"
              onClick={() => setShowAIPanteao(true)}
              sx={{
                background: 'linear-gradient(45deg, #ff6b6b, #4ecdc4)',
                '&:hover': {
                  background: 'linear-gradient(45deg, #ff5252, #26a69a)',
                }
              }}
            >
              <Psychology />
            </Fab>
          </Tooltip>
          
          <Tooltip title="Entrar no CHRONOS - Consciência Operacional">
            <Fab
              color="primary"
              variant="extended"
              onClick={() => setChronosMode(true)}
              sx={{
                background: 'linear-gradient(45deg, #1a1a2e, #16213e)',
                color: 'white',
                '&:hover': {
                  background: 'linear-gradient(45deg, #0f3460, #1a1a2e)',
                  transform: 'scale(1.05)'
                }
              }}
            >
              <RocketLaunch sx={{ mr: 1 }} />
              Ativar CHRONOS
            </Fab>
          </Tooltip>
        </Box>
      </Box>

      {/* Traditional metrics grid */}
      <Grid container spacing={3}>
        {metrics.map(metric => (
          <Grid item xs={12} md={6} lg={3} key={metric.id}>
            <Paper sx={{ p: 2 }}>
              <Typography
                variant="h6"
                sx={{ display: "flex", alignItems: "center", gap: 1 }}
              >
                {metric.icon && <span>{metric.icon}</span>}
                {metric.title}
              </Typography>
              <Typography variant="h4" color={getMetricColor(metric.type)}>
                {metric.value}
              </Typography>
              {metric.trend && (
                <Typography variant="body2" color="text.secondary">
                  {dashboardService.getTrendIcon(metric.trend.direction)}{" "}
                  {metric.trend.value}%
                </Typography>
              )}
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Chronos introduction card */}
      <Zoom in>
        <Paper
          sx={{
            mt: 4,
            p: 3,
            background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
            color: 'white',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'scale(1.02)',
              boxShadow: '0 8px 32px rgba(0,0,0,0.3)'
            }
          }}
          onClick={() => setChronosMode(true)}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
            <RocketLaunch sx={{ fontSize: 60, color: '#4ecdc4' }} />
            <Box sx={{ flex: 1 }}>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
                🌌 PROJETO CHRONOS
              </Typography>
              <Typography variant="h6" gutterBottom sx={{ color: '#4ecdc4' }}>
                A Consciência Operacional Viva
              </Typography>
              <Typography variant="body1" sx={{ opacity: 0.9 }}>
                Abandone a metáfora de "páginas e abas". Entre em um universo onde cada 
                estrela é uma Contabilidade, cada planeta é um Cliente, e você orquestra 
                todo o ecossistema contábil através de um espaço tridimensional vivo.
              </Typography>
            </Box>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="caption" sx={{ opacity: 0.7 }}>
                Clique para entrar
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Zoom>

      {/* AI Panteão Dialog */}
      <ChronosAIPanteao
        open={showAIPanteao}
        onClose={() => setShowAIPanteao(false)}
      />
    </Container>
  );
};

export default Dashboard;