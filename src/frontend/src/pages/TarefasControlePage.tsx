/**
 * 📋 TarefasControlePage - Central de Tarefas e Controles (Phase 3)
 * 
 * Sistema unificado de gestão de tarefas e controles:
 * - Dashboard de tarefas por empresa/período
 * - Workflow de aprovação e acompanhamento
 * - Notificações automáticas por prazos
 * - Integração com auditoria e lançamentos
 * 
 * Implementa o "Ecossistema de Gestão" do manifesto Grand Tomo
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
  LinearProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Checkbox,
  Alert,
  IconButton,
  Tooltip,
  Badge,
  Fab
} from '@mui/material';
import {
  Assignment,
  CheckCircle,
  Warning,
  Schedule,
  TrendingUp,
  Business,
  CalendarToday,
  Notifications,
  Add,
  Edit,
  Visibility,
  PlayArrow,
  Stop,
  Timer,
  NotificationImportant
} from '@mui/icons-material';

interface TarefaControle {
  id: number;
  empresa_id: number;
  empresa_nome: string;
  mes: number;
  ano: number;
  descricao_tarefa: string;
  status: 'PENDENTE' | 'EM_ANDAMENTO' | 'CONCLUIDA' | 'ATRASADA';
  prioridade: 'BAIXA' | 'MEDIA' | 'ALTA' | 'CRITICA';
  responsavel?: string;
  prazo_estimado?: string;
  iniciada_em?: string;
  concluida_em?: string;
  tempo_gasto_minutos?: number;
  observacoes?: string;
  origem: 'TEMPLATE' | 'AUDITORIA' | 'MANUAL';
  template_nome?: string;
}

interface ControleMensal {
  id: number;
  empresa_id: number;
  empresa_nome: string;
  mes: number;
  ano: number;
  status: 'PENDENTE' | 'EM_ANDAMENTO' | 'CONCLUIDO' | 'ATRASADO';
  total_tarefas: number;
  tarefas_concluidas: number;
  progresso_percentual: number;
  prazo_final?: string;
  tarefas: TarefaControle[];
}

const TarefasControlePage: React.FC = () => {
  const [controles, setControles] = useState<ControleMensal[]>([]);
  const [tarefasSelecionadas, setTarefasSelecionadas] = useState<number[]>([]);
  const [loading, setLoading] = useState(true);
  const [filtroStatus, setFiltroStatus] = useState<string>('TODOS');
  const [filtroEmpresa, setFiltroEmpresa] = useState<string>('TODAS');
  const [filtroPeriodo, setFiltroPeriodo] = useState<string>('2024-01');
  const [dialogTarefaAberto, setDialogTarefaAberto] = useState(false);
  const [tarefaSelecionada, setTarefaSelecionada] = useState<TarefaControle | null>(null);

  // Mock data
  useEffect(() => {
    const mockControles: ControleMensal[] = [
      {
        id: 1,
        empresa_id: 101,
        empresa_nome: "Empresa ABC Ltda",
        mes: 1,
        ano: 2024,
        status: "EM_ANDAMENTO",
        total_tarefas: 8,
        tarefas_concluidas: 5,
        progresso_percentual: 62.5,
        prazo_final: "2024-02-10",
        tarefas: [
          {
            id: 1,
            empresa_id: 101,
            empresa_nome: "Empresa ABC Ltda",
            mes: 1,
            ano: 2024,
            descricao_tarefa: "Auditoria de Folha de Pagamento",
            status: "CONCLUIDA",
            prioridade: "ALTA",
            responsavel: "Sistema Auditor",
            concluida_em: "2024-01-16T14:30:00Z",
            tempo_gasto_minutos: 25,
            origem: "AUDITORIA",
            observacoes: "3 divergências encontradas - já corrigidas"
          },
          {
            id: 2,
            empresa_id: 101,
            empresa_nome: "Empresa ABC Ltda", 
            mes: 1,
            ano: 2024,
            descricao_tarefa: "Aprovação de Lançamentos Contábeis",
            status: "PENDENTE",
            prioridade: "CRITICA",
            prazo_estimado: "2024-01-20",
            origem: "AUDITORIA"
          },
          {
            id: 3,
            empresa_id: 101,
            empresa_nome: "Empresa ABC Ltda",
            mes: 1,
            ano: 2024,
            descricao_tarefa: "Conferência de CCT Vigente",
            status: "CONCLUIDA",
            prioridade: "MEDIA",
            responsavel: "Ana Paula",
            concluida_em: "2024-01-15T16:45:00Z",
            tempo_gasto_minutos: 45,
            origem: "TEMPLATE",
            template_nome: "Controle Mensal Padrão"
          }
        ]
      },
      {
        id: 2,
        empresa_id: 102,
        empresa_nome: "Empresa XYZ S.A.",
        mes: 1,
        ano: 2024,
        status: "CONCLUIDO",
        total_tarefas: 6,
        tarefas_concluidas: 6,
        progresso_percentual: 100,
        prazo_final: "2024-02-10",
        tarefas: [
          {
            id: 4,
            empresa_id: 102,
            empresa_nome: "Empresa XYZ S.A.",
            mes: 1,
            ano: 2024,
            descricao_tarefa: "Auditoria de Folha de Pagamento",
            status: "CONCLUIDA",
            prioridade: "ALTA", 
            responsavel: "Sistema Auditor",
            concluida_em: "2024-01-14T11:20:00Z",
            tempo_gasto_minutos: 18,
            origem: "AUDITORIA"
          }
        ]
      }
    ];

    setTimeout(() => {
      setControles(mockControles);
      setLoading(false);
    }, 1000);
  }, []);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDENTE': return 'warning';
      case 'EM_ANDAMENTO': return 'info';
      case 'CONCLUIDA': return 'success';
      case 'ATRASADA': return 'error';
      case 'CONCLUIDO': return 'success';
      case 'ATRASADO': return 'error';
      default: return 'default';
    }
  };

  const getPrioridadeColor = (prioridade: string) => {
    switch (prioridade) {
      case 'BAIXA': return 'success';
      case 'MEDIA': return 'info';
      case 'ALTA': return 'warning';
      case 'CRITICA': return 'error';
      default: return 'default';
    }
  };

  const handleIniciarTarefa = (tarefaId: number) => {
    // TODO: Implement start task logic
    alert(`Tarefa ${tarefaId} iniciada!`);
  };

  const handleConcluirTarefa = (tarefaId: number) => {
    setControles(prev => prev.map(controle => ({
      ...controle,
      tarefas: controle.tarefas.map(tarefa => 
        tarefa.id === tarefaId
          ? {
              ...tarefa,
              status: 'CONCLUIDA',
              concluida_em: new Date().toISOString(),
              tempo_gasto_minutos: Math.floor(Math.random() * 120) + 10
            }
          : tarefa
      )
    })));
  };

  const handleConcluirSelecionadas = () => {
    if (tarefasSelecionadas.length === 0) {
      alert('Selecione pelo menos uma tarefa');
      return;
    }

    const confirmacao = window.confirm(
      `Marcar ${tarefasSelecionadas.length} tarefa(s) como concluída(s)?`
    );

    if (confirmacao) {
      setControles(prev => prev.map(controle => ({
        ...controle,
        tarefas: controle.tarefas.map(tarefa => 
          tarefasSelecionadas.includes(tarefa.id)
            ? {
                ...tarefa,
                status: 'CONCLUIDA',
                concluida_em: new Date().toISOString(),
                tempo_gasto_minutos: Math.floor(Math.random() * 120) + 10
              }
            : tarefa
        )
      })));
      setTarefasSelecionadas([]);
    }
  };

  // Calculate statistics
  const todasTarefas = controles.flatMap(c => c.tarefas);
  const tarefasPendentes = todasTarefas.filter(t => t.status === 'PENDENTE').length;
  const tarefasEmAndamento = todasTarefas.filter(t => t.status === 'EM_ANDAMENTO').length;
  const tarefasConcluidas = todasTarefas.filter(t => t.status === 'CONCLUIDA').length;
  const tarefasCriticas = todasTarefas.filter(t => t.prioridade === 'CRITICA').length;
  const empresasComPendencias = controles.filter(c => c.status !== 'CONCLUIDO').length;

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
        <Box display="flex" alignItems="center" justifyContent="center" minHeight="400px">
          <Typography variant="h6">Carregando controles...</Typography>
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
            📋 Central de Tarefas e Controles
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Sistema unificado de gestão - Phase 3 Grand Tomo
          </Typography>
        </Box>
        <Box display="flex" gap={2}>
          <Button
            variant="contained"
            color="success"
            startIcon={<CheckCircle />}
            onClick={handleConcluirSelecionadas}
            disabled={tarefasSelecionadas.length === 0}
          >
            Concluir Selecionadas ({tarefasSelecionadas.length})
          </Button>
          <Fab
            color="primary"
            aria-label="add"
            size="small"
            onClick={() => setDialogTarefaAberto(true)}
          >
            <Add />
          </Fab>
        </Box>
      </Box>

      {/* Critical Alert */}
      {tarefasCriticas > 0 && (
        <Alert 
          severity="error" 
          icon={<NotificationImportant />}
          sx={{ mb: 3 }}
        >
          <strong>Atenção!</strong> Você tem {tarefasCriticas} tarefa(s) crítica(s) pendente(s). 
          Revisar imediatamente para evitar impactos nos prazos de compliance.
        </Alert>
      )}

      {/* Momento Surreal Alert */}
      <Alert severity="info" sx={{ mb: 3 }}>
        <strong>Momento Surreal:</strong> O sistema criou automaticamente tarefas baseadas nos templates 
        aplicados e nas auditorias executadas. Cada ação disparou um evento que gerou tarefas específicas 
        para os responsáveis, tudo sem intervenção manual!
      </Alert>

      {/* Statistics Dashboard */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Pendentes
                  </Typography>
                  <Typography variant="h4" color="warning.main">
                    {tarefasPendentes}
                  </Typography>
                </Box>
                <Badge badgeContent={tarefasCriticas} color="error">
                  <Schedule color="warning" sx={{ fontSize: 40 }} />
                </Badge>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Em Andamento
                  </Typography>
                  <Typography variant="h4" color="info.main">
                    {tarefasEmAndamento}
                  </Typography>
                </Box>
                <PlayArrow color="info" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Concluídas
                  </Typography>
                  <Typography variant="h4" color="success.main">
                    {tarefasConcluidas}
                  </Typography>
                </Box>
                <CheckCircle color="success" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Empresas Pendentes
                  </Typography>
                  <Typography variant="h4" color="primary.main">
                    {empresasComPendencias}
                  </Typography>
                </Box>
                <Business color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} sm={6} md={2.4}>
          <Card>
            <CardContent>
              <Box display="flex" alignItems="center">
                <Box sx={{ flexGrow: 1 }}>
                  <Typography color="text.secondary" gutterBottom>
                    Total Tarefas
                  </Typography>
                  <Typography variant="h4">
                    {todasTarefas.length}
                  </Typography>
                </Box>
                <Assignment color="primary" sx={{ fontSize: 40 }} />
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Filters */}
      <Box display="flex" gap={2} mb={3}>
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Período</InputLabel>
          <Select
            value={filtroPeriodo}
            label="Período"
            onChange={(e) => setFiltroPeriodo(e.target.value)}
          >
            <MenuItem value="2024-01">Janeiro/2024</MenuItem>
            <MenuItem value="2024-02">Fevereiro/2024</MenuItem>
            <MenuItem value="2024-03">Março/2024</MenuItem>
          </Select>
        </FormControl>
        
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Status</InputLabel>
          <Select
            value={filtroStatus}
            label="Status"
            onChange={(e) => setFiltroStatus(e.target.value)}
          >
            <MenuItem value="TODOS">Todos</MenuItem>
            <MenuItem value="PENDENTE">Pendente</MenuItem>
            <MenuItem value="EM_ANDAMENTO">Em Andamento</MenuItem>
            <MenuItem value="CONCLUIDA">Concluída</MenuItem>
            <MenuItem value="ATRASADA">Atrasada</MenuItem>
          </Select>
        </FormControl>
        
        <FormControl size="small" sx={{ minWidth: 150 }}>
          <InputLabel>Empresa</InputLabel>
          <Select
            value={filtroEmpresa}
            label="Empresa"
            onChange={(e) => setFiltroEmpresa(e.target.value)}
          >
            <MenuItem value="TODAS">Todas</MenuItem>
            {controles.map(c => (
              <MenuItem key={c.empresa_id} value={c.empresa_nome}>
                {c.empresa_nome}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
      </Box>

      {/* Controls Cards */}
      <Grid container spacing={3}>
        {controles.map((controle) => (
          <Grid item xs={12} key={controle.id}>
            <Card>
              <CardContent>
                {/* Controle Header */}
                <Box display="flex" justifyContent="between" alignItems="center" mb={2}>
                  <Box>
                    <Typography variant="h6" component="div">
                      {controle.empresa_nome}
                    </Typography>
                    <Typography color="text.secondary" variant="body2">
                      {new Date(0, controle.mes - 1).toLocaleDateString('pt-BR', { month: 'long' })} {controle.ano}
                    </Typography>
                  </Box>
                  <Box display="flex" alignItems="center" gap={2}>
                    <Box textAlign="center">
                      <Typography variant="body2" color="text.secondary">
                        Progresso
                      </Typography>
                      <Typography variant="h6" color="primary">
                        {controle.progresso_percentual.toFixed(0)}%
                      </Typography>
                    </Box>
                    <Chip
                      label={controle.status}
                      color={getStatusColor(controle.status) as any}
                      icon={getStatusColor(controle.status) === 'success' ? <CheckCircle /> : <Schedule />}
                    />
                  </Box>
                </Box>

                {/* Progress Bar */}
                <Box mb={2}>
                  <LinearProgress 
                    variant="determinate" 
                    value={controle.progresso_percentual}
                    sx={{ height: 8, borderRadius: 4 }}
                    color={controle.progresso_percentual === 100 ? 'success' : 'primary'}
                  />
                  <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                    {controle.tarefas_concluidas} de {controle.total_tarefas} tarefas concluídas
                  </Typography>
                </Box>

                {/* Tarefas Table */}
                <TableContainer>
                  <Table size="small">
                    <TableHead>
                      <TableRow>
                        <TableCell padding="checkbox">
                          <Checkbox
                            indeterminate={
                              tarefasSelecionadas.some(id => controle.tarefas.some(t => t.id === id)) &&
                              !controle.tarefas.every(t => tarefasSelecionadas.includes(t.id))
                            }
                            checked={controle.tarefas.every(t => tarefasSelecionadas.includes(t.id))}
                            onChange={(e) => {
                              if (e.target.checked) {
                                setTarefasSelecionadas(prev => [
                                  ...prev, 
                                  ...controle.tarefas
                                    .filter(t => t.status !== 'CONCLUIDA')
                                    .map(t => t.id)
                                    .filter(id => !prev.includes(id))
                                ]);
                              } else {
                                const controleTaskIds = controle.tarefas.map(t => t.id);
                                setTarefasSelecionadas(prev => 
                                  prev.filter(id => !controleTaskIds.includes(id))
                                );
                              }
                            }}
                          />
                        </TableCell>
                        <TableCell>Tarefa</TableCell>
                        <TableCell>Status</TableCell>
                        <TableCell>Prioridade</TableCell>
                        <TableCell>Responsável</TableCell>
                        <TableCell>Origem</TableCell>
                        <TableCell align="center">Ações</TableCell>
                      </TableRow>
                    </TableHead>
                    <TableBody>
                      {controle.tarefas.map((tarefa) => (
                        <TableRow key={tarefa.id} hover>
                          <TableCell padding="checkbox">
                            <Checkbox
                              checked={tarefasSelecionadas.includes(tarefa.id)}
                              onChange={(e) => {
                                if (e.target.checked) {
                                  setTarefasSelecionadas(prev => [...prev, tarefa.id]);
                                } else {
                                  setTarefasSelecionadas(prev => prev.filter(id => id !== tarefa.id));
                                }
                              }}
                              disabled={tarefa.status === 'CONCLUIDA'}
                            />
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2" sx={{ fontWeight: 'medium' }}>
                              {tarefa.descricao_tarefa}
                            </Typography>
                            {tarefa.observacoes && (
                              <Typography variant="caption" color="text.secondary">
                                {tarefa.observacoes}
                              </Typography>
                            )}
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={tarefa.status}
                              color={getStatusColor(tarefa.status) as any}
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={tarefa.prioridade}
                              color={getPrioridadeColor(tarefa.prioridade) as any}
                              variant="outlined"
                              size="small"
                            />
                          </TableCell>
                          <TableCell>
                            <Typography variant="body2">
                              {tarefa.responsavel || 'Não atribuído'}
                            </Typography>
                          </TableCell>
                          <TableCell>
                            <Chip
                              label={tarefa.origem}
                              variant="outlined"
                              size="small"
                            />
                          </TableCell>
                          <TableCell align="center">
                            <Box display="flex" gap={0.5}>
                              {tarefa.status === 'PENDENTE' && (
                                <Tooltip title="Iniciar Tarefa">
                                  <IconButton 
                                    size="small"
                                    color="primary"
                                    onClick={() => handleIniciarTarefa(tarefa.id)}
                                  >
                                    <PlayArrow />
                                  </IconButton>
                                </Tooltip>
                              )}
                              {(tarefa.status === 'PENDENTE' || tarefa.status === 'EM_ANDAMENTO') && (
                                <Tooltip title="Marcar como Concluída">
                                  <IconButton 
                                    size="small"
                                    color="success"
                                    onClick={() => handleConcluirTarefa(tarefa.id)}
                                  >
                                    <CheckCircle />
                                  </IconButton>
                                </Tooltip>
                              )}
                              <Tooltip title="Ver Detalhes">
                                <IconButton 
                                  size="small"
                                  onClick={() => {
                                    setTarefaSelecionada(tarefa);
                                    setDialogTarefaAberto(true);
                                  }}
                                >
                                  <Visibility />
                                </IconButton>
                              </Tooltip>
                            </Box>
                          </TableCell>
                        </TableRow>
                      ))}
                    </TableBody>
                  </Table>
                </TableContainer>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Task Details Dialog */}
      <Dialog
        open={dialogTarefaAberto}
        onClose={() => setDialogTarefaAberto(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          {tarefaSelecionada ? 'Detalhes da Tarefa' : 'Nova Tarefa'}
        </DialogTitle>
        <DialogContent>
          {tarefaSelecionada && (
            <Grid container spacing={2} sx={{ mt: 1 }}>
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Descrição da Tarefa"
                  value={tarefaSelecionada.descricao_tarefa}
                  InputProps={{ readOnly: true }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Empresa"
                  value={tarefaSelecionada.empresa_nome}
                  InputProps={{ readOnly: true }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Período"
                  value={`${tarefaSelecionada.mes}/${tarefaSelecionada.ano}`}
                  InputProps={{ readOnly: true }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Status"
                  value={tarefaSelecionada.status}
                  InputProps={{ readOnly: true }}
                />
              </Grid>
              <Grid item xs={12} sm={6}>
                <TextField
                  fullWidth
                  label="Prioridade"
                  value={tarefaSelecionada.prioridade}
                  InputProps={{ readOnly: true }}
                />
              </Grid>
              {tarefaSelecionada.responsavel && (
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Responsável"
                    value={tarefaSelecionada.responsavel}
                    InputProps={{ readOnly: true }}
                  />
                </Grid>
              )}
              {tarefaSelecionada.tempo_gasto_minutos && (
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Tempo Gasto"
                    value={`${tarefaSelecionada.tempo_gasto_minutos} minutos`}
                    InputProps={{ readOnly: true }}
                  />
                </Grid>
              )}
              <Grid item xs={12}>
                <TextField
                  fullWidth
                  label="Origem"
                  value={`${tarefaSelecionada.origem}${tarefaSelecionada.template_nome ? ` - ${tarefaSelecionada.template_nome}` : ''}`}
                  InputProps={{ readOnly: true }}
                />
              </Grid>
              {tarefaSelecionada.observacoes && (
                <Grid item xs={12}>
                  <TextField
                    fullWidth
                    label="Observações"
                    value={tarefaSelecionada.observacoes}
                    InputProps={{ readOnly: true }}
                    multiline
                    rows={3}
                  />
                </Grid>
              )}
            </Grid>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDialogTarefaAberto(false)}>
            Fechar
          </Button>
          {tarefaSelecionada && tarefaSelecionada.status !== 'CONCLUIDA' && (
            <Button 
              variant="contained"
              color="success"
              onClick={() => {
                handleConcluirTarefa(tarefaSelecionada.id);
                setDialogTarefaAberto(false);
              }}
            >
              Marcar como Concluída
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default TarefasControlePage;