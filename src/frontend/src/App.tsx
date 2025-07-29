import React from "react";
import { Routes, Route, Navigate } from "react-router-dom";
import { Box } from "@mui/material";
import Navbar from "./components/Navbar";
import Sidebar from "./components/Sidebar";
import Dashboard from "./pages/Dashboard";
import PayrollPage from "./pages/PayrollPage";
import DocumentsPage from "./pages/DocumentsPage";
import CCTPage from "./pages/CCTPage";
import AuditPage from "./pages/AuditPage";
import ChatbotPage from "./pages/ChatbotPage";
import LoginPage from "./pages/LoginPage";
import { useAuth } from "./hooks/useAuth";

function App() {
  const { isAuthenticated, loading } = useAuth();

  if (loading) {
    return <div>Loading...</div>;
  }

  if (!isAuthenticated) {
    return <LoginPage />;
  }

  return (
    <Box sx={{ display: "flex" }}>
      <Navbar />
      <Sidebar />
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          bgcolor: "background.default",
          p: 3,
          mt: 8, // Account for navbar height
        }}
      >
        <Routes>
          <Route path="/" element={<Navigate to="/dashboard" replace />} />
          <Route path="/dashboard" element={<Dashboard />} />
          <Route path="/payroll/*" element={<PayrollPage />} />
          <Route path="/documents/*" element={<DocumentsPage />} />
          <Route path="/cct/*" element={<CCTPage />} />
          <Route path="/audit/*" element={<AuditPage />} />
          <Route path="/chatbot" element={<ChatbotPage />} />
        </Routes>
      </Box>
    </Box>
  );
}

export default App;
