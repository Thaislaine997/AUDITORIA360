/**
 * 💰 LancamentosContabeisPage - Gestão de Lançamentos Contábeis (Phase 2)
 * 
 * Interface para visualizar e aprovar lançamentos contábeis automáticos:
 * - Lançamentos gerados pela auditoria de folha
 * - Aprovação/rejeição de lançamentos em lote
 * - Visualização de débitos e créditos
 * - Integração com plano de contas
 * 
 * Implementa o "Fechamento Automático" do manifesto Grand Tomo
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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  Checkbox,
  IconButton,
  Collapse,
  Tooltip
} from '@mui/material';
import {
  AccountBalance,
  CheckCircle,
  Cancel,
  ExpandMore,
  ExpandLess,
  Visibility,
  Edit,
  Download,
  TrendingUp,
  TrendingDown,
  AccountBalanceWallet,
  ReceiptLong
} from '@mui/icons-material';

interface LancamentoContabil {
  id: number;
  numero_lancamento: string;
  data_lancamento: string;
  historico: string;
  valor_total: number;
  origem_lancamento: string;
  referencia_origem_id?: number;
  status_lancamento: 'RASCUNHO' | 'APROVADO' | 'CONTABILIZADO' | 'CANCELADO';
  aprovado_por?: string;
  aprovado_em?: string;
  empresa_nome: string;
  itens: LancamentoItem[];
}

interface LancamentoItem {
  id: number;
  conta_codigo: string;
  conta_nome: string;
  tipo_movimentacao: 'DEBITO' | 'CREDITO';
  valor: number;
  historico_item?: string;
}

const LancamentosContabeisPage: React.FC = () => {
  const [lancamentos, setLancamentos] = useState<LancamentoContabil[]>([]);
  const [loading, setLoading] = useState(true);
  const [filtroStatus, setFiltroStatus] = useState<string>('TODOS');
  const [filtroOrigem, setFiltroOrigem] = useState<string>('TODOS');
  const [lancamentoDetalhes, setLancamentoDetalhes] = useState<LancamentoContabil | null>(null);
  const [dialogDetalhesAberto, setDialogDetalhesAberto] = useState(false);
  const [lancamentosSelecionados, setLancamentosSelecionados] = useState<number[]>([]);
  const [expandedRows, setExpandedRows] = useState<Set<number>>(new Set());

  // Mock data
  useEffect(() => {
    const mockLancamentos: LancamentoContabil[] = [
      {
        id: 1,
        numero_lancamento: "LAN-2024-001",
        data_lancamento: "2024-01-15",
        historico: "Provisão Folha de Pagamento - Janeiro/2024",
        valor_total: 85750.50,
        origem_lancamento: "AUDITORIA_FOLHA",
        referencia_origem_id: 123,
        status_lancamento: "RASCUNHO",
        empresa_nome: "Empresa ABC Ltda",
        itens: [
          {
            id: 1,
            conta_codigo: "3.1.1.01.001",
            conta_nome: "Salários e Ordenados",
            tipo_movimentacao: "DEBITO",
            valor: 65000.00,
            historico_item: "Salários Janeiro/2024"
          },
          {
            id: 2,
            conta_codigo: "3.1.1.02.001", 
            conta_nome: "Encargos Sociais",
            tipo_movimentacao: "DEBITO",
            valor: 20750.50,
            historico_item: "INSS, FGTS Janeiro/2024"
          },
          {
            id: 3,
            conta_codigo: "2.1.1.01.001",
            conta_nome: "Salários a Pagar",
            tipo_movimentacao: "CREDITO",
            valor: 52500.00,
            historico_item: "Valores líquidos a pagar"
          },
          {
            id: 4,
            conta_codigo: "2.1.1.02.001",
            conta_nome: "INSS a Recolher",
            tipo_movimentacao: "CREDITO",
            valor: 18750.00,
            historico_item: "INSS Janeiro/2024"
          },
          {
            id: 5,
            conta_codigo: "2.1.1.03.001", 
            conta_nome: "FGTS a Recolher",
            tipo_movimentacao: "CREDITO",
            valor: 14500.50,
            historico_item: "FGTS Janeiro/2024"
          }
        ]
      },
      {
        id: 2,
        numero_lancamento: "LAN-2024-002",
        data_lancamento: "2024-01-16",
        historico: "Ajustes Auditoria - Horas Extras CCT",
        valor_total: 3250.75,
        origem_lancamento: "AUDITORIA_FOLHA",
        referencia_origem_id: 124,
        status_lancamento: "APROVADO",
        aprovado_por: "João Contador",
        aprovado_em: "2024-01-16T14:30:00Z",
        empresa_nome: "Empresa XYZ S.A.",
        itens: [
          {
            id: 6,
            conta_codigo: "3.1.1.01.002",
            conta_nome: "Horas Extras",
            tipo_movimentacao: "DEBITO",
            valor: 3250.75,
            historico_item: "Ajuste horas extras conforme CCT"
          },
          {
            id: 7,
            conta_codigo: "2.1.1.01.001",
            conta_nome: "Salários a Pagar", 
            tipo_movimentacao: "CREDITO",
            valor: 3250.75,
            historico_item: "Complemento folha Janeiro/2024"
          }
        ]
      }
    ];

    setTimeout(() => {
      setLancamentos(mockLancamentos);
      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'RASCUNHO': return 'warning';
      case 'APROVADO': return 'success';
      case 'CONTABILIZADO': return 'info';
      case 'CANCELADO': return 'error';
      default: return 'default';
    }
  };

  const getOrigemLabel = (origem: string) => {
    switch (origem) {
      case 'AUDITORIA_FOLHA': return 'Auditoria de Folha';
      case 'AUDITORIA_IA': return 'Auditoria IA';
      case 'MANUAL': return 'Manual';
      default: return origem;
    }
  };

  const handleAprovarLancamento = (lancamentoId: number) => {
    setLancamentos(prev => prev.map(l => 
      l.id === lancamentoId 
        ? { 
            ...l, 
            status_lancamento: 'APROVADO',
            aprovado_por: 'Sistema',
            aprovado_em: new Date().toISOString()
          }
        : l
    ));
  };

  const handleRejeitarLancamento = (lancamentoId: number) => {
    setLancamentos(prev => prev.map(l => 
      l.id === lancamentoId 
        ? { ...l, status_lancamento: 'CANCELADO' }
        : l
    ));
  };

  const handleAprovarSelecionados = () => {
    if (lancamentosSelecionados.length === 0) {
      alert('Selecione pelo menos um lançamento');
      return;
    }

    const confirmacao = window.confirm(
      `Aprovar ${lancamentosSelecionados.length} lançamento(s) selecionado(s)?`
    );

    if (confirmacao) {
      setLancamentos(prev => prev.map(l => 
        lancamentosSelecionados.includes(l.id)
          ? { 
              ...l, 
              status_lancamento: 'APROVADO',
              aprovado_por: 'Sistema',
              aprovado_em: new Date().toISOString()
            }
          : l
      ));
      setLancamentosSelecionados([]);
    }
  };

  const toggleRowExpanded = (lancamentoId: number) => {
    const newExpanded = new Set(expandedRows);
    if (newExpanded.has(lancamentoId)) {
      newExpanded.delete(lancamentoId);
    } else {
      newExpanded.add(lancamentoId);
    }
    setExpandedRows(newExpanded);
  };

  const lancamentosFiltrados = lancamentos.filter(l => {
    if (filtroStatus !== 'TODOS' && l.status_lancamento !== filtroStatus) return false;
    if (filtroOrigem !== 'TODOS' && l.origem_lancamento !== filtroOrigem) return false;
    return true;
  });

  const totalRascunhos = lancamentos.filter(l => l.status_lancamento === 'RASCUNHO').length;
  const totalAprovados = lancamentos.filter(l => l.status_lancamento === 'APROVADO').length;
  const valorTotalRascunhos = lancamentos
    .filter(l => l.status_lancamento === 'RASCUNHO')
    .reduce((sum, l) => sum + l.valor_total, 0);

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" alignItems="center" justifyContent="center" minHeight="400px">
          <Typography variant="h6">Carregando lançamentos...</Typography>
        </Box>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box display="flex" justifyContent="between" alignItems="center" mb={4}>
        <Box>
          <Typography variant="h4" component="h1" gutterBottom>
            💰 Lançamentos Contábeis
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Gestão de lançamentos automáticos - Phase 2 Grand Tomo
          </Typography>
        </Box>
        <Button
          variant="contained"
          startIcon={<CheckCircle />}
          onClick={handleAprovarSelecionados}
          disabled={lancamentosSelecionados.length === 0}
        >
          Aprovar Selecionados ({lancamentosSelecionados.length})
        </Button>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Aguardando Aprovação
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    {totalRascunhos}
                  </Typography>
                </Box>
                <ReceiptLong color="warning" sx={{ fontSize: 40 }} />
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
                    Aprovados
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    {totalAprovados}
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
                    Valor Pendente
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    R$ {valorTotalRascunhos.toLocaleString('pt-BR', {
                      minimumFractionDigits: 2
                    })}
                  </Typography>
                </Box>
                <AccountBalanceWallet color="warning" sx={{ fontSize: 40 }} />
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
                    Total Lançamentos
                  </Typography>
                  <Typography variant="h4">
                    {lancamentos.length}
                  </Typography>
                </Box>
                <AccountBalance color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Momento Surreal Alert */}
      <Alert severity="success" sx={{ mb: 3 }}>
        <strong>Momento Surreal:</strong> Os lançamentos foram gerados automaticamente pelo Robô Auditor 
        após processar a folha de pagamento. Os débitos e créditos já estão balanceados e prontos 
        para aprovação. Isso elimina horas de trabalho manual!
      </Alert>

      {/* Filters */}
      <Box display="flex" gap={2} mb={3}>
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={filtroStatus}
            label="Status"
            onChange={(e) => setFiltroStatus(e.target.value)}
          >
            <MenuItem value="TODOS">Todos</MenuItem>
            <MenuItem value="RASCUNHO">Rascunho</MenuItem>
            <MenuItem value="APROVADO">Aprovado</MenuItem>
            <MenuItem value="CONTABILIZADO">Contabilizado</MenuItem>
            <MenuItem value="CANCELADO">Cancelado</MenuItem>
          </Select>
        </FormControl>
        
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Origem</InputLabel>
          <Select
            value={filtroOrigem}
            label="Origem"
            onChange={(e) => setFiltroOrigem(e.target.value)}
          >
            <MenuItem value="TODOS">Todas</MenuItem>
            <MenuItem value="AUDITORIA_FOLHA">Auditoria de Folha</MenuItem>
            <MenuItem value="AUDITORIA_IA">Auditoria IA</MenuItem>
            <MenuItem value="MANUAL">Manual</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Lancamentos Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell padding="checkbox">
                <Checkbox
                  checked={lancamentosSelecionados.length === lancamentosFiltrados.length && lancamentosFiltrados.length > 0}
                  indeterminate={lancamentosSelecionados.length > 0 && lancamentosSelecionados.length < lancamentosFiltrados.length}
                  onChange={(e) => {
                    if (e.target.checked) {
                      setLancamentosSelecionados(lancamentosFiltrados.map(l => l.id));
                    } else {
                      setLancamentosSelecionados([]);
                    }
                  }}
                />
              </TableCell>
              <TableCell>Nº Lançamento</TableCell>
              <TableCell>Data</TableCell>
              <TableCell>Histórico</TableCell>
              <TableCell>Empresa</TableCell>
              <TableCell align="right">Valor</TableCell>
              <TableCell>Origem</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="center">Ações</TableCell>
              <TableCell></TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {lancamentosFiltrados.map((lancamento) => (
              <React.Fragment key={lancamento.id}>
                <TableRow hover>
                  <TableCell padding="checkbox">
                    <Checkbox
                      checked={lancamentosSelecionados.includes(lancamento.id)}
                      onChange={(e) => {
                        if (e.target.checked) {
                          setLancamentosSelecionados(prev => [...prev, lancamento.id]);
                        } else {
                          setLancamentosSelecionados(prev => prev.filter(id => id !== lancamento.id));
                        }
                      }}
                    />
                  </TableCell>
                  <TableCell>{lancamento.numero_lancamento}</TableCell>
                  <TableCell>
                    {new Date(lancamento.data_lancamento).toLocaleDateString('pt-BR')}
                  </TableCell>
                  <TableCell>
                    <Box sx={{ maxWidth: 200 }}>
                      <Typography variant="body2" noWrap>
                        {lancamento.historico}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{lancamento.empresa_nome}</TableCell>
                  <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                    R$ {lancamento.valor_total.toLocaleString('pt-BR', {
                      minimumFractionDigits: 2
                    })}
                  </TableCell>
                  <TableCell>
                    <Chip 
                      label={getOrigemLabel(lancamento.origem_lancamento)}
                      variant="outlined"
                      size="small"
                    />
                  </TableCell>
                  <TableCell>
                    <Chip
                      label={lancamento.status_lancamento}
                      color={getStatusColor(lancamento.status_lancamento) as any}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <Box display="flex" gap={1}>
                      {lancamento.status_lancamento === 'RASCUNHO' && (
                        <>
                          <Tooltip title="Aprovar">
                            <IconButton 
                              size="small" 
                              color="success"
                              onClick={() => handleAprovarLancamento(lancamento.id)}
                            >
                              <CheckCircle />
                            </IconButton>
                          </Tooltip>
                          <Tooltip title="Rejeitar">
                            <IconButton 
                              size="small" 
                              color="error"
                              onClick={() => handleRejeitarLancamento(lancamento.id)}
                            >
                              <Cancel />
                            </IconButton>
                          </Tooltip>
                        </>
                      )}
                      <Tooltip title="Ver Detalhes">
                        <IconButton 
                          size="small"
                          onClick={() => {
                            setLancamentoDetalhes(lancamento);
                            setDialogDetalhesAberto(true);
                          }}
                        >
                          <Visibility />
                        </IconButton>
                      </Tooltip>
                    </Box>
                  </TableCell>
                  <TableCell>
                    <IconButton 
                      size="small"
                      onClick={() => toggleRowExpanded(lancamento.id)}
                    >
                      {expandedRows.has(lancamento.id) ? <ExpandLess /> : <ExpandMore />}
                    </IconButton>
                  </TableCell>
                </TableRow>
                
                {/* Expanded Row - Débitos e Créditos */}
                <TableRow>
                  <TableCell style={{ paddingBottom: 0, paddingTop: 0 }} colSpan={10}>
                    <Collapse in={expandedRows.has(lancamento.id)} timeout="auto" unmountOnExit>
                      <Box sx={{ margin: 2 }}>
                        <Typography variant="h6" gutterBottom component="div">
                          Débitos e Créditos
                        </Typography>
                        <Table size="small">
                          <TableHead>
                            <TableRow>
                              <TableCell>Conta</TableCell>
                              <TableCell>Descrição</TableCell>
                              <TableCell align="center">Tipo</TableCell>
                              <TableCell align="right">Valor</TableCell>
                              <TableCell>Histórico</TableCell>
                            </TableRow>
                          </TableHead>
                          <TableBody>
                            {lancamento.itens.map((item) => (
                              <TableRow key={item.id}>
                                <TableCell sx={{ fontFamily: 'monospace' }}>
                                  {item.conta_codigo}
                                </TableCell>
                                <TableCell>{item.conta_nome}</TableCell>
                                <TableCell align="center">
                                  <Chip
                                    icon={item.tipo_movimentacao === 'DEBITO' ? <TrendingUp /> : <TrendingDown />}
                                    label={item.tipo_movimentacao}
                                    color={item.tipo_movimentacao === 'DEBITO' ? 'error' : 'success'}
                                    variant="outlined"
                                    size="small"
                                  />
                                </TableCell>
                                <TableCell align="right" sx={{ fontWeight: 'bold' }}>
                                  R$ {item.valor.toLocaleString('pt-BR', {
                                    minimumFractionDigits: 2
                                  })}
                                </TableCell>
                                <TableCell>{item.historico_item}</TableCell>
                              </TableRow>
                            ))}
                          </TableBody>
                        </Table>
                      </Box>
                    </Collapse>
                  </TableCell>
                </TableRow>
              </React.Fragment>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {/* Detalhes Dialog */}
      <Dialog
        open={dialogDetalhesAberto}
        onClose={() => setDialogDetalhesAberto(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Detalhes do Lançamento - {lancamentoDetalhes?.numero_lancamento}
        </DialogTitle>
        <DialogContent>
          {lancamentoDetalhes && (
            <Grid container spacing={2}>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Número do Lançamento"
                  value={lancamentoDetalhes.numero_lancamento}
                  InputProps={{ readOnly: true }}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Data do Lançamento"
                  value={new Date(lancamentoDetalhes.data_lancamento).toLocaleDateString('pt-BR')}
                  InputProps={{ readOnly: true }}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Histórico"
                  value={lancamentoDetalhes.historico}
                  InputProps={{ readOnly: true }}
                  margin="normal"
                  multiline
                  rows={2}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Valor Total"
                  value={`R$ ${lancamentoDetalhes.valor_total.toLocaleString('pt-BR', {
                    minimumFractionDigits: 2
                  })}`}
                  InputProps={{ readOnly: true }}
                  margin="normal"
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Status"
                  value={lancamentoDetalhes.status_lancamento}
                  InputProps={{ readOnly: true }}
                  margin="normal"
                />
              </Grid>
              {lancamentoDetalhes.aprovado_por && (
                <>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Aprovado Por"
                      value={lancamentoDetalhes.aprovado_por}
                      InputProps={{ readOnly: true }}
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      label="Data de Aprovação"
                      value={lancamentoDetalhes.aprovado_em ? 
                        new Date(lancamentoDetalhes.aprovado_em).toLocaleString('pt-BR') : ''
                      }
                      InputProps={{ readOnly: true }}
                      margin="normal"
                    />
                  </Grid>
                </>
              )}
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogDetalhesAberto(false)}>
            Fechar
          </Button>
          {lancamentoDetalhes?.status_lancamento === 'RASCUNHO' && (
            <>
              <Button 
                color="error"
                onClick={() => {
                  handleRejeitarLancamento(lancamentoDetalhes.id);
                  setDialogDetalhesAberto(false);
                }}
              >
                Rejeitar
              </Button>
              <Button 
                variant="contained"
                color="success"
                onClick={() => {
                  handleAprovarLancamento(lancamentoDetalhes.id);
                  setDialogDetalhesAberto(false);
                }}
              >
                Aprovar
              </Button>
            </>
          )}
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default LancamentosContabeisPage;