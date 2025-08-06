import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  CircularProgress,
  Alert,
  Chip,
} from "@mui/material";
import {
  Psychology,
  Speed,
  Visibility,
} from "@mui/icons-material";

import {
  dashboardService,
  type DashboardMetric,
} from "../modules/dashboard/dashboardService";
import { usePredictiveLoading, useAdaptiveUI } from "../hooks/useNeuralSignals";
import { useIntentionStore } from "../stores/intentionStore";


const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetric[]>([]);
  const [loading, setLoading] = useState(true);
  const [speculativePages, setSpeculativePages] = useState<Record<string, boolean>>({});
  
  // Neuro-Symbolic hooks
  const { predictions, preloadHighProbabilityTargets, isDataPreloaded } = usePredictiveLoading();
  const { shouldSimplify, adaptationStrategy, loadLevel } = useAdaptiveUI();
  const { currentIntentions } = useIntentionStore();

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

  // Speculative rendering: Pre-render pages with 90%+ navigation probability
  useEffect(() => {
    const highProbabilityTargets = Object.entries(predictions)
      .filter(([_, probability]) => probability > 0.9)
      .map(([target, _]) => target);

    if (highProbabilityTargets.length > 0) {
      console.log("🧠 Neuro-Symbolic: Starting speculative rendering for:", highProbabilityTargets);
      
      const speculativeState: Record<string, boolean> = {};
      highProbabilityTargets.forEach(target => {
        speculativeState[target] = true;
        
        // Simulate pre-rendering components in background
        setTimeout(() => {
          console.log(`🚀 Speculative rendering completed for: ${target}`);
        }, 100);
      });
      
      setSpeculativePages(speculativeState);
      preloadHighProbabilityTargets();
    }
  }, [predictions, preloadHighProbabilityTargets]);

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
      {/* Header */}
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
        <Typography variant="h4" gutterBottom>
          Dashboard
          {shouldSimplify && (
            <Chip 
              label={`Modo Adaptivo - Carga Cognitiva: ${loadLevel.toUpperCase()}`}
              color="warning"
              icon={<Psychology />}
              sx={{ ml: 2 }}
            />
          )}
        </Typography>
        
        {/* Neuro-Symbolic Status */}
        <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
          {Object.keys(speculativePages).length > 0 && (
            <Alert severity="info" icon={<Speed />}>
              🧠 {Object.keys(speculativePages).length} página(s) pré-renderizada(s)
            </Alert>
          )}
          
          {currentIntentions.length > 0 && (
            <Alert severity="success" icon={<Visibility />}>
              {currentIntentions.length} intenção(ões) neural detectada(s)
            </Alert>
          )}
        </Box>
      </Box>

      {/* Adaptive UI: Hide advanced features if cognitive load is high */}
      {adaptationStrategy.hideAdvancedFeatures && (
        <Alert severity="info" sx={{ mb: 3 }}>
          🧠 Interface simplificada ativada. Recursos avançados ocultados para reduzir sobrecarga cognitiva.
        </Alert>
      )}

      {/* Traditional metrics grid - adapted based on cognitive load */}
      <Grid container spacing={adaptationStrategy.reduceAnimations ? 1 : 3}>
        {metrics
          .filter((_, index) => !adaptationStrategy.hideAdvancedFeatures || index < 4)
          .map(metric => (
          <Grid item xs={12} md={6} lg={3} key={metric.id}>
            <Paper 
              sx={{ 
                p: 2,
                border: adaptationStrategy.highlightPrimaryActions && metric.type === 'success' 
                  ? 2 
                  : 0,
                borderColor: 'success.main',
                transition: adaptationStrategy.reduceAnimations ? 'none' : 'all 0.3s ease',
              }}
            >
              <Typography
                variant="h6"
                sx={{ display: "flex", alignItems: "center", gap: 1 }}
              >
                {metric.icon && <span>{metric.icon}</span>}
                {metric.title}
                {adaptationStrategy.showHelpHints && (
                  <Chip label="Principal" size="small" color="primary" />
                )}
              </Typography>
              <Typography variant="h4" color={getMetricColor(metric.type)}>
                {metric.value}
              </Typography>
              {metric.trend && !adaptationStrategy.hideAdvancedFeatures && (
                <Typography variant="body2" color="text.secondary">
                  {dashboardService.getTrendIcon(metric.trend.direction)}{" "}
                  {metric.trend.value}%
                </Typography>
              )}
            </Paper>
          </Grid>
        ))}
      </Grid>

      {/* Speculative rendering status for debugging */}
      {Object.keys(speculativePages).length > 0 && (
        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" gutterBottom>
            🧠 Sistema Neuro-Simbólico - Status da Renderização Especulativa
          </Typography>
          <Grid container spacing={1}>
            {Object.entries(speculativePages).map(([page, isPrerendered]) => (
              <Grid item key={page}>
                <Chip
                  label={`${page} (${isPrerendered ? 'Pré-renderizado' : 'Aguardando'})`}
                  color={isPrerendered ? 'success' : 'default'}
                  size="small"
                />
              </Grid>
            ))}
          </Grid>
        </Box>
      )}
    </Container>
  );
};

export default Dashboard;
