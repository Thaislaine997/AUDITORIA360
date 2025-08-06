import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Grid,
  Paper,
  Box,
  Button,
  Card,
  CardContent,
  CardActions,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Tooltip,
  Alert,
  Tabs,
  Tab,
  Link,
  Accordion,
  AccordionSummary,
  AccordionDetails,
} from "@mui/material";
import {
  Add,
  ContentCopy,
  Delete,
  Visibility,
  VisibilityOff,
  Code,
  Description,
  Security,
  Analytics,
  ExpandMore,
  Launch,
  Key,
  Monitor,
} from "@mui/icons-material";

interface APIKey {
  id: string;
  name: string;
  key: string;
  createdAt: string;
  lastUsed: string;
  requestCount: number;
  status: 'active' | 'revoked';
  permissions: string[];
}

interface APIUsageLog {
  timestamp: string;
  endpoint: string;
  method: string;
  statusCode: number;
  responseTime: number;
  userAgent: string;
}

const DeveloperPortal: React.FC = () => {
  const [activeTab, setActiveTab] = useState(0);
  const [apiKeys, setApiKeys] = useState<APIKey[]>([]);
  const [usageLogs, setUsageLogs] = useState<APIUsageLog[]>([]);
  const [showCreateKeyDialog, setShowCreateKeyDialog] = useState(false);
  const [newKeyName, setNewKeyName] = useState("");
  const [selectedPermissions, setSelectedPermissions] = useState<string[]>([]);
  const [visibleKeys, setVisibleKeys] = useState<Set<string>>(new Set());

  // Mock data initialization
  useEffect(() => {
    setApiKeys([
      {
        id: "key-1",
        name: "Produção Principal",
        key: "ak_prod_1234567890abcdef",
        createdAt: "2024-01-15",
        lastUsed: "2024-01-20",
        requestCount: 15420,
        status: "active",
        permissions: ["read:employees", "read:payroll", "write:reports"]
      },
      {
        id: "key-2",
        name: "Desenvolvimento",
        key: "ak_dev_abcdef1234567890",
        createdAt: "2024-01-10",
        lastUsed: "2024-01-19",
        requestCount: 2340,
        status: "active",
        permissions: ["read:employees", "read:payroll"]
      }
    ]);

    setUsageLogs([
      {
        timestamp: "2024-01-20 14:30:22",
        endpoint: "/api/v1/employees",
        method: "GET",
        statusCode: 200,
        responseTime: 145,
        userAgent: "AUDITORIA360-SDK/1.0"
      },
      {
        timestamp: "2024-01-20 14:28:15",
        endpoint: "/api/v1/payroll/calculate",
        method: "POST",
        statusCode: 200,
        responseTime: 892,
        userAgent: "PostmanRuntime/7.26.8"
      },
      {
        timestamp: "2024-01-20 14:25:03",
        endpoint: "/api/v1/reports",
        method: "GET",
        statusCode: 200,
        responseTime: 234,
        userAgent: "AUDITORIA360-SDK/1.0"
      }
    ]);
  }, []);

  const handleCreateKey = () => {
    if (!newKeyName.trim()) return;

    const newKey: APIKey = {
      id: `key-${Date.now()}`,
      name: newKeyName,
      key: `ak_${Math.random().toString(36).substr(2, 16)}`,
      createdAt: new Date().toISOString().split('T')[0],
      lastUsed: "Nunca",
      requestCount: 0,
      status: "active",
      permissions: selectedPermissions
    };

    setApiKeys([...apiKeys, newKey]);
    setShowCreateKeyDialog(false);
    setNewKeyName("");
    setSelectedPermissions([]);
  };

  const toggleKeyVisibility = (keyId: string) => {
    const newVisible = new Set(visibleKeys);
    if (newVisible.has(keyId)) {
      newVisible.delete(keyId);
    } else {
      newVisible.add(keyId);
    }
    setVisibleKeys(newVisible);
  };

  const copyToClipboard = (text: string) => {
    navigator.clipboard.writeText(text);
    // In a real app, show success toast
    console.log("Copied to clipboard:", text);
  };

  const revokeKey = (keyId: string) => {
    setApiKeys(apiKeys.map(key => 
      key.id === keyId ? { ...key, status: 'revoked' as const } : key
    ));
  };

  const availablePermissions = [
    "read:employees",
    "write:employees", 
    "read:payroll",
    "write:payroll",
    "read:reports",
    "write:reports",
    "read:audit",
    "write:audit",
    "admin:all"
  ];

  const TabPanel = ({ children, value, index }: any) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ py: 3 }}>{children}</Box>}
    </div>
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <Code sx={{ mr: 2 }} />
          Portal de Desenvolvedores
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Gerencie suas chaves de API, monitore o uso e acesse a documentação
        </Typography>
      </Box>

      {/* Info Card */}
      <Alert severity="info" sx={{ mb: 3 }}>
        <Typography variant="body2">
          🚀 <strong>API-as-a-Product</strong> - Nossa API está disponível para integração com seus sistemas. 
          Crie chaves de API seguras e monitore seu uso em tempo real.
        </Typography>
      </Alert>

      {/* Tabs */}
      <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 3 }}>
        <Tabs value={activeTab} onChange={(_, newValue) => setActiveTab(newValue)}>
          <Tab icon={<Key />} label="Chaves de API" />
          <Tab icon={<Monitor />} label="Logs de Uso" />
          <Tab icon={<Description />} label="Documentação" />
          <Tab icon={<Analytics />} label="Estatísticas" />
        </Tabs>
      </Box>

      {/* API Keys Tab */}
      <TabPanel value={activeTab} index={0}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
          <Typography variant="h6">Suas Chaves de API</Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={() => setShowCreateKeyDialog(true)}
          >
            Nova Chave
          </Button>
        </Box>

        <Grid container spacing={3}>
          {apiKeys.map((apiKey) => (
            <Grid item xs={12} key={apiKey.id}>
              <Card sx={{ 
                border: apiKey.status === 'revoked' ? '1px solid #f44336' : '1px solid #e0e0e0',
                opacity: apiKey.status === 'revoked' ? 0.6 : 1
              }}>
                <CardContent>
                  <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                    <Box>
                      <Typography variant="h6">{apiKey.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        Criada em {apiKey.createdAt} • Último uso: {apiKey.lastUsed}
                      </Typography>
                    </Box>
                    <Chip 
                      label={apiKey.status === 'active' ? 'Ativa' : 'Revogada'}
                      color={apiKey.status === 'active' ? 'success' : 'error'}
                      size="small"
                    />
                  </Box>

                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                    <TextField
                      fullWidth
                      value={visibleKeys.has(apiKey.id) ? apiKey.key : '•'.repeat(20)}
                      InputProps={{
                        readOnly: true,
                        endAdornment: (
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Tooltip title={visibleKeys.has(apiKey.id) ? "Ocultar" : "Mostrar"}>
                              <IconButton onClick={() => toggleKeyVisibility(apiKey.id)}>
                                {visibleKeys.has(apiKey.id) ? <VisibilityOff /> : <Visibility />}
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Copiar">
                              <IconButton onClick={() => copyToClipboard(apiKey.key)}>
                                <ContentCopy />
                              </IconButton>
                            </Tooltip>
                          </Box>
                        )
                      }}
                    />
                  </Box>

                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" sx={{ mb: 1 }}>Permissões:</Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {apiKey.permissions.map((permission) => (
                        <Chip key={permission} label={permission} size="small" variant="outlined" />
                      ))}
                    </Box>
                  </Box>

                  <Typography variant="body2" color="text.secondary">
                    {apiKey.requestCount.toLocaleString()} requisições realizadas
                  </Typography>
                </CardContent>

                {apiKey.status === 'active' && (
                  <CardActions>
                    <Button 
                      size="small" 
                      color="error"
                      startIcon={<Delete />}
                      onClick={() => revokeKey(apiKey.id)}
                    >
                      Revogar
                    </Button>
                  </CardActions>
                )}
              </Card>
            </Grid>
          ))}
        </Grid>
      </TabPanel>

      {/* Usage Logs Tab */}
      <TabPanel value={activeTab} index={1}>
        <Typography variant="h6" sx={{ mb: 3 }}>Logs de Uso da API</Typography>
        
        <TableContainer component={Paper}>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Timestamp</TableCell>
                <TableCell>Endpoint</TableCell>
                <TableCell>Método</TableCell>
                <TableCell>Status</TableCell>
                <TableCell>Tempo (ms)</TableCell>
                <TableCell>User Agent</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {usageLogs.map((log, index) => (
                <TableRow key={index}>
                  <TableCell>{log.timestamp}</TableCell>
                  <TableCell>
                    <code>{log.endpoint}</code>
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={log.method} 
                      size="small"
                      color={log.method === 'GET' ? 'primary' : 'secondary'}
                    />
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={log.statusCode}
                      size="small"
                      color={log.statusCode === 200 ? 'success' : 'error'}
                    />
                  </TableCell>
                  <TableCell>{log.responseTime}ms</TableCell>
                  <TableCell>
                    <code style={{ fontSize: '0.8rem' }}>{log.userAgent}</code>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </TabPanel>

      {/* Documentation Tab */}
      <TabPanel value={activeTab} index={2}>
        <Typography variant="h6" sx={{ mb: 3 }}>Documentação da API</Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Description sx={{ mr: 1 }} />
                  Referência da API
                </Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  Documentação completa de todos os endpoints disponíveis
                </Typography>
                <Button 
                  variant="outlined" 
                  endIcon={<Launch />}
                  fullWidth
                >
                  Ver Documentação OpenAPI
                </Button>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Code sx={{ mr: 1 }} />
                  SDKs e Exemplos
                </Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  Bibliotecas e códigos de exemplo para diferentes linguagens
                </Typography>
                <Button 
                  variant="outlined" 
                  endIcon={<Launch />}
                  fullWidth
                >
                  Acessar GitHub
                </Button>
              </CardContent>
            </Card>
          </Grid>
        </Grid>

        <Box sx={{ mt: 4 }}>
          <Typography variant="h6" sx={{ mb: 2 }}>Guia de Início Rápido</Typography>
          
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography>1. Autenticação</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body2" component="div">
                <Box sx={{ mb: 2 }}>
                  Inclua sua chave de API no header de todas as requisições:
                </Box>
                <Paper sx={{ p: 2, bgcolor: 'grey.100' }}>
                  <code>Authorization: Bearer SUA_CHAVE_DE_API</code>
                </Paper>
              </Typography>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography>2. Rate Limiting</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Typography variant="body2">
                As requisições são limitadas a 1000 por hora por chave de API. 
                O header X-RateLimit-Remaining indica quantas requisições restam.
              </Typography>
            </AccordionDetails>
          </Accordion>

          <Accordion>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Typography>3. Exemplo de Requisição</Typography>
            </AccordionSummary>
            <AccordionDetails>
              <Paper sx={{ p: 2, bgcolor: 'grey.100' }}>
                <code>
                  curl -H "Authorization: Bearer SUA_CHAVE" <br/>
                  https://api.auditoria360.com/v1/employees
                </code>
              </Paper>
            </AccordionDetails>
          </Accordion>
        </Box>
      </TabPanel>

      {/* Statistics Tab */}
      <TabPanel value={activeTab} index={3}>
        <Typography variant="h6" sx={{ mb: 3 }}>Estatísticas de Uso</Typography>
        
        <Grid container spacing={3}>
          <Grid item xs={12} md={3}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="primary">
                  {apiKeys.reduce((sum, key) => sum + key.requestCount, 0).toLocaleString()}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total de Requisições
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={3}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="success.main">
                  {apiKeys.filter(key => key.status === 'active').length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Chaves Ativas
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={3}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="info.main">
                  245ms
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Tempo Médio de Resposta
                </Typography>
              </CardContent>
            </Card>
          </Grid>

          <Grid item xs={12} md={3}>
            <Card>
              <CardContent sx={{ textAlign: 'center' }}>
                <Typography variant="h4" color="success.main">
                  99.8%
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Uptime
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </TabPanel>

      {/* Create API Key Dialog */}
      <Dialog open={showCreateKeyDialog} onClose={() => setShowCreateKeyDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Criar Nova Chave de API</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Nome da Chave"
            fullWidth
            variant="outlined"
            value={newKeyName}
            onChange={(e) => setNewKeyName(e.target.value)}
            sx={{ mb: 3 }}
          />
          
          <Typography variant="body2" sx={{ mb: 2 }}>
            Selecione as permissões:
          </Typography>
          
          <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
            {availablePermissions.map((permission) => (
              <Chip
                key={permission}
                label={permission}
                clickable
                color={selectedPermissions.includes(permission) ? 'primary' : 'default'}
                onClick={() => {
                  if (selectedPermissions.includes(permission)) {
                    setSelectedPermissions(selectedPermissions.filter(p => p !== permission));
                  } else {
                    setSelectedPermissions([...selectedPermissions, permission]);
                  }
                }}
              />
            ))}
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowCreateKeyDialog(false)}>Cancelar</Button>
          <Button onClick={handleCreateKey} variant="contained" disabled={!newKeyName.trim()}>
            Criar
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default DeveloperPortal;