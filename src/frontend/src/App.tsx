import React, { Suspense } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { CircularProgress, Typography, LinearProgress } from "@mui/material";
import Navbar from "./components/layout/Navbar";
import Sidebar from "./components/layout/Sidebar";
import KeyboardNavigation from "./components/ui/KeyboardNavigation";
import { useAuthStore } from "./stores/authStore";
import { useUIStore } from "./stores/uiStore";

// Lazy loaded pages (apenas existentes)
const Dashboard = React.lazy(() => import("./pages/Dashboard"));
const PayrollPage = React.lazy(() => import("./pages/PayrollPage"));
const DocumentsPage = React.lazy(() => import("./pages/DocumentsPage"));
const CCTPage = React.lazy(() => import("./pages/CCTPage"));
const AuditPage = React.lazy(() => import("./pages/AuditPage"));
const ChatbotPage = React.lazy(() => import("./pages/ChatbotPage"));
const ReportTemplatesPage = React.lazy(() => import("./pages/ReportTemplatesPage"));
const LoginPage = React.lazy(() => import("./pages/LoginPage"));
const PortalDemandas = React.lazy(() => import("./pages/PortalDemandas"));
const PortalDemandasDashboard = React.lazy(() => import("./pages/PortalDemandasDashboard"));
const EmpresaDetailPage = React.lazy(() => import("./pages/EmpresaDetailPage"));
const TicketDetailPage = React.lazy(() => import("./pages/TicketDetailPage"));
const TarefaDetailPage = React.lazy(() => import("./pages/TarefaDetailPage"));
const SindicatoDetailPage = React.lazy(() => import("./pages/SindicatoDetailPage"));
const CCTDetailPage = React.lazy(() => import("./pages/CCTDetailPage"));
const AuditoriaDetailPage = React.lazy(() => import("./pages/AuditoriaDetailPage"));
const RelatorioDetailPage = React.lazy(() => import("./pages/RelatorioDetailPage"));
const UploadDetailPage = React.lazy(() => import("./pages/UploadDetailPage"));
const ConsultorRiscos = React.lazy(() => import("./pages/ConsultorRiscos"));
const GestaoContabilidades = React.lazy(() => import("./pages/GestaoContabilidades"));
const GestaoClientes = React.lazy(() => import("./pages/GestaoClientes"));
const GerenciamentoUsuarios = React.lazy(() => import("./pages/GerenciamentoUsuarios"));
const RelatoriosAvancados = React.lazy(() => import("./pages/RelatoriosAvancados"));
const MinhaConta = React.lazy(() => import("./pages/MinhaConta"));
const Templates = React.lazy(() => import("./pages/Templates"));
const ValidacaoIAPage = React.lazy(() => import("./pages/ValidacaoIAPage"));
const ControleMensalPage = React.lazy(() => import("./pages/ControleMensalPage"));
const GestaoLegislacaoPage = React.lazy(() => import("./pages/GestaoLegislacaoPage"));

// Loading component
const LoadingSpinner: React.FC = () => (
  <>
    <CircularProgress size={40} />
    <Typography variant="body2" color="text.secondary">
      Carregando...
    </Typography>
  </>
);

function App() {
  const { isAuthenticated, loading, logout } = useAuthStore();
  const { layoutMode, setLayoutMode } = useUIStore();
  const [sessionExpired, setSessionExpired] = React.useState(false);

  React.useEffect(() => {
    // Initialize auth state
    useAuthStore.getState().checkAuth();
    // Initialize Fluxo layout mode
    setLayoutMode(layoutMode);
    // Listener para sessão expirada
    const onSessionExpired = () => {
      setSessionExpired(true);
      logout();
    };
    window.addEventListener("sessionExpired", onSessionExpired);
    return () => {
      window.removeEventListener("sessionExpired", onSessionExpired);
    };
  }, [layoutMode, setLayoutMode, logout]);

  if (loading) {
    return (
      <>
        <LinearProgress color="primary" style={{ position: 'fixed', top: 0, left: 0, width: '100%', zIndex: 2000 }} />
        <LoadingSpinner />
      </>
    );
  }

  if (!isAuthenticated) {
    return (
      <Suspense fallback={<LoadingSpinner />}>
        {sessionExpired && (
          <div style={{ margin: 16 }}>
            <Typography color="error">Sessão expirada. Faça login novamente.</Typography>
          </div>
        )}
        <LoginPage />
      </Suspense>
    );
  }

  return (
    <KeyboardNavigation>
      <div>
        <Navbar />
        <Sidebar />
        <div>
          <Suspense fallback={<LoadingSpinner />}>
            <Routes>
              <Route path="/" element={<Navigate to="/dashboard" replace />} />
              <Route path="/dashboard" element={<Dashboard />} />
              {/* OPERAÇÃO submenu */}
              <Route path="/demandas" element={<PortalDemandas />} />
              <Route path="/demandas/dashboard" element={<PortalDemandasDashboard />} />
              <Route path="/demandas/empresa/:id" element={<EmpresaDetailPage />} />
              <Route path="/demandas/ticket/:id" element={<TicketDetailPage />} />
              <Route path="/demandas/tarefa/:id" element={<TarefaDetailPage />} />
              <Route path="/demandas/sindicato/:id" element={<SindicatoDetailPage />} />
              <Route path="/demandas/cct/:id" element={<CCTDetailPage />} />
              <Route path="/demandas/auditoria/:id" element={<AuditoriaDetailPage />} />
              <Route path="/demandas/relatorio/:id" element={<RelatorioDetailPage />} />
              <Route path="/demandas/upload/:id" element={<UploadDetailPage />} />
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
              {/* Legacy routes - keep for backward compatibility */}
              <Route path="/payroll/*" element={<PayrollPage />} />
              <Route path="/documents/*" element={<DocumentsPage />} />
              <Route path="/cct/*" element={<CCTPage />} />
              <Route path="/audit/*" element={<AuditPage />} />
              <Route path="/chatbot" element={<ChatbotPage />} />
              <Route path="/reports/templates" element={<ReportTemplatesPage />} />
            </Routes>
          </Suspense>
        </div>
      </div>
    </KeyboardNavigation>
  );
}

export default App;
