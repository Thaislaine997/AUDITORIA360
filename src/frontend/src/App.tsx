import React, { Suspense } from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { Box, CircularProgress, Typography } from "@mui/material";
import Navbar from "./components/layout/Navbar";
import Sidebar from "./components/layout/Sidebar";
import { useAuthStore } from "./stores/authStore";
import { useUIStore } from "./stores/uiStore";

// Lazy loaded pages
const Dashboard = React.lazy(() => import("./pages/Dashboard"));
const PayrollPage = React.lazy(() => import("./pages/PayrollPage"));
const DocumentsPage = React.lazy(() => import("./pages/DocumentsPage"));
const CCTPage = React.lazy(() => import("./pages/CCTPage"));
const AuditPage = React.lazy(() => import("./pages/AuditPage"));
const ChatbotPage = React.lazy(() => import("./pages/ChatbotPage"));
const ReportTemplatesPage = React.lazy(() => import("./pages/ReportTemplatesPage"));
const LoginPage = React.lazy(() => import("./pages/LoginPage"));

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
  const { sidebarOpen } = useUIStore();

  React.useEffect(() => {
    // Initialize auth state
    useAuthStore.getState().checkAuth();
  }, []);

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
          ml: sidebarOpen ? 0 : "-240px",
          transition: "margin-left 0.3s ease",
          minHeight: "calc(100vh - 64px)",
        }}
      >
        <Suspense fallback={<LoadingSpinner />}>
          <Routes>
            <Route path="/" element={<Navigate to="/dashboard" replace />} />
            <Route path="/dashboard" element={<Dashboard />} />
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
  );
}

export default App;
