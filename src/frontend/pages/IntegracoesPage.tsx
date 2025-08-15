/**
 * 🔗 IntegracoesPage - Sistema de Integrações Externas (Phase 1)
 * 
 * Módulo para configurar integrações com sistemas externos:
 * - ERPs (SAP, TOTVS, Senior, etc.)
 * - Sistemas de RH (Folha de pagamento)
 * - APIs bancárias e financeiras
 * - Conectores com órgãos fiscais
 * 
 * Implementa o "Hub de Conectividade" do manifesto Grand Tomo
 */

import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Paper,
  Box,
  Card,
  CardContent,
  Grid,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  Alert,
  LinearProgress,
  IconButton,
  Switch,
  FormControlLabel
} from '@mui/material';
import {
  Settings,
  CloudSync,
  CheckCircle,
  Error,
  Warning,
  Add,
  Edit,
  Delete,
  Test,
  Refresh,
  AccountBalance,
  Business,
  People,
  Receipt
} from '@mui/icons-material';

interface Integracao {
  id: number;
  nome_sistema: string;
  tipo_sistema: 'ERP' | 'RH' | 'BANCO' | 'FISCAL' | 'OUTROS';
  provider: string;
  status_conexao: 'ATIVO' | 'INATIVO' | 'ERRO' | 'TESTANDO';
  url_api?: string;
  ultima_sincronizacao?: string;
  dados_sincronizados?: number;
  configuracoes: any;
  criado_em: string;
}

const IntegracoesPage: React.FC = () => {
  const [integracoes, setIntegracoes] = useState<Integracao[]>([]);
  const [loading, setLoading] = useState(true);
  const [dialogAberto, setDialogAberto] = useState(false);
  const [integracaoSelecionada, setIntegracaoSelecionada] = useState<Integracao | null>(null);
  const [testando, setTestando] = useState<number | null>(null);

  // Mock data - replace with real API calls
  useEffect(() => {
    const mockIntegracoes: Integracao[] = [
      {
        id: 1,
        nome_sistema: "TOTVS Protheus",
        tipo_sistema: "ERP",
        provider: "TOTVS",
        status_conexao: "ATIVO",
        url_api: "https://api.totvs.com.br/protheus/v1",
        ultima_sincronizacao: "2024-01-15T10:30:00Z",
        dados_sincronizados: 1250,
        configuracoes: {
          tenant: "empresa001",
          database: "P12",
          modules: ["FINA", "GPEA"]
        },
        criado_em: "2024-01-01T00:00:00Z"
      },
      {
        id: 2,
        nome_sistema: "Senior X",
        tipo_sistema: "RH",
        provider: "Senior",
        status_conexao: "ATIVO",
        url_api: "https://api.senior.com.br/hcm/v2",
        ultima_sincronizacao: "2024-01-15T09:15:00Z",
        dados_sincronizados: 847,
        configuracoes: {
          company_id: "12345",
          modules: ["payroll", "employees"]
        },
        criado_em: "2024-01-05T00:00:00Z"
      },
      {
        id: 3,
        nome_sistema: "API Banco do Brasil",
        tipo_sistema: "BANCO",
        provider: "Banco do Brasil",
        status_conexao: "ERRO",
        url_api: "https://api.bb.com.br/pix/v1",
        ultima_sincronizacao: "2024-01-14T16:45:00Z",
        dados_sincronizados: 0,
        configuracoes: {
          client_id: "encrypted_client_id",
          certificate: "cert.p12"
        },
        criado_em: "2024-01-10T00:00:00Z"
      }
    ];

    setTimeout(() => {
      setIntegracoes(mockIntegracoes);
      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ATIVO': return 'success';
      case 'INATIVO': return 'default';
      case 'ERRO': return 'error';
      case 'TESTANDO': return 'warning';
      default: return 'default';
    }
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'ATIVO': return <CheckCircle color="success" />;
      case 'INATIVO': return <Warning color="disabled" />;
      case 'ERRO': return <Error color="error" />;
      case 'TESTANDO': return <CloudSync color="warning" />;
      default: return <Warning />;
    }
  };

  const getTipoIcon = (tipo: string) => {
    switch (tipo) {
      case 'ERP': return <Business />;
      case 'RH': return <People />;
      case 'BANCO': return <AccountBalance />;
      case 'FISCAL': return <Receipt />;
      default: return <Settings />;
    }
  };

  const handleTestarConexao = async (integracaoId: number) => {
    setTestando(integracaoId);
    
    // Simulate testing
    setTimeout(() => {
      setIntegracoes(prev => prev.map(int => 
        int.id === integracaoId 
          ? { ...int, status_conexao: Math.random() > 0.3 ? 'ATIVO' : 'ERRO' }
          : int
      ));
      setTestando(null);
    }, 2000);
  };

  const handleSincronizarManual = async (integracaoId: number) => {
    // Simulate manual sync
    const integracao = integracoes.find(i => i.id === integracaoId);
    if (!integracao) return;

    alert(`Sincronização iniciada para ${integracao.nome_sistema}`);
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" alignItems="center" mb={3}>
          <CircularProgress size={24} sx={{ mr: 2 }} />
          <Typography variant="h6">Carregando integrações...</Typography>
        </Box>
        <LinearProgress />
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box display="flex" justifyContent="between" alignItems="center" mb={4}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            🔗 Central de Integrações
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Hub de conectividade com sistemas externos - Phase 1 Grand Tomo
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<Add />}
          onClick={() => {
            setIntegracaoSelecionada(null);
            setDialogAberto(true);
          }}
        >
          Nova Integração
        </Button>
      </Box>

      {/* Statistics Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Total Integrações
                  </Typography>
                  <Typography variant="h4">
                    {integracoes.length}
                  </Typography>
                </Box>
                <Settings color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Ativas
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    {integracoes.filter(i => i.status_conexao === 'ATIVO').length}
                  </Typography>
                </Box>
                <CheckCircle color="success" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Com Erro
                  </Typography>
                  <Typography variant="h4" color="error.main">
                    {integracoes.filter(i => i.status_conexao === 'ERRO').length}
                  </Typography>
                </Box>
                <Error color="error" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Dados Sincronizados
                  </Typography>
                  <Typography variant="h4">
                    {integracoes.reduce((sum, i) => sum + (i.dados_sincronizados || 0), 0).toLocaleString()}
                  </Typography>
                </Box>
                <CloudSync color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Alert for configuration */}
      <Alert severity="info" sx={{ mb: 3 }}>
        <strong>Momento Surreal:</strong> Configure suas integrações e veja o AUDITORIA360 se conectar automaticamente 
        aos seus sistemas, populando a base de dados sem intervenção manual. A sincronização elimina a necessidade 
        de importações manuais no futuro!
      </Alert>

      {/* Integrations List */}
      <Grid container spacing={3}>
        {integracoes.map((integracao) => (
          <Grid item xs={12} md={6} lg={4} key={integracao.id}>
            <Card sx={{ height: '100%' }}>
              <CardContent>
                <Box display="flex" justifyContent="between" alignItems="start" mb={2}>
                  <Box display="flex" alignItems="center">
                    {getTipoIcon(integracao.tipo_sistema)}
                    <Box ml={1}>
                      <Typography variant="h6" component="div">
                        {integracao.nome_sistema}
                      </Typography>
                      <Typography color="text.secondary" variant="body2">
                        {integracao.provider}
                      </Typography>
                    </Box>
                  </Box>
                  <Chip
                    icon={getStatusIcon(integracao.status_conexao)}
                    label={integracao.status_conexao}
                    color={getStatusColor(integracao.status_conexao) as any}
                    size="small"
                  />
                </Box>

                <Box mb={2}>
                  <Chip 
                    label={integracao.tipo_sistema} 
                    variant="outlined" 
                    size="small"
                    sx={{ mr: 1 }}
                  />
                  {integracao.dados_sincronizados && (
                    <Chip 
                      label={`${integracao.dados_sincronizados} registros`} 
                      variant="outlined" 
                      size="small" 
                    />
                  )}
                </Box>

                {integracao.ultima_sincronizacao && (
                  <Typography variant="body2" color="text.secondary" gutterBottom>
                    Última sinc: {new Date(integracao.ultima_sincronizacao).toLocaleDateString('pt-BR', {
                      day: '2-digit',
                      month: '2-digit', 
                      year: 'numeric',
                      hour: '2-digit',
                      minute: '2-digit'
                    })}
                  </Typography>
                )}

                <Box display="flex" gap={1} mt={2}>
                  <Button
                    size="small"
                    variant="outlined"
                    startIcon={testando === integracao.id ? <CircularProgress size={16} /> : <Test />}
                    onClick={() => handleTestarConexao(integracao.id)}
                    disabled={testando === integracao.id}
                  >
                    Testar
                  </Button>
                  
                  <Button
                    size="small"
                    variant="outlined"
                    startIcon={<Refresh />}
                    onClick={() => handleSincronizarManual(integracao.id)}
                  >
                    Sincronizar
                  </Button>
                  
                  <IconButton
                    size="small"
                    onClick={() => {
                      setIntegracaoSelecionada(integracao);
                      setDialogAberto(true);
                    }}
                  >
                    <Edit />
                  </IconButton>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Configuration Dialog */}
      <Dialog 
        open={dialogAberto} 
        onClose={() => setDialogAberto(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {integracaoSelecionada ? 'Editar Integração' : 'Nova Integração'}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Nome do Sistema"
                variant="outlined"
                defaultValue={integracaoSelecionada?.nome_sistema || ''}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth>
                <InputLabel>Tipo de Sistema</InputLabel>
                <Select
                  defaultValue={integracaoSelecionada?.tipo_sistema || 'ERP'}
                >
                  <MenuItem value="ERP">ERP</MenuItem>
                  <MenuItem value="RH">Recursos Humanos</MenuItem>
                  <MenuItem value="BANCO">Bancário</MenuItem>
                  <MenuItem value="FISCAL">Fiscal</MenuItem>
                  <MenuItem value="OUTROS">Outros</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Provider/Fornecedor"
                variant="outlined"
                defaultValue={integracaoSelecionada?.provider || ''}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="URL da API"
                variant="outlined"
                defaultValue={integracaoSelecionada?.url_api || ''}
              />
            </Grid>
            <Grid item xs={12}>
              <Alert severity="warning">
                <strong>Segurança:</strong> As credenciais serão criptografadas e armazenadas de forma segura. 
                Nunca compartilhe credenciais através de canais inseguros.
              </Alert>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Client ID / Username"
                variant="outlined"
                type="password"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Client Secret / Password"
                variant="outlined"
                type="password"
              />
            </Grid>
            <Grid item xs={12}>
              <FormControlLabel
                control={<Switch defaultChecked={integracaoSelecionada?.status_conexao === 'ATIVO'} />}
                label="Ativar integração após salvar"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogAberto(false)}>
            Cancelar
          </Button>
          <Button 
            variant="contained" 
            onClick={() => {
              // TODO: Implement save logic
              alert('Configuração salva com sucesso!');
              setDialogAberto(false);
            }}
          >
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default IntegracoesPage;