import React from "react";
import ReactDOM from "react-dom/client";
import { BrowserRouter } from "react-router-dom";
import { QueryClient, QueryClientProvider } from "react-query";
import { ThemeProvider, createTheme } from "@mui/material/styles";
import CssBaseline from "@mui/material/CssBaseline";
import App from "./App";

// ACR (Agente de Rastreamento Cinético) - Initialize OpenTelemetry tracing
import "./services/acr";

const queryClient = new QueryClient();

// Fluxo Design System Theme Configuration
const theme = createTheme({
  palette: {
    mode: 'light', // Fluxo uses light mode by default
    primary: {
      main: "#0077FF", // Electric Blue
      contrastText: "#FFFFFF",
    },
    secondary: {
      main: "#10B981", // Mint Green
      contrastText: "#FFFFFF",
    },
    background: {
      default: "#FDFDFD", // Off-white
      paper: "#FFFFFF",
    },
    text: {
      primary: "#1A1A1A", // Main text
      secondary: "#6B7280", // Muted text
    },
    error: {
      main: "#EF4444",
    },
    warning: {
      main: "#F59E0B",
    },
    success: {
      main: "#10B981", // Mint Green
    },
    info: {
      main: "#0077FF", // Electric Blue
    },
  },
  typography: {
    fontFamily: '"Inter", "Segoe UI", "Roboto", -apple-system, BlinkMacSystemFont, sans-serif',
    h1: {
      fontWeight: 700,
    },
    h2: {
      fontWeight: 600,
    },
    h3: {
      fontWeight: 600,
    },
    button: {
      fontWeight: 500,
      textTransform: 'none', // Fluxo uses normal case
    },
  },
  shape: {
    borderRadius: 8, // Fluxo rounded corners
  },
  components: {
    // Enhanced Material-UI components for Fluxo design system
    MuiButton: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          transition: 'all 0.15s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            transform: 'translateY(-1px)',
            boxShadow: '0 4px 20px rgba(0, 0, 0, 0.15)',
          },
          '&:active': {
            transform: 'translateY(1px)',
          },
        },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          borderRadius: 8,
          border: '1px solid #E5E7EB',
          boxShadow: '0 1px 3px rgba(0, 0, 0, 0.1)',
          transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)',
          '&:hover': {
            boxShadow: '0 8px 30px rgba(0, 0, 0, 0.2)',
            transform: 'translateY(-2px)',
            borderColor: '#0077FF',
          },
        },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: {
          '& .MuiOutlinedInput-root': {
            borderRadius: 8,
            transition: 'all 0.15s cubic-bezier(0.4, 0, 0.2, 1)',
            '&:hover fieldset': {
              borderColor: '#0077FF',
              borderWidth: '1.5px',
            },
            '&.Mui-focused fieldset': {
              borderColor: '#0077FF',
              borderWidth: '2px',
              boxShadow: '0 0 0 3px rgba(0, 119, 255, 0.1)',
            },
          },
        },
      },
    },
  },
});

ReactDOM.createRoot(document.getElementById("root")!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <BrowserRouter>
          <App />
        </BrowserRouter>
      </ThemeProvider>
    </QueryClientProvider>
  </React.StrictMode>
);
