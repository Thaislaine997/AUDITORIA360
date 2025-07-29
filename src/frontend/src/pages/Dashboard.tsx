import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  CircularProgress,
} from "@mui/material";
import {
  dashboardService,
  type DashboardMetric,
} from "../modules/dashboard/dashboardService";

const Dashboard: React.FC = () => {
  const [metrics, setMetrics] = useState<DashboardMetric[]>([]);
  const [loading, setLoading] = useState(true);

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
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
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
    </Container>
  );
};

export default Dashboard;
