import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Grid,
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
  Paper,
  Chip,
  IconButton,
  Tooltip,
  Alert,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  LinearProgress,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Avatar,
  Divider,
  CircularProgress,
} from '@mui/material';
import {
  History,
  Restore,
  CompareArrows,
  PlayArrow,
  Science,
  CheckCircle,
  Error,
  Warning,
  Info,
  ExpandMore,
  FileCopy,
  Save,
  Preview,
  Timeline,
  Speed,
  Security,
  Assignment,
  BugReport,
  Schedule,
} from '@mui/icons-material';

interface ConfigurationVersion {
  id: number;
  version: number;
  name: string;
  description: string;
  createdAt: Date;
  createdBy: string;
  status: 'draft' | 'active' | 'archived';
  parentVersionId?: number;
  rollbackReason?: string;
  configurationData: any;
  changesSummary: string[];
  validationResults?: ValidationResult;
}

interface ValidationResult {
  isValid: boolean;
  errors: ValidationError[];
  warnings: ValidationWarning[];
  performance: {
    estimatedSendTime: string;
    successRate: number;
    costEstimate: string;
  };
}

interface ValidationError {
  field: string;
  message: string;
  severity: 'error' | 'warning' | 'info';
}

interface ValidationWarning {
  field: string;
  message: string;
  recommendation: string;
}

interface SimulationResult {
  id: string;
  sessionName: string;
  configurationData: any;
  results: {
    success: boolean;
    documentsProcessed: number;
    recipientsNotified: number;
    channelsUsed: string[];
    executionTime: number;
    errors: string[];
    warnings: string[];
  };
  performance: {
    successRate: number;
    avgProcessingTime: number;
    resourceUsage: number;
  };
  startedAt: Date;
  completedAt?: Date;
}

interface ConfigurationVersioningProps {
  clientId: number;
  configurationId: number;
}

const ConfigurationVersioning: React.FC<ConfigurationVersioningProps> = ({
  clientId,
  configurationId,
}) => {
  const [versions, setVersions] = useState<ConfigurationVersion[]>([]);
  const [selectedVersions, setSelectedVersions] = useState<number[]>([]);
  const [compareDialogOpen, setCompareDialogOpen] = useState(false);
  const [simulationDialogOpen, setSimulationDialogOpen] = useState(false);
  const [rollbackDialogOpen, setRollbackDialogOpen] = useState(false);
  const [simulationResults, setSimulationResults] = useState<SimulationResult[]>([]);
  const [isSimulating, setIsSimulating] = useState(false);
  const [simulationStep, setSimulationStep] = useState(0);
  const [rollbackReason, setRollbackReason] = useState('');

  // Mock data
  useEffect(() => {
    const mockVersions: ConfigurationVersion[] = [
      {
        id: 1,
        version: 1,
        name: 'Configuração Inicial',
        description: 'Primeira configuração para o cliente',
        createdAt: new Date('2024-01-15'),
        createdBy: 'Ana Silva',
        status: 'archived',
        configurationData: {
          documents: ['DARF', 'DAS'],
          channels: ['email'],
          recipients: ['contato@cliente.com'],
          schedule: 'monthly'
        },
        changesSummary: ['Configuração inicial criada'],
        validationResults: {
          isValid: true,
          errors: [],
          warnings: [],
          performance: {
            estimatedSendTime: '2-3 minutos',
            successRate: 0.85,
            costEstimate: 'R$ 0,15 por envio'
          }
        }
      },
      {
        id: 2,
        version: 2,
        name: 'Adição de WhatsApp',
        description: 'Inclusão do canal WhatsApp para backup',
        createdAt: new Date('2024-01-20'),
        createdBy: 'Carlos Lima',
        status: 'archived',
        parentVersionId: 1,
        configurationData: {
          documents: ['DARF', 'DAS'],
          channels: ['email', 'whatsapp'],
          recipients: ['contato@cliente.com', '+5511999999999'],
          schedule: 'monthly'
        },
        changesSummary: [
          'Adicionado canal WhatsApp',
          'Incluído número de telefone nos destinatários'
        ],
        validationResults: {
          isValid: true,
          errors: [],
          warnings: [
            {
              field: 'whatsapp',
              message: 'Número de WhatsApp não verificado',
              recommendation: 'Teste o envio antes de ativar em produção'
            }
          ],
          performance: {
            estimatedSendTime: '3-4 minutos',
            successRate: 0.92,
            costEstimate: 'R$ 0,25 por envio'
          }
        }
      },
      {
        id: 3,
        version: 3,
        name: 'Configuração Atual',
        description: 'Adição de documentos obrigatórios DEFIS',
        createdAt: new Date('2024-01-25'),
        createdBy: 'Ana Silva',
        status: 'active',
        parentVersionId: 2,
        configurationData: {
          documents: ['DARF', 'DAS', 'DEFIS'],
          channels: ['email', 'whatsapp'],
          recipients: ['contato@cliente.com', '+5511999999999'],
          schedule: 'monthly',
          automation: true
        },
        changesSummary: [
          'Adicionado documento DEFIS',
          'Ativada automação de envio',
          'Ajustado cronograma para compliance'
        ],
        validationResults: {
          isValid: true,
          errors: [],
          warnings: [],
          performance: {
            estimatedSendTime: '4-5 minutos',
            successRate: 0.95,
            costEstimate: 'R$ 0,30 por envio'
          }
        }
      },
    ];

    const mockSimulations: SimulationResult[] = [
      {
        id: 'sim-1',
        sessionName: 'Teste da versão 3',
        configurationData: mockVersions[2].configurationData,
        results: {
          success: true,
          documentsProcessed: 3,
          recipientsNotified: 2,
          channelsUsed: ['email', 'whatsapp'],
          executionTime: 245000, // ms
          errors: [],
          warnings: ['WhatsApp backup usado para 1 destinatário']
        },
        performance: {
          successRate: 0.95,
          avgProcessingTime: 4.1,
          resourceUsage: 0.75
        },
        startedAt: new Date('2024-01-25T10:30:00'),
        completedAt: new Date('2024-01-25T10:34:05'),
      }
    ];

    setVersions(mockVersions);
    setSimulationResults(mockSimulations);
  }, []);

  const handleVersionSelect = (versionId: number) => {
    setSelectedVersions(prev => {
      if (prev.includes(versionId)) {
        return prev.filter(id => id !== versionId);
      } else if (prev.length < 2) {
        return [...prev, versionId];
      } else {
        return [prev[1], versionId];
      }
    });
  };

  const handleCompareVersions = () => {
    if (selectedVersions.length === 2) {
      setCompareDialogOpen(true);
    }
  };

  const handleRollback = async (targetVersionId: number) => {
    const targetVersion = versions.find(v => v.id === targetVersionId);
    if (!targetVersion) return;

    // Create a new version based on the target version
    const newVersion: ConfigurationVersion = {
      id: Date.now(),
      version: Math.max(...versions.map(v => v.version)) + 1,
      name: `Rollback para v${targetVersion.version}`,
      description: `Rollback automático para versão ${targetVersion.version}`,
      createdAt: new Date(),
      createdBy: 'Sistema',
      status: 'active',
      parentVersionId: targetVersion.id,
      rollbackReason: rollbackReason,
      configurationData: { ...targetVersion.configurationData },
      changesSummary: [`Rollback para versão ${targetVersion.version}`, `Motivo: ${rollbackReason}`],
    };

    // Mark current active version as archived
    setVersions(prev => 
      prev.map(v => ({
        ...v,
        status: v.status === 'active' ? 'archived' as const : v.status
      })).concat(newVersion)
    );

    setRollbackDialogOpen(false);
    setRollbackReason('');
  };

  const runSimulation = async (versionId: number) => {
    const version = versions.find(v => v.id === versionId);
    if (!version) return;

    setIsSimulating(true);
    setSimulationStep(0);
    setSimulationDialogOpen(true);

    const steps = [
      'Validando configuração...',
      'Preparando documentos de teste...',
      'Simulando envio por email...',
      'Simulando envio por WhatsApp...',
      'Calculando métricas de performance...',
      'Gerando relatório final...'
    ];

    for (let i = 0; i < steps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 1500));
      setSimulationStep(i + 1);
    }

    // Generate simulation results
    const simulationResult: SimulationResult = {
      id: `sim-${Date.now()}`,
      sessionName: `Simulação da ${version.name}`,
      configurationData: version.configurationData,
      results: {
        success: true,
        documentsProcessed: version.configurationData.documents?.length || 0,
        recipientsNotified: version.configurationData.recipients?.length || 0,
        channelsUsed: version.configurationData.channels || [],
        executionTime: Math.random() * 300000 + 120000, // 2-7 minutes
        errors: [],
        warnings: Math.random() > 0.7 ? ['Simulação detectou potencial lentidão no envio'] : []
      },
      performance: {
        successRate: 0.9 + Math.random() * 0.1,
        avgProcessingTime: 3 + Math.random() * 3,
        resourceUsage: 0.5 + Math.random() * 0.4
      },
      startedAt: new Date(),
      completedAt: new Date()
    };

    setSimulationResults(prev => [simulationResult, ...prev]);
    setIsSimulating(false);
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'active':
        return 'success';
      case 'draft':
        return 'warning';
      case 'archived':
        return 'default';
      default:
        return 'default';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'active':
        return 'Ativa';
      case 'draft':
        return 'Rascunho';
      case 'archived':
        return 'Arquivada';
      default:
        return status;
    }
  };

  const renderVersionComparison = () => {
    if (selectedVersions.length !== 2) return null;

    const version1 = versions.find(v => v.id === selectedVersions[0]);
    const version2 = versions.find(v => v.id === selectedVersions[1]);

    if (!version1 || !version2) return null;

    return (
      <Grid container spacing={3}>
        <Grid item xs={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Versão {version1.version} - {version1.name}
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              {version1.description}
            </Typography>
            <pre style={{ fontSize: '0.8rem', overflow: 'auto' }}>
              {JSON.stringify(version1.configurationData, null, 2)}
            </pre>
          </Paper>
        </Grid>
        <Grid item xs={6}>
          <Paper sx={{ p: 2 }}>
            <Typography variant="h6" gutterBottom>
              Versão {version2.version} - {version2.name}
            </Typography>
            <Typography variant="body2" color="text.secondary" paragraph>
              {version2.description}
            </Typography>
            <pre style={{ fontSize: '0.8rem', overflow: 'auto' }}>
              {JSON.stringify(version2.configurationData, null, 2)}
            </pre>
          </Paper>
        </Grid>
      </Grid>
    );
  };

  const renderSimulationResults = (result: SimulationResult) => (
    <Accordion key={result.id}>
      <AccordionSummary expandIcon={<ExpandMore />}>
        <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
          <Typography variant="h6" sx={{ flexGrow: 1 }}>
            {result.sessionName}
          </Typography>
          <Chip
            label={result.results.success ? 'Sucesso' : 'Falha'}
            color={result.results.success ? 'success' : 'error'}
            size="small"
            sx={{ mr: 2 }}
          />
          <Typography variant="body2" color="text.secondary">
            {result.completedAt?.toLocaleString()}
          </Typography>
        </Box>
      </AccordionSummary>
      <AccordionDetails>
        <Grid container spacing={3}>
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2" gutterBottom>
              Resultados da Execução
            </Typography>
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <Assignment />
                </ListItemIcon>
                <ListItemText 
                  primary="Documentos Processados"
                  secondary={result.results.documentsProcessed}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Speed />
                </ListItemIcon>
                <ListItemText 
                  primary="Tempo de Execução"
                  secondary={`${(result.results.executionTime / 1000 / 60).toFixed(1)} minutos`}
                />
              </ListItem>
              <ListItem>
                <ListItemIcon>
                  <Timeline />
                </ListItemIcon>
                <ListItemText 
                  primary="Canais Utilizados"
                  secondary={result.results.channelsUsed.join(', ')}
                />
              </ListItem>
            </List>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2" gutterBottom>
              Métricas de Performance
            </Typography>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2">
                Taxa de Sucesso: {(result.performance.successRate * 100).toFixed(1)}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={result.performance.successRate * 100}
                color="success"
                sx={{ mt: 0.5 }}
              />
            </Box>
            <Box sx={{ mb: 2 }}>
              <Typography variant="body2">
                Tempo Médio: {result.performance.avgProcessingTime.toFixed(1)}min
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={(result.performance.avgProcessingTime / 10) * 100}
                color="info"
                sx={{ mt: 0.5 }}
              />
            </Box>
            <Box>
              <Typography variant="body2">
                Uso de Recursos: {(result.performance.resourceUsage * 100).toFixed(0)}%
              </Typography>
              <LinearProgress 
                variant="determinate" 
                value={result.performance.resourceUsage * 100}
                color={result.performance.resourceUsage > 0.8 ? 'warning' : 'primary'}
                sx={{ mt: 0.5 }}
              />
            </Box>
          </Grid>
          
          <Grid item xs={12} md={4}>
            <Typography variant="subtitle2" gutterBottom>
              Alertas e Observações
            </Typography>
            {result.results.errors.length > 0 && (
              <Alert severity="error" sx={{ mb: 1 }}>
                {result.results.errors.join(', ')}
              </Alert>
            )}
            {result.results.warnings.length > 0 && (
              <Alert severity="warning" sx={{ mb: 1 }}>
                {result.results.warnings.join(', ')}
              </Alert>
            )}
            {result.results.errors.length === 0 && result.results.warnings.length === 0 && (
              <Alert severity="success">
                Simulação executada sem problemas
              </Alert>
            )}
          </Grid>
        </Grid>
      </AccordionDetails>
    </Accordion>
  );

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <History sx={{ mr: 2, color: 'primary.main' }} />
          Versionamento e Simulação
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Gerencie versões da configuração e teste mudanças em modo simulação
        </Typography>
      </Box>

      {/* Version Actions */}
      <Box sx={{ mb: 3, display: 'flex', gap: 2, flexWrap: 'wrap' }}>
        <Button
          variant="outlined"
          startIcon={<CompareArrows />}
          onClick={handleCompareVersions}
          disabled={selectedVersions.length !== 2}
        >
          Comparar Versões ({selectedVersions.length}/2)
        </Button>
        <Button
          variant="outlined"
          startIcon={<FileCopy />}
        >
          Criar Nova Versão
        </Button>
        <Button
          variant="outlined"
          startIcon={<Save />}
        >
          Salvar Como Template
        </Button>
      </Box>

      {/* Versions Table */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Histórico de Versões
          </Typography>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell padding="checkbox"></TableCell>
                  <TableCell>Versão</TableCell>
                  <TableCell>Nome</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Criado por</TableCell>
                  <TableCell>Data</TableCell>
                  <TableCell>Principais Mudanças</TableCell>
                  <TableCell align="center">Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {versions.map((version) => (
                  <TableRow 
                    key={version.id}
                    selected={selectedVersions.includes(version.id)}
                    onClick={() => handleVersionSelect(version.id)}
                    sx={{ cursor: 'pointer' }}
                  >
                    <TableCell padding="checkbox">
                      <input
                        type="checkbox"
                        checked={selectedVersions.includes(version.id)}
                        onChange={() => handleVersionSelect(version.id)}
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="h6">v{version.version}</Typography>
                    </TableCell>
                    <TableCell>
                      <Typography variant="subtitle2">{version.name}</Typography>
                      <Typography variant="body2" color="text.secondary">
                        {version.description}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={getStatusLabel(version.status)}
                        color={getStatusColor(version.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{version.createdBy}</TableCell>
                    <TableCell>{version.createdAt.toLocaleDateString()}</TableCell>
                    <TableCell>
                      <Box sx={{ maxWidth: 200 }}>
                        {version.changesSummary.slice(0, 2).map((change, index) => (
                          <Typography key={index} variant="body2" component="div">
                            • {change}
                          </Typography>
                        ))}
                        {version.changesSummary.length > 2 && (
                          <Typography variant="body2" color="text.secondary">
                            +{version.changesSummary.length - 2} mais...
                          </Typography>
                        )}
                      </Box>
                    </TableCell>
                    <TableCell align="center">
                      <Tooltip title="Simular configuração">
                        <IconButton 
                          onClick={(e) => {
                            e.stopPropagation();
                            runSimulation(version.id);
                          }}
                        >
                          <Science />
                        </IconButton>
                      </Tooltip>
                      {version.status !== 'active' && (
                        <Tooltip title="Restaurar versão">
                          <IconButton 
                            onClick={(e) => {
                              e.stopPropagation();
                              setRollbackDialogOpen(true);
                            }}
                          >
                            <Restore />
                          </IconButton>
                        </Tooltip>
                      )}
                      <Tooltip title="Visualizar detalhes">
                        <IconButton>
                          <Preview />
                        </IconButton>
                      </Tooltip>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Simulation Results */}
      {simulationResults.length > 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
              <Science sx={{ mr: 1 }} />
              Resultados de Simulação
            </Typography>
            {simulationResults.map(renderSimulationResults)}
          </CardContent>
        </Card>
      )}

      {/* Compare Versions Dialog */}
      <Dialog
        open={compareDialogOpen}
        onClose={() => setCompareDialogOpen(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          Comparação de Versões
        </DialogTitle>
        <DialogContent>
          {renderVersionComparison()}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCompareDialogOpen(false)}>
            Fechar
          </Button>
        </DialogActions>
      </Dialog>

      {/* Simulation Dialog */}
      <Dialog
        open={simulationDialogOpen}
        onClose={!isSimulating ? () => setSimulationDialogOpen(false) : undefined}
        maxWidth="md"
        fullWidth
        disableEscapeKeyDown={isSimulating}
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Science sx={{ mr: 2, color: 'primary.main' }} />
            Simulação em Andamento
          </Box>
        </DialogTitle>
        <DialogContent>
          {isSimulating ? (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                Executando simulação da configuração em ambiente seguro...
              </Alert>
              
              <Stepper activeStep={simulationStep} orientation="vertical">
                {[
                  'Validando configuração',
                  'Preparando documentos de teste',
                  'Simulando envio por email',
                  'Simulando envio por WhatsApp',
                  'Calculando métricas de performance',
                  'Gerando relatório final'
                ].map((label, index) => (
                  <Step key={index}>
                    <StepLabel>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        {simulationStep > index && <CheckCircle color="success" sx={{ mr: 1 }} />}
                        {simulationStep === index && <CircularProgress size={20} sx={{ mr: 1 }} />}
                        {label}
                      </Box>
                    </StepLabel>
                  </Step>
                ))}
              </Stepper>
            </Box>
          ) : (
            <Alert severity="success">
              Simulação concluída com sucesso! Verifique os resultados na seção "Resultados de Simulação".
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => setSimulationDialogOpen(false)}
            disabled={isSimulating}
          >
            {isSimulating ? 'Executando...' : 'Fechar'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Rollback Dialog */}
      <Dialog
        open={rollbackDialogOpen}
        onClose={() => setRollbackDialogOpen(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle>
          Confirmar Rollback
        </DialogTitle>
        <DialogContent>
          <Alert severity="warning" sx={{ mb: 3 }}>
            Esta ação irá criar uma nova versão baseada na versão selecionada e marcará a versão atual como arquivada.
          </Alert>
          
          <TextField
            fullWidth
            label="Motivo do rollback"
            multiline
            rows={3}
            value={rollbackReason}
            onChange={(e) => setRollbackReason(e.target.value)}
            placeholder="Descreva o motivo do rollback..."
            required
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRollbackDialogOpen(false)}>
            Cancelar
          </Button>
          <Button 
            variant="contained"
            color="warning"
            onClick={() => selectedVersions[0] && handleRollback(selectedVersions[0])}
            disabled={!rollbackReason.trim()}
          >
            Confirmar Rollback
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ConfigurationVersioning;