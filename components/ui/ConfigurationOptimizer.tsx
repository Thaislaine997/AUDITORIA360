import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  LinearProgress,
  Avatar,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  CircularProgress,
  Grid,
  Divider,
  Paper,
} from '@mui/material';
import {
  AutoAwesome,
  TrendingUp,
  CheckCircle,
  Warning,
  Info,
  ErrorOutline,
  ExpandMore,
  Lightbulb,
  Speed,
  Security,
  AttachMoney,
  Timeline,
  PlayArrow,
  Science,
} from '@mui/icons-material';

interface AIOptimization {
  id: string;
  type: 'configuration' | 'document' | 'channel' | 'automation' | 'compliance';
  title: string;
  description: string;
  confidence: number;
  expectedBenefit: string;
  implementationEffort: 'baixo' | 'médio' | 'alto';
  priority: 'baixa' | 'média' | 'alta' | 'crítica';
  impactMetrics: {
    successRate?: number;
    timeReduction?: number;
    costSaving?: number;
    complianceImprovement?: number;
  };
  implementation: {
    steps: string[];
    estimatedTime: string;
    requirements: string[];
  };
  baseAnalysis: {
    currentState: string;
    suggestedState: string;
    similarClientsUsage: number;
  };
}

interface ConfigurationOptimizerProps {
  clientId?: number;
  configurationId?: number;
  onOptimizationApplied?: (optimization: AIOptimization) => void;
}

const ConfigurationOptimizer: React.FC<ConfigurationOptimizerProps> = ({
  clientId,
  configurationId,
  onOptimizationApplied,
}) => {
  const [optimizations, setOptimizations] = useState<AIOptimization[]>([]);
  const [selectedOptimization, setSelectedOptimization] = useState<AIOptimization | null>(null);
  const [previewDialogOpen, setPreviewDialogOpen] = useState(false);
  const [implementationDialogOpen, setImplementationDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [analyzing, setAnalyzing] = useState(false);
  const [activeStep, setActiveStep] = useState(0);

  // Mock optimizations - in reality, these would come from AI analysis
  const mockOptimizations: AIOptimization[] = [
    {
      id: 'opt-1',
      type: 'document',
      title: 'Adicionar DEFIS ao envio',
      description: '92% das empresas do Simples Nacional neste porte também enviam o documento DEFIS.',
      confidence: 0.92,
      expectedBenefit: 'Compliance obrigatória para faturamento > R$1M',
      implementationEffort: 'baixo',
      priority: 'alta',
      impactMetrics: {
        complianceImprovement: 15,
        successRate: 2
      },
      implementation: {
        steps: [
          'Verificar regime tributário do cliente',
          'Adicionar DEFIS à lista de documentos',
          'Configurar periodicidade anual',
          'Testar envio em modo simulação'
        ],
        estimatedTime: '5 minutos',
        requirements: ['Cliente no Simples Nacional', 'Faturamento > R$1M']
      },
      baseAnalysis: {
        currentState: 'Sem envio de DEFIS configurado',
        suggestedState: 'DEFIS configurado para envio anual',
        similarClientsUsage: 92
      }
    },
    {
      id: 'opt-2',
      type: 'channel',
      title: 'Adicionar WhatsApp como canal secundário',
      description: 'Clientes com WhatsApp backup têm 15% menos falhas de entrega.',
      confidence: 0.87,
      expectedBenefit: 'Redução de falhas de entrega e melhor comunicação',
      implementationEffort: 'baixo',
      priority: 'média',
      impactMetrics: {
        successRate: 15,
        timeReduction: 8
      },
      implementation: {
        steps: [
          'Configurar número de WhatsApp do cliente',
          'Adicionar WhatsApp como canal secundário',
          'Configurar templates de mensagem',
          'Testar envio de teste'
        ],
        estimatedTime: '10 minutos',
        requirements: ['Número de WhatsApp válido', 'Consentimento do cliente']
      },
      baseAnalysis: {
        currentState: 'Apenas email configurado',
        suggestedState: 'Email principal + WhatsApp backup',
        similarClientsUsage: 73
      }
    },
    {
      id: 'opt-3',
      type: 'automation',
      title: 'Automatizar envio de GFIP',
      description: 'Baseado no perfil da empresa, o GFIP pode ser enviado automaticamente.',
      confidence: 0.85,
      expectedBenefit: 'Economia de tempo e redução de esquecimentos',
      implementationEffort: 'médio',
      priority: 'média',
      impactMetrics: {
        timeReduction: 25,
        successRate: 5
      },
      implementation: {
        steps: [
          'Analisar cronograma de obrigações',
          'Configurar regra de automação',
          'Definir destinatários para GFIP',
          'Agendar primeiro envio automático'
        ],
        estimatedTime: '15 minutos',
        requirements: ['Cronograma definido', 'Templates configurados']
      },
      baseAnalysis: {
        currentState: 'Envio manual do GFIP',
        suggestedState: 'Envio automático agendado',
        similarClientsUsage: 68
      }
    },
    {
      id: 'opt-4',
      type: 'compliance',
      title: 'Implementar verificação de LGPD',
      description: 'Adicionar controles de consentimento e rastreabilidade para compliance LGPD.',
      confidence: 0.95,
      expectedBenefit: 'Compliance total com LGPD e redução de riscos',
      implementationEffort: 'alto',
      priority: 'crítica',
      impactMetrics: {
        complianceImprovement: 40,
        successRate: 3
      },
      implementation: {
        steps: [
          'Configurar coleta de consentimento',
          'Implementar logs de auditoria',
          'Configurar direitos do titular',
          'Treinar equipe sobre LGPD'
        ],
        estimatedTime: '45 minutos',
        requirements: ['Política de privacidade', 'Termos de consentimento']
      },
      baseAnalysis: {
        currentState: 'Controles básicos de LGPD',
        suggestedState: 'Compliance completa LGPD',
        similarClientsUsage: 45
      }
    },
    {
      id: 'opt-5',
      type: 'configuration',
      title: 'Otimizar horários de envio',
      description: 'Análise mostra que envios às 14h têm 12% mais taxa de abertura.',
      confidence: 0.78,
      expectedBenefit: 'Maior engajamento e taxa de leitura',
      implementationEffort: 'baixo',
      priority: 'baixa',
      impactMetrics: {
        successRate: 12,
        timeReduction: 0
      },
      implementation: {
        steps: [
          'Analisar horários atuais de envio',
          'Configurar novo horário otimizado',
          'Ajustar agenda de automação',
          'Monitorar resultados'
        ],
        estimatedTime: '8 minutos',
        requirements: ['Histórico de envios', 'Flexibilidade de horários']
      },
      baseAnalysis: {
        currentState: 'Envio às 9h',
        suggestedState: 'Envio às 14h',
        similarClientsUsage: 56
      }
    }
  ];

  useEffect(() => {
    if (clientId || configurationId) {
      analyzeConfiguration();
    }
  }, [clientId, configurationId]);

  const analyzeConfiguration = async () => {
    setAnalyzing(true);
    
    // Simulate AI analysis
    setTimeout(() => {
      setOptimizations(mockOptimizations);
      setAnalyzing(false);
    }, 3000);
  };

  const handlePreviewOptimization = (optimization: AIOptimization) => {
    setSelectedOptimization(optimization);
    setPreviewDialogOpen(true);
  };

  const handleImplementOptimization = (optimization: AIOptimization) => {
    setSelectedOptimization(optimization);
    setActiveStep(0);
    setImplementationDialogOpen(true);
  };

  const executeImplementation = async () => {
    if (!selectedOptimization) return;
    
    setLoading(true);
    
    // Simulate implementation
    for (let i = 0; i < selectedOptimization.implementation.steps.length; i++) {
      await new Promise(resolve => setTimeout(resolve, 1500));
      setActiveStep(i + 1);
    }
    
    setLoading(false);
    setImplementationDialogOpen(false);
    
    if (onOptimizationApplied) {
      onOptimizationApplied(selectedOptimization);
    }
    
    // Remove applied optimization from list
    setOptimizations(prev => prev.filter(opt => opt.id !== selectedOptimization.id));
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'crítica':
        return 'error';
      case 'alta':
        return 'warning';
      case 'média':
        return 'info';
      default:
        return 'default';
    }
  };

  const getEffortColor = (effort: string) => {
    switch (effort) {
      case 'alto':
        return 'error';
      case 'médio':
        return 'warning';
      default:
        return 'success';
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case 'document':
        return <Info />;
      case 'channel':
        return <Timeline />;
      case 'automation':
        return <AutoAwesome />;
      case 'compliance':
        return <Security />;
      case 'configuration':
        return <Speed />;
      default:
        return <Lightbulb />;
    }
  };

  const renderMetricImpact = (metrics: AIOptimization['impactMetrics']) => {
    const impacts = [];
    
    if (metrics.successRate) {
      impacts.push(`+${metrics.successRate}% taxa de sucesso`);
    }
    if (metrics.timeReduction) {
      impacts.push(`-${metrics.timeReduction}% tempo`);
    }
    if (metrics.costSaving) {
      impacts.push(`-${metrics.costSaving}% custos`);
    }
    if (metrics.complianceImprovement) {
      impacts.push(`+${metrics.complianceImprovement}% compliance`);
    }
    
    return impacts;
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <AutoAwesome sx={{ mr: 2, color: 'primary.main' }} />
          Otimizador de Configuração IA
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Sugestões inteligentes para otimizar sua configuração baseadas em análise de dados e melhores práticas
        </Typography>
      </Box>

      {/* Analysis Status */}
      {analyzing && (
        <Card sx={{ mb: 4 }}>
          <CardContent>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <CircularProgress size={24} sx={{ mr: 2 }} />
              <Typography variant="h6">Analisando configuração...</Typography>
            </Box>
            <Typography variant="body2" color="text.secondary" paragraph>
              Nossa IA está analisando sua configuração atual, comparando com empresas similares e identificando oportunidades de otimização.
            </Typography>
            <LinearProgress />
          </CardContent>
        </Card>
      )}

      {/* Optimizations List */}
      {optimizations.length > 0 && (
        <Box>
          <Typography variant="h6" gutterBottom sx={{ mb: 3 }}>
            {optimizations.length} Otimizações Identificadas
          </Typography>
          
          <Grid container spacing={3}>
            {optimizations.map((optimization) => (
              <Grid item xs={12} md={6} lg={4} key={optimization.id}>
                <Card 
                  sx={{ 
                    height: '100%',
                    border: optimization.priority === 'crítica' ? 2 : 1,
                    borderColor: optimization.priority === 'crítica' ? 'error.main' : 'divider',
                  }}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                        {getTypeIcon(optimization.type)}
                      </Avatar>
                      <Box sx={{ flexGrow: 1 }}>
                        <Typography variant="h6" noWrap>
                          {optimization.title}
                        </Typography>
                        <Box sx={{ display: 'flex', gap: 1, mt: 0.5 }}>
                          <Chip
                            label={optimization.priority}
                            size="small"
                            color={getPriorityColor(optimization.priority) as any}
                          />
                          <Chip
                            label={optimization.implementationEffort}
                            size="small"
                            color={getEffortColor(optimization.implementationEffort) as any}
                            variant="outlined"
                          />
                        </Box>
                      </Box>
                    </Box>
                    
                    <Typography variant="body2" paragraph>
                      {optimization.description}
                    </Typography>
                    
                    <Box sx={{ mb: 2 }}>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                        <Typography variant="caption">Confiança da IA</Typography>
                        <Typography variant="caption" fontWeight="bold">
                          {(optimization.confidence * 100).toFixed(0)}%
                        </Typography>
                      </Box>
                      <LinearProgress
                        variant="determinate"
                        value={optimization.confidence * 100}
                        color={optimization.confidence > 0.8 ? 'success' : optimization.confidence > 0.6 ? 'warning' : 'error'}
                      />
                    </Box>
                    
                    <Typography variant="subtitle2" gutterBottom>
                      Impacto Esperado:
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mb: 2 }}>
                      {renderMetricImpact(optimization.impactMetrics).map((impact, index) => (
                        <Chip
                          key={index}
                          label={impact}
                          size="small"
                          color="success"
                          variant="outlined"
                        />
                      ))}
                    </Box>
                    
                    <Typography variant="body2" color="text.secondary">
                      <strong>Benefício:</strong> {optimization.expectedBenefit}
                    </Typography>
                  </CardContent>
                  
                  <CardActions>
                    <Button
                      size="small"
                      onClick={() => handlePreviewOptimization(optimization)}
                    >
                      Detalhes
                    </Button>
                    <Button
                      size="small"
                      variant="contained"
                      startIcon={<PlayArrow />}
                      onClick={() => handleImplementOptimization(optimization)}
                    >
                      Implementar
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Box>
      )}

      {/* No Optimizations Found */}
      {!analyzing && optimizations.length === 0 && (
        <Card>
          <CardContent sx={{ textAlign: 'center', py: 6 }}>
            <CheckCircle sx={{ fontSize: 80, color: 'success.main', mb: 2 }} />
            <Typography variant="h5" gutterBottom>
              Configuração Otimizada!
            </Typography>
            <Typography variant="body1" color="text.secondary" paragraph>
              Nossa IA analisou sua configuração e não encontrou oportunidades significativas de otimização. 
              Sua configuração atual já segue as melhores práticas.
            </Typography>
            <Button variant="outlined" onClick={analyzeConfiguration}>
              Analisar Novamente
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Preview Dialog */}
      <Dialog
        open={previewDialogOpen}
        onClose={() => setPreviewDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
              {selectedOptimization && getTypeIcon(selectedOptimization.type)}
            </Avatar>
            <Box>
              <Typography variant="h6">
                {selectedOptimization?.title}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Análise detalhada da otimização
              </Typography>
            </Box>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          {selectedOptimization && (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                <strong>Confiança da IA: {(selectedOptimization.confidence * 100).toFixed(0)}%</strong>
                {' • '}
                Baseado em análise de {selectedOptimization.baseAnalysis.similarClientsUsage}% de empresas similares
              </Alert>
              
              <Accordion defaultExpanded>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography variant="h6">Análise Atual vs Sugerida</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={2}>
                    <Grid item xs={12} md={6}>
                      <Paper sx={{ p: 2, bgcolor: 'error.50' }}>
                        <Typography variant="subtitle2" color="error" gutterBottom>
                          Estado Atual
                        </Typography>
                        <Typography variant="body2">
                          {selectedOptimization.baseAnalysis.currentState}
                        </Typography>
                      </Paper>
                    </Grid>
                    <Grid item xs={12} md={6}>
                      <Paper sx={{ p: 2, bgcolor: 'success.50' }}>
                        <Typography variant="subtitle2" color="success.main" gutterBottom>
                          Estado Sugerido
                        </Typography>
                        <Typography variant="body2">
                          {selectedOptimization.baseAnalysis.suggestedState}
                        </Typography>
                      </Paper>
                    </Grid>
                  </Grid>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography variant="h6">Impacto Estimado</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Grid container spacing={2}>
                    {Object.entries(selectedOptimization.impactMetrics).map(([key, value]) => (
                      <Grid item xs={6} key={key}>
                        <Box sx={{ textAlign: 'center', p: 2 }}>
                          <Typography variant="h4" color="primary">
                            +{value}%
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {key === 'successRate' ? 'Taxa de Sucesso' :
                             key === 'timeReduction' ? 'Redução de Tempo' :
                             key === 'costSaving' ? 'Economia de Custo' :
                             key === 'complianceImprovement' ? 'Melhoria Compliance' : key}
                          </Typography>
                        </Box>
                      </Grid>
                    ))}
                  </Grid>
                </AccordionDetails>
              </Accordion>
              
              <Accordion>
                <AccordionSummary expandIcon={<ExpandMore />}>
                  <Typography variant="h6">Plano de Implementação</Typography>
                </AccordionSummary>
                <AccordionDetails>
                  <Typography variant="body2" color="text.secondary" paragraph>
                    <strong>Tempo estimado:</strong> {selectedOptimization.implementation.estimatedTime}
                  </Typography>
                  
                  <Typography variant="subtitle2" gutterBottom>
                    Etapas:
                  </Typography>
                  <List dense>
                    {selectedOptimization.implementation.steps.map((step, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <Avatar sx={{ width: 24, height: 24, bgcolor: 'primary.main', fontSize: '0.8rem' }}>
                            {index + 1}
                          </Avatar>
                        </ListItemIcon>
                        <ListItemText primary={step} />
                      </ListItem>
                    ))}
                  </List>
                  
                  <Divider sx={{ my: 2 }} />
                  
                  <Typography variant="subtitle2" gutterBottom>
                    Requisitos:
                  </Typography>
                  <List dense>
                    {selectedOptimization.implementation.requirements.map((req, index) => (
                      <ListItem key={index}>
                        <ListItemIcon>
                          <CheckCircle color="success" />
                        </ListItemIcon>
                        <ListItemText primary={req} />
                      </ListItem>
                    ))}
                  </List>
                </AccordionDetails>
              </Accordion>
            </Box>
          )}
        </DialogContent>
        
        <DialogActions>
          <Button onClick={() => setPreviewDialogOpen(false)}>
            Fechar
          </Button>
          <Button 
            variant="contained" 
            startIcon={<PlayArrow />}
            onClick={() => {
              setPreviewDialogOpen(false);
              selectedOptimization && handleImplementOptimization(selectedOptimization);
            }}
          >
            Implementar Agora
          </Button>
        </DialogActions>
      </Dialog>

      {/* Implementation Dialog */}
      <Dialog
        open={implementationDialogOpen}
        onClose={!loading ? () => setImplementationDialogOpen(false) : undefined}
        maxWidth="md"
        fullWidth
        disableEscapeKeyDown={loading}
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Science sx={{ mr: 2, color: 'primary.main' }} />
            <Typography variant="h6">
              Implementando Otimização
            </Typography>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          {selectedOptimization && (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                Implementando: <strong>{selectedOptimization.title}</strong>
              </Alert>
              
              <Stepper activeStep={activeStep} orientation="vertical">
                {selectedOptimization.implementation.steps.map((step, index) => (
                  <Step key={index}>
                    <StepLabel>
                      {step}
                    </StepLabel>
                    <StepContent>
                      {loading && activeStep === index && (
                        <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                          <CircularProgress size={20} sx={{ mr: 1 }} />
                          <Typography variant="body2">
                            Executando...
                          </Typography>
                        </Box>
                      )}
                    </StepContent>
                  </Step>
                ))}
              </Stepper>
              
              {activeStep === selectedOptimization.implementation.steps.length && (
                <Alert severity="success" sx={{ mt: 2 }}>
                  ✅ Otimização implementada com sucesso!
                </Alert>
              )}
            </Box>
          )}
        </DialogContent>
        
        <DialogActions>
          <Button 
            onClick={() => setImplementationDialogOpen(false)}
            disabled={loading}
          >
            {activeStep === selectedOptimization?.implementation.steps.length ? 'Concluir' : 'Cancelar'}
          </Button>
          {!loading && activeStep < (selectedOptimization?.implementation.steps.length || 0) && (
            <Button 
              variant="contained"
              onClick={executeImplementation}
            >
              Executar Implementação
            </Button>
          )}
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ConfigurationOptimizer;