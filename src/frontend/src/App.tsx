import React, { Suspense } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { Box, CircularProgress, Typography } from "@mui/material";
import Navbar from "./components/layout/Navbar";
import Sidebar from "./components/layout/Sidebar";
import KeyboardNavigation from "./components/ui/KeyboardNavigation";
import { useAuthStore } from "./stores/authStore";
import { useUIStore } from "./stores/uiStore";
import { useNavigationStore } from "./stores/navigationStore";

// Lazy loaded pages
const Dashboard = React.lazy(() => import("./pages/Dashboard"));
const PayrollPage = React.lazy(() => import("./pages/PayrollPage"));
const DocumentsPage = React.lazy(() => import("./pages/DocumentsPage"));
const CCTPage = React.lazy(() => import("./pages/CCTPage"));
const AuditPage = React.lazy(() => import("./pages/AuditPage"));
const ChatbotPage = React.lazy(() => import("./pages/ChatbotPage"));
const ReportTemplatesPage = React.lazy(() => import("./pages/ReportTemplatesPage"));
const LoginPage = React.lazy(() => import("./pages/LoginPage"));

// New pages for the unified navigation
const PortalDemandas = React.lazy(() => import("./pages/PortalDemandas"));
const ConsultorRiscos = React.lazy(() => import("./pages/ConsultorRiscos"));
const GestaoContabilidades = React.lazy(() => import("./pages/GestaoContabilidades"));
const GestaoClientes = React.lazy(() => import("./pages/GestaoClientes"));
const GerenciamentoUsuarios = React.lazy(() => import("./pages/GerenciamentoUsuarios"));
const RelatoriosAvancados = React.lazy(() => import("./pages/RelatoriosAvancados"));
const MinhaConta = React.lazy(() => import("./pages/MinhaConta"));
const Templates = React.lazy(() => import("./pages/Templates"));
const NeuroSymbolicDemo = React.lazy(() => import("./pages/NeuroSymbolicDemo"));
const ValidacaoIAPage = React.lazy(() => import("./pages/ValidacaoIAPage").then(module => ({ default: module.ValidacaoIAPage })));

// Monthly Control module
const ControleMensalPage = React.lazy(() => import("./pages/ControleMensalPage").then(module => ({ default: module.ControleMensalPage })));

// Gestão de Legislação module
const GestaoLegislacaoPage = React.lazy(() => import("./pages/GestaoLegislacaoPage").then(module => ({ default: module.GestaoLegislacaoPage })));

// Grande Síntese - New pages (Initiative II, III, IV)
const MasteryPaths = React.lazy(() => import("./pages/MasteryPaths"));
const DeveloperPortal = React.lazy(() => import("./pages/DeveloperPortal"));

// Loading component
const LoadingSpinner: React.FC = () => (
  <Box
    sx={{
      display: "flex",
      flexDirection: "column",
      alignItems: "center",
      justifyContent: "center",
      height: "50vh",
      gap: 2,
    }}
  >
    <CircularProgress size={40} />
    <Typography variant="body2" color="text.secondary">
      Carregando...
    </Typography>
  </Box>
);

function App() {
  const { isAuthenticated, loading } = useAuthStore();
  const { sidebarOpen, layoutMode, setLayoutMode } = useUIStore();
  const { sidebarCollapsed } = useNavigationStore();
  
  // Calculate sidebar width
  const getSidebarWidth = () => {
    if (!sidebarOpen) return 0;
    return sidebarCollapsed ? 60 : 240;
  };

  React.useEffect(() => {
    // Initialize auth state
    useAuthStore.getState().checkAuth();
    
    // Initialize Fluxo layout mode
    setLayoutMode(layoutMode);
  }, [layoutMode, setLayoutMode]);

  if (loading) {
    return <LoadingSpinner />;
  }

  if (!isAuthenticated) {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        <LoginPage />
      </Suspense>
    );
  }

  return (
    <KeyboardNavigation>
      <Box sx={{ display: "flex", minHeight: "100vh" }}>
        <Navbar />
        <Sidebar />
        <Box
          component="main"
          sx={{
            flexGrow: 1,
            bgcolor: "background.default",
            p: 3,
            mt: 8, // Account for navbar height
            ml: `${getSidebarWidth()}px`,
            transition: "margin-left 0.3s ease",
            minHeight: "calc(100vh - 64px)",
          }}
        >
          <Suspense fallback={<LoadingSpinner />}>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              
              {/* OPERAÇÃO submenu */}
              <Route path="/demandas" element={<PortalDemandas />} />
              <Route path="/consultor-riscos" element={<ConsultorRiscos />} />
              
              {/* CONTROLE MENSAL module */}
              <Route path="/controle-mensal" element={<ControleMensalPage />} />
              
              {/* GESTÃO DE LEGISLAÇÃO module */}
              <Route path="/gestao-legislacao" element={<GestaoLegislacaoPage />} />
              
              {/* VALIDAÇÃO DE IA - New route for AI validation */}
              <Route path="/validacao-ia" element={<ValidacaoIAPage />} />
              
              {/* GESTÃO submenu */}
              <Route path="/gestao/contabilidades" element={<GestaoContabilidades />} />
              <Route path="/gestao/clientes" element={<GestaoClientes />} />
              <Route path="/gestao/usuarios" element={<GerenciamentoUsuarios />} />
              
              {/* RELATÓRIOS submenu */}
              <Route path="/relatorios/avancados" element={<RelatoriosAvancados />} />
              
              {/* CONFIGURAÇÕES submenu */}
              <Route path="/configuracoes/minha-conta" element={<MinhaConta />} />
              <Route path="/configuracoes/templates" element={<Templates />} />
              
              {/* GRANDE SÍNTESE - New routes */}
              <Route path="/mastery-paths" element={<MasteryPaths />} />
              <Route path="/developer-portal" element={<DeveloperPortal />} />
              
              {/* Neuro-Symbolic Demo */}
              <Route path="/demo" element={<NeuroSymbolicDemo />} />
              
              {/* Legacy routes - keep for backward compatibility */}
              <Route path="/payroll/*" element={<PayrollPage />} />
              <Route path="/documents/*" element={<DocumentsPage />} />
              <Route path="/cct/*" element={<CCTPage />} />
              <Route path="/audit/*" element={<AuditPage />} />
              <Route path="/chatbot" element={<ChatbotPage />} />
              <Route path="/reports/templates" element={<ReportTemplatesPage />} />
            </Routes>
          </Suspense>
        </Box>
      </Box>
    </KeyboardNavigation>
  );
}

export default App;
