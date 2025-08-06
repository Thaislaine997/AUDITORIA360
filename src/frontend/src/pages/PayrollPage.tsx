import React, { useState, useEffect } from "react";
import { 
  Container, 
  Typography, 
  Paper, 
  Box, 
  Grid, 
  Card, 
  CardContent, 
  Button,
  Chip,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from "@mui/material";
import { 
  TrendingUp, 
  People, 
  AttachMoney, 
  Warning,
  Refresh,
  PlayArrow 
} from "@mui/icons-material";

interface BusinessFlow {
  client: {
    id: number;
    name: string;
    employee_count: number;
    status: string;
  };
  payroll: {
    latest_competency: {
      id: number;
      year: number;
      month: number;
      status: string;
      total_employees: number;
      total_gross_amount: number;
      divergences_count: number;
    } | null;
    total_competencies: number;
    active_employees: number;
  };
  system_health: {
    auth_validated: boolean;
    cache_active: boolean;
    context_id: string;
    timestamp: string;
  };
  available_actions: string[];
}

const PayrollPage: React.FC = () => {
  const [businessFlow, setBusinessFlow] = useState<BusinessFlow | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [actionLoading, setActionLoading] = useState<string | null>(null);

  // Mock client ID - in real implementation this would come from route params or context
  const clientId = 1;

  useEffect(() => {
    loadBusinessFlow();
  }, []);

  const loadBusinessFlow = async () => {
    try {
      setLoading(true);
      setError(null);
      
      // In a real implementation, this would use proper authentication
      const response = await fetch(`http://localhost:8001/api/core/business-flow/${clientId}`, {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          // 'Authorization': `Bearer ${userToken}` - would be added with real auth
        },
      });

      if (!response.ok) {
        throw new Error(`API Error: ${response.status}`);
      }

      const data = await response.json();
      if (data.success) {
        setBusinessFlow(data.data);
      } else {
        throw new Error(data.message || 'Failed to load business flow');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Unknown error occurred');
      console.error('Error loading business flow:', err);
    } finally {
      setLoading(false);
    }
  };

  const executeAction = async (actionType: string, params: any = {}) => {
    try {
      setActionLoading(actionType);
      
      const response = await fetch(`http://localhost:8001/api/core/business-flow/${clientId}/execute-action`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          type: actionType,
          params: params
        })
      });

      const data = await response.json();
      if (data.success) {
        // In a real implementation, you might want to refresh the business flow
        // or show a success message
        alert(`Action "${actionType}" executed successfully!`);
      } else {
        throw new Error(data.message || 'Action failed');
      }
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Action failed');
    } finally {
      setActionLoading(null);
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4, display: 'flex', justifyContent: 'center' }}>
        <CircularProgress size={60} />
      </Container>
    );
  }

  if (error) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert 
          severity="error" 
          action={
            <Button color="inherit" size="small" onClick={loadBusinessFlow}>
              Retry
            </Button>
          }
        >
          {error}
        </Alert>
      </Container>
    );
  }

  if (!businessFlow) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Alert severity="warning">No business flow data available</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Folha de Pagamento - {businessFlow.client.name}
        </Typography>
        <Button
          startIcon={<Refresh />}
          onClick={loadBusinessFlow}
          variant="outlined"
        >
          Atualizar
        </Button>
      </Box>

      {/* System Health Status */}
      <Box sx={{ mb: 3 }}>
        <Chip 
          label={`Sistema: ${businessFlow.system_health.auth_validated ? 'Conectado' : 'Offline'}`}
          color={businessFlow.system_health.auth_validated ? 'success' : 'error'}
          size="small"
          sx={{ mr: 1 }}
        />
        <Chip 
          label={`Cache: ${businessFlow.system_health.cache_active ? 'Ativo' : 'Fallback'}`}
          color={businessFlow.system_health.cache_active ? 'success' : 'warning'}
          size="small"
          sx={{ mr: 1 }}
        />
        <Chip 
          label={`Sessão: ${businessFlow.system_health.context_id.substring(0, 8)}...`}
          color="info"
          size="small"
        />
      </Box>

      <Grid container spacing={3}>
        {/* Client Overview */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <People sx={{ mr: 1 }} />
                <Typography variant="h6">Cliente</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Funcionários Ativos: {businessFlow.payroll.active_employees}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Status: <Chip label={businessFlow.client.status} size="small" color="success" />
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Latest Payroll */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <AttachMoney sx={{ mr: 1 }} />
                <Typography variant="h6">Última Competência</Typography>
              </Box>
              {businessFlow.payroll.latest_competency ? (
                <>
                  <Typography variant="body2" color="text.secondary">
                    {businessFlow.payroll.latest_competency.month}/{businessFlow.payroll.latest_competency.year}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Funcionários: {businessFlow.payroll.latest_competency.total_employees}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Valor Bruto: R$ {businessFlow.payroll.latest_competency.total_gross_amount?.toLocaleString('pt-BR') || '0,00'}
                  </Typography>
                  <Chip 
                    label={businessFlow.payroll.latest_competency.status} 
                    size="small" 
                    color="primary" 
                  />
                </>
              ) : (
                <Typography variant="body2" color="text.secondary">
                  Nenhuma competência encontrada
                </Typography>
              )}
            </CardContent>
          </Card>
        </Grid>

        {/* Issues & Warnings */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <Warning sx={{ mr: 1 }} />
                <Typography variant="h6">Divergências</Typography>
              </Box>
              <Typography variant="body2" color="text.secondary">
                Divergências Ativas: {businessFlow.payroll.latest_competency?.divergences_count || 0}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Total de Competências: {businessFlow.payroll.total_competencies}
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Available Actions */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Ações Disponíveis
            </Typography>
            <Grid container spacing={2}>
              {businessFlow.available_actions.map((action) => (
                <Grid item key={action}>
                  <Button
                    variant="contained"
                    startIcon={<PlayArrow />}
                    onClick={() => executeAction(action)}
                    disabled={actionLoading === action}
                    sx={{ minWidth: 180 }}
                  >
                    {actionLoading === action ? (
                      <CircularProgress size={20} />
                    ) : (
                      getActionLabel(action)
                    )}
                  </Button>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Business Flow Data (for development) */}
        <Grid item xs={12}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Dados do Fluxo de Negócio (Debug)
            </Typography>
            <TableContainer>
              <Table size="small">
                <TableHead>
                  <TableRow>
                    <TableCell>Propriedade</TableCell>
                    <TableCell>Valor</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  <TableRow>
                    <TableCell>Client ID</TableCell>
                    <TableCell>{businessFlow.client.id}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Context ID</TableCell>
                    <TableCell>{businessFlow.system_health.context_id}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Last Update</TableCell>
                    <TableCell>{new Date(businessFlow.system_health.timestamp).toLocaleString('pt-BR')}</TableCell>
                  </TableRow>
                  <TableRow>
                    <TableCell>Auth Validated</TableCell>
                    <TableCell>{businessFlow.system_health.auth_validated ? 'Sim' : 'Não'}</TableCell>
                  </TableRow>
                </TableBody>
              </Table>
            </TableContainer>
          </Paper>
        </Grid>
      </Grid>
    </Container>
  );
};

function getActionLabel(action: string): string {
  const labels: Record<string, string> = {
    'process_payroll': 'Processar Folha',
    'generate_reports': 'Gerar Relatórios',
    'run_automation': 'Executar Automação',
    'analyze_risks': 'Analisar Riscos',
    'audit_compliance': 'Auditar Conformidade'
  };
  return labels[action] || action;
}

export default PayrollPage;
