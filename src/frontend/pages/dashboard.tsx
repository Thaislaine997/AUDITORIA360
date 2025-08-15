// Unificação: Dashboard Next.js (autenticação, layout, SEO) + Dashboard legado (métricas, widgets, IA, UI adaptativa)
import React, { useState, useEffect } from "react"; // Moved to pages/dashboard/index.tsx
import Head from 'next/head';
import { useRouter } from 'next/router';
import { Container, Typography, Paper, Box, Alert, Chip, Grid } from "@mui/material";
import { Psychology, Speed, Visibility } from "@mui/icons-material";
import { authHelpers } from '../../../lib/supabaseClient';
import { dashboardService, type DashboardMetric } from "../modules/dashboard/dashboardService";
import { usePredictiveLoading, useAdaptiveUI } from "../hooks/useNeuralSignals";
import { useIntentionStore } from "../stores/intentionStore";
import ROICognitivoWidget from "../components/ui/ROICognitivoWidget";

interface User {
  id: string;
  email?: string;
  user_metadata?: {
    full_name?: string;
  };
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null); // Moved to pages/dashboard/index.tsx
  const [loading, setLoading] = useState(true);
  const [metrics, setMetrics] = useState<DashboardMetric[]>([]);
  const [speculativePages, setSpeculativePages] = useState<Record<string, boolean>>({});
  const router = useRouter();

  // Autenticação Next.js/Supabase
  useEffect(() => {
  const checkUser = async () => { // Moved to pages/dashboard/index.tsx
      try {
        const currentUser = await authHelpers.getCurrentUser();
        if (!currentUser) {
          router.push('/login');
          return;
        }
        setUser(currentUser);
      } catch (error) {
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };
    checkUser();
  }, [router]);

  // Dashboard legado: métricas, UI adaptativa, IA // Moved to pages/dashboard/index.tsx
  useEffect(() => {
    const loadMetrics = async () => {
      try {
        const data = await dashboardService.getMetrics();
        setMetrics(data);
      } catch (error) {
        // Silencia erro para não quebrar dashboard
      }
    };
    loadMetrics();
  }, []);

  const { predictions, preloadHighProbabilityTargets } = usePredictiveLoading();
  const { shouldSimplify, loadLevel, adaptationStrategy } = useAdaptiveUI();
  const { currentIntentions } = useIntentionStore();

  useEffect(() => {
    const highProbabilityTargets = Object.entries(predictions || {})
      .filter(([_, probability]) => (typeof probability === 'number' && probability > 0.9))
      .map(([target]) => target);
    if (highProbabilityTargets.length > 0) {
      const speculativeState: Record<string, boolean> = {};
      highProbabilityTargets.forEach(target => {
        speculativeState[target] = true;
        setTimeout(() => {}, 100);
      });
      setSpeculativePages(speculativeState);
      if (typeof preloadHighProbabilityTargets === 'function') {
        preloadHighProbabilityTargets();
      }
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

  const handleSignOut = async () => {
    try {
      await authHelpers.signOut();
      router.push('/');
    } catch (error) {}
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto"></div>
          <p className="mt-4 text-gray-600">Carregando...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null;
  }

  return (
  <> // Moved to pages/dashboard/index.tsx
      <Head>
        <title>Dashboard - Portal AUDITORIA360</title>
        <meta name="description" content="Dashboard do Portal AUDITORIA360 - Gestão completa da folha de pagamento e auditoria inteligente." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      <div className="min-h-screen bg-gray-50">
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <div className="flex items-center">
                <h1 className="text-2xl font-bold text-blue-600">AUDITORIA360</h1>
                <span className="ml-3 text-sm text-gray-500">Portal de Gestão</span>
              </div>
              <div className="flex items-center space-x-4">
                <span className="text-sm text-gray-600">
                  Olá, {user.user_metadata?.full_name || user.email}
                </span>
                <button
                  onClick={handleSignOut}
                  className="bg-red-600 text-white px-4 py-2 rounded-lg text-sm font-medium hover:bg-red-700 transition-colors"
                >
                  Sair
                </button>
              </div>
            </div>
          </div>
        </header>
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          <div className="mb-8">
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Bem-vindo ao Portal AUDITORIA360
            </h2>
            <p className="text-gray-600">
              Sua central de controle para gestão da folha de pagamento e auditoria inteligente.
            </p>
          </div>
          {/* Widgets e métricas do dashboard legado */}
          <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
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
              <Box sx={{ display: 'flex', gap: 1, alignItems: 'center' }}>
                {Object.keys(speculativePages).length > 0 && (
                  <Alert severity="info" icon={<Speed />}>
                    🧠 {Object.keys(speculativePages).length} página(s) pré-renderizada(s)
                  </Alert>
                )}
                {currentIntentions && currentIntentions.length > 0 && (
                  <Alert severity="success" icon={<Visibility />}>
                    {currentIntentions.length} intenção(ões) neural detectada(s)
                  </Alert>
                )}
              </Box>
            </Box>
            {adaptationStrategy && adaptationStrategy.hideAdvancedFeatures && (
              <Alert severity="info" sx={{ mb: 3 }}>
                🧠 Interface simplificada ativada. Recursos avançados ocultados para reduzir sobrecarga cognitiva.
              </Alert>
            )}
            <Grid container spacing={3} sx={{ mb: 4 }}>
              <Grid item xs={12} lg={8}>
                <ROICognitivoWidget 
                  className="h-full"
                  updateFrequency="real-time"
                  tenantId={undefined}
                />
              </Grid>
              <Grid item xs={12} lg={4}>
                <Box sx={{ p: 3, bgcolor: 'background.paper', borderRadius: 2, border: '1px solid', borderColor: 'divider' }}>
                  <Typography variant="h6" gutterBottom color="primary">
                    🌟 Metamorfose Completa
                  </Typography>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                    A Mente Coletiva integrou com sucesso a consciência econômica, estratégica e de segurança 
                    neste widget que demonstra valor tangível aos clientes.
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
                    <Chip label="Consciência Econômica" size="small" color="success" />
                    <Chip label="Consciência Estratégica" size="small" color="primary" />
                    <Chip label="Segurança Integrada" size="small" color="warning" />
                  </Box>
                </Box>
              </Grid>
            </Grid>
            <Grid container spacing={adaptationStrategy && adaptationStrategy.reduceAnimations ? 1 : 3}>
              {metrics
                .filter((_, index) => !adaptationStrategy || !adaptationStrategy.hideAdvancedFeatures || index < 4)
                .map(metric => (
                <Grid item xs={12} md={6} lg={3} key={metric.id}>
                  <Paper 
                    sx={{ 
                      p: 2,
                      border: adaptationStrategy && adaptationStrategy.highlightPrimaryActions && metric.type === 'success' 
                        ? 2 
                        : 0,
                      borderColor: 'success.main',
                      transition: adaptationStrategy && adaptationStrategy.reduceAnimations ? 'none' : 'all 0.3s ease',
                    }}
                  >
                    <Typography
                      variant="h6"
                      sx={{ display: "flex", alignItems: "center", gap: 1 }}
                    >
                      {metric.icon && <span>{metric.icon}</span>}
                      {metric.title}
                      {adaptationStrategy && adaptationStrategy.showHelpHints && (
                        <Chip label="Principal" size="small" color="primary" />
                      )}
                    </Typography>
                    <Typography variant="h4" color={getMetricColor(metric.type)}>
                      {metric.value}
                    </Typography>
                    {metric.trend && (!adaptationStrategy || !adaptationStrategy.hideAdvancedFeatures) && (
                      <Typography variant="body2" color="text.secondary">
                        {dashboardService.getTrendIcon(metric.trend.direction)}{" "}
                        {metric.trend.value}%
                      </Typography>
                    )}
                  </Paper>
                </Grid>
              ))}
            </Grid>
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
        </div>
      </div>
    </>
  );
}

function DashboardModule({ title, description, icon, href }: {
  title: string // Moved to pages/dashboard/index.tsx
  description: string
  icon: string
  href: string
}) {
    return null;
}

function ActivityItem({ title, description, time, status }: {
  title: string // Moved to pages/dashboard/index.tsx
  description: string
  time: string
  status: 'success' | 'info' | 'warning'
}) {
  const statusClasses = {
    success: 'bg-green-100 text-green-600',
    info: 'bg-blue-100 text-blue-600',
    warning: 'bg-yellow-100 text-yellow-600'
  }

  return (
    <div className="flex items-start space-x-3 py-2">
      <div className={`w-2 h-2 rounded-full mt-2 ${statusClasses[status].replace('text-', 'bg-').replace('100', '600')}`}></div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-600">{description}</p>
        <p className="text-xs text-gray-400 mt-1">{time}</p>
      </div>
    </div>
  )
}