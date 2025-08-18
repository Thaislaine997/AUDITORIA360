// Unificação: Dashboard Next.js (autenticação, layout, SEO) + Dashboard legado (métricas, widgets, IA, UI adaptativa)
import React, { useState, useEffect } from "react";
import Head from 'next/head';
import { useRouter } from 'next/router';
import { Container, Typography, Paper, Box, Alert, Chip, Grid } from "@mui/material";
import { Psychology, Speed, Visibility } from "@mui/icons-material";
import { authHelpers } from '../../../lib/supabaseClient';
import { dashboardService, type DashboardMetric } from "../modules/dashboard/dashboardService";
import { usePredictiveLoading, useAdaptiveUI } from "../hooks/useNeuralSignals";
import { useIntentionStore } from "../stores/intentionStore";
import ROICognitivoWidget from "../components/ui/ROICognitivoWidget";

// ...restante do código conforme lido acima...
