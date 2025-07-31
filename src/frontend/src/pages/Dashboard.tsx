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
  Psychology,
  Nature,
  Timeline,
} from "@mui/icons-material";
import {
  dashboardService,
  type DashboardMetric,
} from "../modules/dashboard/dashboardService";
import ChronosGalaxyView from "../components/chronos/ChronosGalaxyView";
import ChronosAIPanteao from "../components/chronos/ChronosAIPanteao";
import KairosOrganicDashboard from "../components/kairos/KairosOrganicDashboard";
import ComplianceLoom from "../components/kairos/ComplianceLoom";
import DuraLexAI from "../components/kairos/DuraLexAI";

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [chronosMode, setChronosMode] = useState(false);
  const [kairosMode, setKairosMode] = useState(false);
  const [complianceLoomMode, setComplianceLoomMode] = useState(false);
  const [showAIPanteao, setShowAIPanteao] = useState(false);
  const [showDuraLex, setShowDuraLex] = useState(false);

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

  // If Kairós Organic mode is active
  if (kairosMode) {
    return (
      <KairosOrganicDashboard 
        onBackToTraditional={() => setKairosMode(false)}
      />
    );
  }

  // If Compliance Loom mode is active
  if (complianceLoomMode) {
    return (
      <ComplianceLoom 
        onBack={() => setComplianceLoomMode(false)}
      />
    );
  }

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
          <Tooltip title="Ativar Dura Lex IA">
            <Fab
              size="small"
              color="secondary"
              onClick={() => setShowDuraLex(true)}
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

          <Tooltip title="Entrar no KAIRÓS - Bioma Operacional">
            <Fab
              color="success"
              variant="extended"
              onClick={() => setKairosMode(true)}
              sx={{
                background: 'linear-gradient(45deg, #2E7D32, #4CAF50)',
                color: 'white',
                '&:hover': {
                  background: 'linear-gradient(45deg, #1B5E20, #2E7D32)',
                  transform: 'scale(1.05)'
                }
              }}
            >
              <Nature sx={{ mr: 1 }} />
              Ativar KAIRÓS
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

      {/* Kairós introduction card */}
      <Zoom in>
        <Paper
          sx={{
            mt: 2,
            p: 3,
            background: 'linear-gradient(135deg, #2E7D32 0%, #4CAF50 50%, #66BB6A 100%)',
            color: 'white',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'scale(1.02)',
              boxShadow: '0 8px 32px rgba(46, 125, 50, 0.4)'
            }
          }}
          onClick={() => setKairosMode(true)}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 3 }}>
            <Nature sx={{ fontSize: 60, color: '#E8F5E8' }} />
            <Box sx={{ flex: 1 }}>
              <Typography variant="h5" gutterBottom sx={{ fontWeight: 'bold' }}>
                🌱 MANIFESTO KAIRÓS
              </Typography>
              <Typography variant="h6" gutterBottom sx={{ color: '#E8F5E8' }}>
                O Ecossistema de Orquestração Departamental
              </Typography>
              <Typography variant="body1" sx={{ opacity: 0.95 }}>
                Uma nova filosofia orgânica. Visualize o Coração Pulsante da Contabilidade, 
                navegue pelos Rios de Clientes e explore a Floresta de Colaboradores. 
                Sinta o pulso de milhares de clientes e aja no momento exato (Kairós).
              </Typography>
            </Box>
            <Box sx={{ textAlign: 'center' }}>
              <Typography variant="caption" sx={{ opacity: 0.8 }}>
                Clique para entrar
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Zoom>

      {/* Compliance Loom shortcut */}
      <Zoom in>
        <Paper
          sx={{
            mt: 2,
            p: 2,
            background: 'linear-gradient(135deg, #795548 0%, #8D6E63 50%, #A1887F 100%)',
            color: 'white',
            cursor: 'pointer',
            transition: 'all 0.3s ease',
            '&:hover': {
              transform: 'scale(1.01)',
              boxShadow: '0 4px 16px rgba(121, 85, 72, 0.4)'
            }
          }}
          onClick={() => setComplianceLoomMode(true)}
        >
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Timeline sx={{ fontSize: 40, color: '#EFEBE9' }} />
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
                🧵 Tear da Conformidade
              </Typography>
              <Typography variant="body2" sx={{ opacity: 0.9 }}>
                Orquestre eventos no tear do tempo. Visualize a folha como uma tapeçaria, 
                identifique nós (erros) e lance ondas eSocial.
              </Typography>
            </Box>
          </Box>
        </Paper>
      </Zoom>

      {/* AI Dialogs */}
      <ChronosAIPanteao
        open={showAIPanteao}
        onClose={() => setShowAIPanteao(false)}
      />

      <DuraLexAI
        open={showDuraLex}
        onClose={() => setShowDuraLex(false)}
      />
    </Container>
  );
};

export default Dashboard;
