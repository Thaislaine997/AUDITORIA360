import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Box,
  Typography,
  Button,
  Paper,
  Tab,
  Tabs,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Alert,
  LinearProgress,
  Chip,
  TextField,
  InputAdornment,
  IconButton,
  Collapse,
} from '@mui/material';
import {
  Psychology,
  Security,
  TrendingUp,
  Warning,
  CheckCircle,
  Error,
  Gavel,
  Search,
  ExpandMore,
  ExpandLess,
  PlayArrow,
  Assessment,
  Lightbulb,
} from '@mui/icons-material';

interface PredictiveAuditRisk {
  id: string;
  clientId: string;
  clientName: string;
  category: 'horas_extras' | 'ferias' | 'adicional_noturno' | 'banco_horas' | 'rescisao';
  severity: 'low' | 'medium' | 'high' | 'critical';
  riskScore: number;
  description: string;
  suggestion: string;
  evidence: string[];
  timeFrame: string;
}

interface ScenarioSimulation {
  id: string;
  title: string;
  description: string;
  impact: {
    financial: number;
    operational: number;
    compliance: number;
  };
  risks: string[];
  recommendations: string[];
}

interface LegislationChange {
  id: string;
  title: string;
  source: string;
  date: string;
  impactLevel: 'low' | 'medium' | 'high';
  affectedClients: number;
  description: string;
  actionRequired: boolean;
}

interface DuraLexAIProps {
  open: boolean;
  onClose: () => void;
}

const DuraLexAI: React.FC<DuraLexAIProps> = ({ open, onClose }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [simulationQuery, setSimulationQuery] = useState('');
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [expandedRisk, setExpandedRisk] = useState<string | null>(null);

  // Mock data for demonstration
  const predictiveRisks: PredictiveAuditRisk[] = [
    {
      id: '1',
      clientId: 'client_1',
      clientName: 'Empresa Alpha',
      category: 'horas_extras',
      severity: 'high',
      riskScore: 85,
      description: 'Aumento de 300% em pagamentos de horas extras nos últimos 2 meses',
      suggestion: 'Preparar documentação de suporte para justificar o banco de horas',
      evidence: [
        'Média mensal anterior: 120 horas extras',
        'Média atual: 360 horas extras',
        'Concentração em 3 funcionários específicos',
        'Ausência de documentação de banco de horas'
      ],
      timeFrame: 'Últimos 60 dias'
    },
    {
      id: '2',
      clientId: 'client_2',
      clientName: 'Beta Corp',
      category: 'ferias',
      severity: 'medium',
      riskScore: 65,
      description: 'Funcionários com mais de 12 meses sem gozar férias',
      suggestion: 'Implementar cronograma de férias obrigatório',
      evidence: [
        '8 funcionários com férias vencidas',
        'Maior período: 18 meses sem férias',
        'Falta de programação de férias coletivas'
      ],
      timeFrame: 'Período atual'
    },
    {
      id: '3',
      clientId: 'client_3',
      clientName: 'Gamma Ltd',
      category: 'adicional_noturno',
      severity: 'critical',
      riskScore: 95,
      description: 'Funcionários noturnos sem recebimento do adicional correto',
      suggestion: 'Revisão urgente da folha e acerto retroativo',
      evidence: [
        '12 funcionários afetados',
        'Período: 6 meses sem adicional',
        'Base de cálculo incorreta',
        'Possível multa: R$ 85.000'
      ],
      timeFrame: 'Janeiro a Junho 2024'
    }
  ];

  const legislationChanges: LegislationChange[] = [
    {
      id: '1',
      title: 'Alteração no Adicional de Periculosidade',
      source: 'Portaria MTE 3.214/2024',
      date: '2024-12-01',
      impactLevel: 'high',
      affectedClients: 15,
      description: 'Nova definição de atividades consideradas perigosas',
      actionRequired: true
    },
    {
      id: '2',
      title: 'Mudança no Cálculo do FGTS',
      source: 'Lei 14.842/2024',
      date: '2024-11-15',
      impactLevel: 'medium',
      affectedClients: 45,
      description: 'Alteração na base de cálculo para funcionários em regime híbrido',
      actionRequired: true
    }
  ];

  const mockScenarios: ScenarioSimulation[] = [
    {
      id: '1',
      title: 'Férias Coletivas - 30% da Empresa X em Dezembro',
      description: 'Simulação do impacto de conceder férias coletivas para 30% dos funcionários',
      impact: {
        financial: 125000,
        operational: 65,
        compliance: 95
      },
      risks: [
        'Redução de 35% na capacidade operacional',
        'Necessidade de terceirização temporária',
        'Possível atraso em entregas'
      ],
      recommendations: [
        'Antecipação do 13º salário',
        'Contratação de temporários',
        'Comunicação prévia aos clientes'
      ]
    }
  ];

  const handleSimulationRun = () => {
    if (!simulationQuery.trim()) return;
    
    setIsAnalyzing(true);
    
    // Simulate analysis time
    setTimeout(() => {
      setIsAnalyzing(false);
    }, 3000);
  };

  const getSeverityColor = (severity: string) => {
    switch (severity) {
      case 'critical': return 'error';
      case 'high': return 'warning';
      case 'medium': return 'info';
      case 'low': return 'success';
      default: return 'default';
    }
  };

  const getSeverityIcon = (severity: string) => {
    switch (severity) {
      case 'critical': return <Error color="error" />;
      case 'high': return <Warning color="warning" />;
      case 'medium': return <CheckCircle color="info" />;
      case 'low': return <CheckCircle color="success" />;
      default: return <CheckCircle />;
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="lg"
      fullWidth
      PaperProps={{
        sx: {
          minHeight: '80vh',
          background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
          color: 'white'
        }
      }}
    >
      <DialogTitle>
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Psychology sx={{ fontSize: 40, color: '#4ecdc4' }} />
          <Box>
            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
              DURA LEX
            </Typography>
            <Typography variant="subtitle1" sx={{ color: '#4ecdc4' }}>
              Consciência Jurídica Preditiva
            </Typography>
          </Box>
        </Box>
      </DialogTitle>

      <DialogContent sx={{ p: 0 }}>
        <Tabs
          value={activeTab}
          onChange={(_, newValue) => setActiveTab(newValue)}
          sx={{
            borderBottom: 1,
            borderColor: 'rgba(255,255,255,0.2)',
            '& .MuiTab-root': { color: 'white' },
            '& .Mui-selected': { color: '#4ecdc4' }
          }}
        >
          <Tab 
            icon={<Security />} 
            label="Fiscal do Futuro" 
            iconPosition="start"
          />
          <Tab 
            icon={<Assessment />} 
            label="Simulador de Cenários" 
            iconPosition="start"
          />
          <Tab 
            icon={<Gavel />} 
            label="Vigia da Legislação" 
            iconPosition="start"
          />
        </Tabs>

        <Box sx={{ p: 3 }}>
          {/* Tab 1: Fiscal do Futuro */}
          {activeTab === 0 && (
            <Box>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Security color="primary" />
                Relatório de Risco de Auditoria Preditivo
              </Typography>
              
              <Alert 
                severity="info" 
                sx={{ mb: 3, bgcolor: 'rgba(76, 175, 80, 0.1)', color: 'white' }}
              >
                Dura Lex analisou continuamente {predictiveRisks.length} cenários de risco. 
                Última atualização: {new Date().toLocaleString()}
              </Alert>

              <List>
                {predictiveRisks.map((risk) => (
                  <Paper
                    key={risk.id}
                    sx={{
                      mb: 2,
                      p: 2,
                      bgcolor: 'rgba(255,255,255,0.05)',
                      border: `1px solid ${getSeverityColor(risk.severity) === 'error' ? '#f44336' : 
                                            getSeverityColor(risk.severity) === 'warning' ? '#ff9800' : '#2196f3'}`
                    }}
                  >
                    <ListItem
                      sx={{ p: 0, cursor: 'pointer' }}
                      onClick={() => setExpandedRisk(expandedRisk === risk.id ? null : risk.id)}
                    >
                      <ListItemIcon>
                        {getSeverityIcon(risk.severity)}
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                            <Typography variant="h6" sx={{ color: 'white' }}>
                              {risk.clientName}
                            </Typography>
                            <Chip
                              label={`${risk.riskScore}% risco`}
                              color={getSeverityColor(risk.severity) as any}
                              size="small"
                            />
                            <Chip
                              label={risk.category.replace('_', ' ')}
                              variant="outlined"
                              size="small"
                              sx={{ color: 'white', borderColor: 'rgba(255,255,255,0.3)' }}
                            />
                          </Box>
                        }
                        secondary={
                          <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                            {risk.description}
                          </Typography>
                        }
                      />
                      <IconButton sx={{ color: 'white' }}>
                        {expandedRisk === risk.id ? <ExpandLess /> : <ExpandMore />}
                      </IconButton>
                    </ListItem>
                    
                    <Collapse in={expandedRisk === risk.id}>
                      <Box sx={{ mt: 2, pl: 2 }}>
                        <Typography variant="subtitle2" gutterBottom sx={{ color: '#4ecdc4' }}>
                          💡 Sugestão:
                        </Typography>
                        <Typography variant="body2" paragraph sx={{ color: 'white' }}>
                          {risk.suggestion}
                        </Typography>
                        
                        <Typography variant="subtitle2" gutterBottom sx={{ color: '#4ecdc4' }}>
                          📋 Evidências:
                        </Typography>
                        <List dense>
                          {risk.evidence.map((evidence, index) => (
                            <ListItem key={index} sx={{ py: 0 }}>
                              <ListItemText
                                primary={evidence}
                                sx={{ '& .MuiListItemText-primary': { color: 'rgba(255,255,255,0.8)', fontSize: '0.875rem' } }}
                              />
                            </ListItem>
                          ))}
                        </List>
                        
                        <Button
                          variant="contained"
                          color="primary"
                          size="small"
                          sx={{ mt: 1 }}
                          onClick={() => {
                            // Handle preparation of documentation
                          }}
                        >
                          Preparar Documentação
                        </Button>
                      </Box>
                    </Collapse>
                  </Paper>
                ))}
              </List>
            </Box>
          )}

          {/* Tab 2: Simulador de Cenários */}
          {activeTab === 1 && (
            <Box>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Assessment color="primary" />
                Simulador de Cenário de Impacto
              </Typography>
              
              <Paper sx={{ p: 3, mb: 3, bgcolor: 'rgba(255,255,255,0.05)' }}>
                <TextField
                  fullWidth
                  multiline
                  rows={3}
                  value={simulationQuery}
                  onChange={(e) => setSimulationQuery(e.target.value)}
                  placeholder="Descreva o cenário que deseja simular... Ex: 'Qual o impacto de conceder férias coletivas para 30% da empresa X em Dezembro?'"
                  sx={{
                    mb: 2,
                    '& .MuiOutlinedInput-root': {
                      color: 'white',
                      '& fieldset': { borderColor: 'rgba(255,255,255,0.3)' },
                      '&:hover fieldset': { borderColor: 'rgba(255,255,255,0.5)' },
                      '&.Mui-focused fieldset': { borderColor: '#4ecdc4' }
                    },
                    '& .MuiInputLabel-root': { color: 'rgba(255,255,255,0.7)' }
                  }}
                  InputProps={{
                    endAdornment: (
                      <InputAdornment position="end">
                        <IconButton 
                          onClick={handleSimulationRun}
                          disabled={!simulationQuery.trim() || isAnalyzing}
                          sx={{ color: '#4ecdc4' }}
                        >
                          <PlayArrow />
                        </IconButton>
                      </InputAdornment>
                    )
                  }}
                />
                
                {isAnalyzing && (
                  <Box sx={{ mb: 2 }}>
                    <Typography variant="body2" gutterBottom sx={{ color: '#4ecdc4' }}>
                      Dura Lex está analisando o cenário...
                    </Typography>
                    <LinearProgress 
                      sx={{ 
                        bgcolor: 'rgba(255,255,255,0.1)',
                        '& .MuiLinearProgress-bar': { bgcolor: '#4ecdc4' }
                      }} 
                    />
                  </Box>
                )}
              </Paper>

              {/* Mock simulation results */}
              {mockScenarios.map((scenario) => (
                <Paper
                  key={scenario.id}
                  sx={{
                    p: 3,
                    mb: 2,
                    bgcolor: 'rgba(255,255,255,0.05)',
                    border: '1px solid rgba(76, 205, 196, 0.3)'
                  }}
                >
                  <Typography variant="h6" gutterBottom sx={{ color: '#4ecdc4' }}>
                    📊 {scenario.title}
                  </Typography>
                  
                  <Typography variant="body2" paragraph sx={{ color: 'white' }}>
                    {scenario.description}
                  </Typography>
                  
                  <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr 1fr', gap: 2, mb: 2 }}>
                    <Paper sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.03)', textAlign: 'center' }}>
                      <Typography variant="h4" sx={{ color: '#4CAF50' }}>
                        R$ {scenario.impact.financial.toLocaleString()}
                      </Typography>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                        Impacto Financeiro
                      </Typography>
                    </Paper>
                    
                    <Paper sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.03)', textAlign: 'center' }}>
                      <Typography variant="h4" sx={{ color: '#FF9800' }}>
                        {scenario.impact.operational}%
                      </Typography>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                        Capacidade Operacional
                      </Typography>
                    </Paper>
                    
                    <Paper sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.03)', textAlign: 'center' }}>
                      <Typography variant="h4" sx={{ color: '#2196F3' }}>
                        {scenario.impact.compliance}%
                      </Typography>
                      <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.7)' }}>
                        Compliance
                      </Typography>
                    </Paper>
                  </Box>
                  
                  <Box sx={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 2 }}>
                    <Box>
                      <Typography variant="subtitle2" gutterBottom sx={{ color: '#ff6b6b' }}>
                        ⚠️ Riscos Identificados:
                      </Typography>
                      <List dense>
                        {scenario.risks.map((risk, index) => (
                          <ListItem key={index} sx={{ py: 0 }}>
                            <ListItemText
                              primary={risk}
                              sx={{ '& .MuiListItemText-primary': { color: 'rgba(255,255,255,0.8)', fontSize: '0.875rem' } }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                    
                    <Box>
                      <Typography variant="subtitle2" gutterBottom sx={{ color: '#4ecdc4' }}>
                        💡 Recomendações:
                      </Typography>
                      <List dense>
                        {scenario.recommendations.map((rec, index) => (
                          <ListItem key={index} sx={{ py: 0 }}>
                            <ListItemText
                              primary={rec}
                              sx={{ '& .MuiListItemText-primary': { color: 'rgba(255,255,255,0.8)', fontSize: '0.875rem' } }}
                            />
                          </ListItem>
                        ))}
                      </List>
                    </Box>
                  </Box>
                </Paper>
              ))}
            </Box>
          )}

          {/* Tab 3: Vigia da Legislação */}
          {activeTab === 2 && (
            <Box>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Gavel color="primary" />
                Mudanças Legislativas Detectadas
              </Typography>
              
              <Alert 
                severity="warning" 
                sx={{ mb: 3, bgcolor: 'rgba(255, 152, 0, 0.1)', color: 'white' }}
              >
                Dura Lex monitora continuamente o Diário Oficial e convenções coletivas. 
                {legislationChanges.filter(c => c.actionRequired).length} mudanças requerem ação.
              </Alert>

              <List>
                {legislationChanges.map((change) => (
                  <Paper
                    key={change.id}
                    sx={{
                      mb: 2,
                      p: 2,
                      bgcolor: 'rgba(255,255,255,0.05)',
                      border: `1px solid ${change.impactLevel === 'high' ? '#f44336' : 
                                           change.impactLevel === 'medium' ? '#ff9800' : '#4caf50'}`
                    }}
                  >
                    <ListItem sx={{ p: 0 }}>
                      <ListItemIcon>
                        <Gavel color={change.impactLevel === 'high' ? 'error' : 
                                     change.impactLevel === 'medium' ? 'warning' : 'success'} />
                      </ListItemIcon>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                            <Typography variant="h6" sx={{ color: 'white' }}>
                              {change.title}
                            </Typography>
                            <Chip
                              label={change.impactLevel}
                              color={change.impactLevel === 'high' ? 'error' : 
                                     change.impactLevel === 'medium' ? 'warning' : 'success'}
                              size="small"
                            />
                            {change.actionRequired && (
                              <Chip
                                label="Ação Necessária"
                                color="warning"
                                size="small"
                              />
                            )}
                          </Box>
                        }
                        secondary={
                          <Box>
                            <Typography variant="body2" sx={{ color: 'rgba(255,255,255,0.7)', mb: 1 }}>
                              {change.description}
                            </Typography>
                            <Typography variant="caption" sx={{ color: 'rgba(255,255,255,0.5)' }}>
                              Fonte: {change.source} | Data: {change.date} | 
                              Clientes afetados: {change.affectedClients}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                    
                    {change.actionRequired && (
                      <Box sx={{ mt: 2, pl: 2 }}>
                        <Button
                          variant="contained"
                          color="primary"
                          size="small"
                          startIcon={<Lightbulb />}
                          onClick={() => {
                            // Handle creating action plan
                          }}
                        >
                          Criar Plano de Ação
                        </Button>
                      </Box>
                    )}
                  </Paper>
                ))}
              </List>
            </Box>
          )}
        </Box>
      </DialogContent>

      <DialogActions sx={{ p: 3 }}>
        <Button 
          onClick={onClose}
          sx={{ color: 'white', borderColor: 'rgba(255,255,255,0.3)' }}
          variant="outlined"
        >
          Fechar
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default DuraLexAI;