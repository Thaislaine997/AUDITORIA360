import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  CardActions,
  Button,
  Grid,
  Alert,
  Chip,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemSecondaryAction,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControlLabel,
  Switch,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Paper,
  Stepper,
  Step,
  StepLabel,
  IconButton,
  Tooltip,
  LinearProgress,
  Divider,
  Avatar,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Fade,
  Slide,
  Zoom,
} from '@mui/material';
import {
  Security,
  CheckCircle,
  Warning,
  Error,
  ExpandMore,
  Visibility,
  Edit,
  Delete,
  Download,
  PersonAdd,
  Shield,
  Policy,
  AccountBox,
  History,
  Map,
  Description,
  VpnKey,
  Timeline,
  Psychology,
  VisibilityOff,
  Gavel,
} from '@mui/icons-material';
import { useIntentionStore } from '../stores/intentionStore';
import { useAdaptiveUI } from '../hooks/useNeuralSignals';

interface DataSubject {
  id: number;
  name: string;
  email: string;
  phone?: string;
  document?: string;
  consentStatus: 'given' | 'withdrawn' | 'pending';
  consentDate: Date;
  dataRetentionDate?: Date;
  lastInteraction: Date;
  dataCategories: string[];
  rights: {
    access: boolean;
    rectification: boolean;
    erasure: boolean;
    portability: boolean;
    restriction: boolean;
  };
}

interface ConsentRecord {
  id: number;
  subjectId: number;
  purpose: string;
  consentType: 'explicit' | 'implicit';
  status: 'active' | 'withdrawn' | 'expired';
  grantedAt: Date;
  withdrawnAt?: Date;
  proofId: string;
  ipAddress: string;
  userAgent: string;
}

interface DataMap {
  dataType: string;
  category: 'personal' | 'sensitive' | 'anonymous';
  purpose: string;
  legalBasis: string;
  retention: string;
  location: string;
  processors: string[];
  transfers: string[];
}

const LGPDComplianceCenter: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'overview' | 'subjects' | 'consent' | 'datamap' | 'rights'>('overview');
  const [subjects, setSubjects] = useState<DataSubject[]>([]);
  const [consentRecords, setConsentRecords] = useState<ConsentRecord[]>([]);
  const [dataMap, setDataMap] = useState<DataMap[]>([]);
  const [selectedSubject, setSelectedSubject] = useState<DataSubject | null>(null);
  const [rightsDialogOpen, setRightsDialogOpen] = useState(false);
  const [consentDialogOpen, setConsentDialogOpen] = useState(false);
  const [dataMapDialogOpen, setDataMapDialogOpen] = useState(false);
  
  // Neuro-Symbolic Guardian State
  const [guardianMode, setGuardianMode] = useState(false);
  const [guardianMessage, setGuardianMessage] = useState("");
  const [privacyRiskLevel, setPrivacyRiskLevel] = useState<'low' | 'medium' | 'high'>('low');
  const [showGuardianDialog, setShowGuardianDialog] = useState(false);
  
  // Neural interface hooks
  const { currentIntentions, cognitiveLoad } = useIntentionStore();
  const { shouldSimplify, adaptationStrategy } = useAdaptiveUI();

  // Guardian activation detection
  useEffect(() => {
    const privacyRelatedIntentions = currentIntentions.filter(intention => 
      intention.target.toLowerCase().includes('lgpd') ||
      intention.target.toLowerCase().includes('privacy') ||
      intention.target.toLowerCase().includes('consent') ||
      intention.target.toLowerCase().includes('data') ||
      intention.context?.privacyRelated
    );

    if (privacyRelatedIntentions.length > 0 && !guardianMode) {
      // Guardian materializes when privacy intentions are detected
      console.log("🛡️ LGPD Guardian: Privacy intention detected, materializing...");
      
      setGuardianMode(true);
      setGuardianMessage(
        "🛡️ Guardião LGPD ativado! Detectei intenções relacionadas à privacidade. " +
        "Como guardião da conformidade, estou aqui para auxiliá-lo com questões de proteção de dados."
      );
      
      // Assess privacy risk based on cognitive load
      if (cognitiveLoad.level === 'high') {
        setPrivacyRiskLevel('high');
      } else if (cognitiveLoad.level === 'medium') {
        setPrivacyRiskLevel('medium');
      }
      
      setShowGuardianDialog(true);
      
      // Auto-hide guardian message after 10 seconds
      setTimeout(() => {
        setShowGuardianDialog(false);
      }, 10000);
    }
  }, [currentIntentions, guardianMode, cognitiveLoad.level]);

  // Mock data
  useEffect(() => {
    const mockSubjects: DataSubject[] = [
      {
        id: 1,
        name: 'João Silva Santos',
        email: 'joao.silva@email.com',
        phone: '+55 11 99999-9999',
        document: '123.456.789-00',
        consentStatus: 'given',
        consentDate: new Date('2024-01-15'),
        dataRetentionDate: new Date('2027-01-15'),
        lastInteraction: new Date('2024-01-20'),
        dataCategories: ['Dados de Contato', 'Dados Financeiros', 'Dados de Uso'],
        rights: {
          access: true,
          rectification: true,
          erasure: true,
          portability: true,
          restriction: false,
        },
      },
      {
        id: 2,
        name: 'Maria Costa Oliveira',
        email: 'maria.costa@empresa.com',
        phone: '+55 11 88888-8888',
        consentStatus: 'given',
        consentDate: new Date('2024-01-10'),
        lastInteraction: new Date('2024-01-22'),
        dataCategories: ['Dados de Contato', 'Dados de Uso'],
        rights: {
          access: true,
          rectification: true,
          erasure: false,
          portability: true,
          restriction: false,
        },
      },
    ];

    const mockConsent: ConsentRecord[] = [
      {
        id: 1,
        subjectId: 1,
        purpose: 'Envio de documentos fiscais',
        consentType: 'explicit',
        status: 'active',
        grantedAt: new Date('2024-01-15'),
        proofId: 'CONSENT_PROOF_001',
        ipAddress: '192.168.1.100',
        userAgent: 'Mozilla/5.0...',
      },
      {
        id: 2,
        subjectId: 2,
        purpose: 'Comunicação via WhatsApp',
        consentType: 'explicit',
        status: 'active',
        grantedAt: new Date('2024-01-10'),
        proofId: 'CONSENT_PROOF_002',
        ipAddress: '192.168.1.101',
        userAgent: 'Mozilla/5.0...',
      },
    ];

    const mockDataMap: DataMap[] = [
      {
        dataType: 'Email',
        category: 'personal',
        purpose: 'Comunicação e envio de documentos',
        legalBasis: 'Consentimento',
        retention: '3 anos após término do contrato',
        location: 'Servidor Brasil (AWS São Paulo)',
        processors: ['AWS', 'SendGrid'],
        transfers: [],
      },
      {
        dataType: 'CPF/CNPJ',
        category: 'personal',
        purpose: 'Identificação e compliance fiscal',
        legalBasis: 'Obrigação legal',
        retention: '5 anos (exigência legal)',
        location: 'Servidor Brasil (AWS São Paulo)',
        processors: ['AWS'],
        transfers: ['Receita Federal (quando exigido)'],
      },
      {
        dataType: 'Dados Financeiros',
        category: 'sensitive',
        purpose: 'Processamento de folha de pagamento',
        legalBasis: 'Consentimento + Obrigação legal',
        retention: '10 anos (CLT)',
        location: 'Servidor Brasil (AWS São Paulo)',
        processors: ['AWS', 'Sistema Bancário'],
        transfers: ['Bancos parceiros (quando autorizado)'],
      },
    ];

    setSubjects(mockSubjects);
    setConsentRecords(mockConsent);
    setDataMap(mockDataMap);
  }, []);

  const handleSubjectRights = (subject: DataSubject) => {
    setSelectedSubject(subject);
    setRightsDialogOpen(true);
  };

  const handleExportData = (subjectId: number) => {
    // Simulate data export
    const exportData = {
      subject: subjects.find(s => s.id === subjectId),
      consent: consentRecords.filter(c => c.subjectId === subjectId),
      dataProcessed: ['Emails enviados', 'Documentos processados', 'Interações registradas'],
      exportDate: new Date().toISOString(),
    };

    const blob = new Blob([JSON.stringify(exportData, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `dados_titular_${subjectId}.json`;
    a.click();
    URL.revokeObjectURL(url);
  };

  const getComplianceScore = () => {
    const totalChecks = 10;
    const passedChecks = 8; // Mock compliance score
    return (passedChecks / totalChecks) * 100;
  };

  const getConsentStatusColor = (status: string) => {
    switch (status) {
      case 'given':
      case 'active':
        return 'success';
      case 'withdrawn':
        return 'error';
      case 'pending':
      case 'expired':
        return 'warning';
      default:
        return 'default';
    }
  };

  const renderOverview = () => (
    <Box>
      {/* Compliance Score */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <Shield sx={{ mr: 1, color: 'primary.main' }} />
            Score de Compliance LGPD
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Box sx={{ width: '100%', mr: 1 }}>
              <LinearProgress 
                variant="determinate" 
                value={getComplianceScore()} 
                sx={{ height: 10, borderRadius: 5 }}
                color={getComplianceScore() >= 80 ? 'success' : getComplianceScore() >= 60 ? 'warning' : 'error'}
              />
            </Box>
            <Typography variant="h6" color="primary">
              {getComplianceScore().toFixed(0)}%
            </Typography>
          </Box>
          <Typography variant="body2" color="text.secondary">
            {getComplianceScore() >= 80 ? 'Excelente compliance LGPD' : 
             getComplianceScore() >= 60 ? 'Compliance adequada, algumas melhorias recomendadas' :
             'Compliance insuficiente, ações urgentes necessárias'}
          </Typography>
        </CardContent>
      </Card>

      {/* Quick Stats */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                  <AccountBox />
                </Avatar>
                <Box>
                  <Typography variant="h4">{subjects.length}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Titulares de Dados
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                  <CheckCircle />
                </Avatar>
                <Box>
                  <Typography variant="h4">
                    {consentRecords.filter(c => c.status === 'active').length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Consentimentos Ativos
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                  <Map />
                </Avatar>
                <Box>
                  <Typography variant="h4">{dataMap.length}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Tipos de Dados Mapeados
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={3}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                  <History />
                </Avatar>
                <Box>
                  <Typography variant="h4">0</Typography>
                  <Typography variant="body2" color="text.secondary">
                    Solicitações Pendentes
                  </Typography>
                </Box>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Compliance Checklist */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Checklist de Compliance LGPD
          </Typography>
          <List>
            <ListItem>
              <ListItemIcon>
                <CheckCircle color="success" />
              </ListItemIcon>
              <ListItemText 
                primary="Política de Privacidade implementada"
                secondary="Documento atualizado e acessível aos usuários"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CheckCircle color="success" />
              </ListItemIcon>
              <ListItemText 
                primary="Sistema de coleta de consentimento"
                secondary="Consentimento explícito sendo coletado para todas as finalidades"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <CheckCircle color="success" />
              </ListItemIcon>
              <ListItemText 
                primary="Mapeamento de dados pessoais"
                secondary="Inventário completo dos dados processados"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Warning color="warning" />
              </ListItemIcon>
              <ListItemText 
                primary="Portal do titular implementado"
                secondary="Implementação em andamento - 75% concluído"
              />
            </ListItem>
            <ListItem>
              <ListItemIcon>
                <Error color="error" />
              </ListItemIcon>
              <ListItemText 
                primary="Processo de resposta a incidentes"
                secondary="Documentação do processo ainda em desenvolvimento"
              />
            </ListItem>
          </List>
        </CardContent>
      </Card>
    </Box>
  );

  const renderSubjects = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h6">Titulares de Dados</Typography>
        <Button variant="contained" startIcon={<PersonAdd />}>
          Cadastrar Titular
        </Button>
      </Box>
      
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Nome</TableCell>
              <TableCell>Email</TableCell>
              <TableCell>Status do Consentimento</TableCell>
              <TableCell>Última Interação</TableCell>
              <TableCell>Categorias de Dados</TableCell>
              <TableCell align="center">Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {subjects.map((subject) => (
              <TableRow key={subject.id}>
                <TableCell>{subject.name}</TableCell>
                <TableCell>{subject.email}</TableCell>
                <TableCell>
                  <Chip
                    label={subject.consentStatus === 'given' ? 'Consentimento Dado' : 
                           subject.consentStatus === 'withdrawn' ? 'Consentimento Retirado' :
                           'Pendente'}
                    color={getConsentStatusColor(subject.consentStatus) as any}
                    size="small"
                  />
                </TableCell>
                <TableCell>{subject.lastInteraction.toLocaleDateString()}</TableCell>
                <TableCell>
                  <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                    {subject.dataCategories.slice(0, 2).map((category) => (
                      <Chip key={category} label={category} size="small" variant="outlined" />
                    ))}
                    {subject.dataCategories.length > 2 && (
                      <Chip label={`+${subject.dataCategories.length - 2}`} size="small" />
                    )}
                  </Box>
                </TableCell>
                <TableCell align="center">
                  <Tooltip title="Ver direitos do titular">
                    <IconButton onClick={() => handleSubjectRights(subject)}>
                      <Visibility />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Exportar dados">
                    <IconButton onClick={() => handleExportData(subject.id)}>
                      <Download />
                    </IconButton>
                  </Tooltip>
                  <Tooltip title="Editar">
                    <IconButton>
                      <Edit />
                    </IconButton>
                  </Tooltip>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );

  const renderDataMap = () => (
    <Box>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 3 }}>
        <Typography variant="h6">Mapeamento de Dados</Typography>
        <Button variant="contained" startIcon={<Map />}>
          Adicionar Tipo de Dado
        </Button>
      </Box>
      
      <Alert severity="info" sx={{ mb: 3 }}>
        O mapeamento de dados é essencial para demonstrar compliance com a LGPD. 
        Mantenha este inventário sempre atualizado.
      </Alert>
      
      {dataMap.map((data, index) => (
        <Accordion key={index}>
          <AccordionSummary expandIcon={<ExpandMore />}>
            <Box sx={{ display: 'flex', alignItems: 'center', width: '100%' }}>
              <Typography variant="h6" sx={{ flexGrow: 1 }}>
                {data.dataType}
              </Typography>
              <Chip
                label={data.category === 'personal' ? 'Pessoal' : 
                       data.category === 'sensitive' ? 'Sensível' : 'Anônimo'}
                color={data.category === 'sensitive' ? 'error' : 
                       data.category === 'personal' ? 'warning' : 'success'}
                size="small"
                sx={{ mr: 2 }}
              />
            </Box>
          </AccordionSummary>
          <AccordionDetails>
            <Grid container spacing={2}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" gutterBottom>Finalidade</Typography>
                <Typography variant="body2" paragraph>{data.purpose}</Typography>
                
                <Typography variant="subtitle2" gutterBottom>Base Legal</Typography>
                <Typography variant="body2" paragraph>{data.legalBasis}</Typography>
                
                <Typography variant="subtitle2" gutterBottom>Retenção</Typography>
                <Typography variant="body2">{data.retention}</Typography>
              </Grid>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" gutterBottom>Localização</Typography>
                <Typography variant="body2" paragraph>{data.location}</Typography>
                
                <Typography variant="subtitle2" gutterBottom>Processadores</Typography>
                <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', mb: 2 }}>
                  {data.processors.map((processor) => (
                    <Chip key={processor} label={processor} size="small" variant="outlined" />
                  ))}
                </Box>
                
                {data.transfers.length > 0 && (
                  <>
                    <Typography variant="subtitle2" gutterBottom>Transferências</Typography>
                    <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                      {data.transfers.map((transfer) => (
                        <Chip key={transfer} label={transfer} size="small" color="warning" />
                      ))}
                    </Box>
                  </>
                )}
              </Grid>
            </Grid>
          </AccordionDetails>
        </Accordion>
      ))}
    </Box>
  );

  return (
    <Box>
      {/* Neuro-Symbolic Guardian Dialog */}
      <Dialog
        open={showGuardianDialog}
        onClose={() => setShowGuardianDialog(false)}
        maxWidth="md"
        fullWidth
        TransitionComponent={Zoom}
      >
        <DialogTitle sx={{ 
          display: 'flex', 
          alignItems: 'center', 
          gap: 1,
          bgcolor: privacyRiskLevel === 'high' ? 'error.light' : 
                  privacyRiskLevel === 'medium' ? 'warning.light' : 'success.light'
        }}>
          <Shield sx={{ 
            color: privacyRiskLevel === 'high' ? 'error.main' : 
                   privacyRiskLevel === 'medium' ? 'warning.main' : 'success.main',
            animation: 'pulse 2s infinite',
            '@keyframes pulse': {
              '0%': { transform: 'scale(1)' },
              '50%': { transform: 'scale(1.1)' },
              '100%': { transform: 'scale(1)' },
            },
          }} />
          🛡️ Guardião LGPD - Interface Neuro-Simbólica
        </DialogTitle>
        <DialogContent>
          <Alert 
            severity={privacyRiskLevel === 'high' ? 'error' : 
                     privacyRiskLevel === 'medium' ? 'warning' : 'info'}
            icon={<Psychology />}
            sx={{ mb: 2 }}
          >
            {guardianMessage}
          </Alert>
          
          <Box sx={{ mt: 2 }}>
            <Typography variant="h6" gutterBottom>
              🧠 Análise Neural da Situação:
            </Typography>
            <List dense>
              <ListItem>
                <ListItemIcon>
                  <Psychology color="primary" />
                </ListItemIcon>
                <ListItemText 
                  primary="Intenções de Privacidade Detectadas"
                  secondary={`${currentIntentions.filter(i => 
                    i.target.toLowerCase().includes('lgpd') || 
                    i.target.toLowerCase().includes('privacy')
                  ).length} intenção(ões) relacionada(s) à privacidade`}
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  <Gavel color={privacyRiskLevel === 'high' ? 'error' : 'success'} />
                </ListItemIcon>
                <ListItemText 
                  primary="Nível de Risco de Privacidade"
                  secondary={`${privacyRiskLevel.toUpperCase()} - Baseado na carga cognitiva e padrões de interação`}
                />
              </ListItem>
              
              <ListItem>
                <ListItemIcon>
                  <VisibilityOff color="info" />
                </ListItemIcon>
                <ListItemText 
                  primary="Modo Guardião Ativo"
                  secondary="Monitoramento contínuo de atividades relacionadas à proteção de dados"
                />
              </ListItem>
            </List>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowGuardianDialog(false)}>
            Entendi
          </Button>
          <Button 
            variant="contained" 
            onClick={() => {
              setShowGuardianDialog(false);
              setActiveTab('overview');
            }}
          >
            Prosseguir com Monitoramento
          </Button>
        </DialogActions>
      </Dialog>

      {/* Header with Guardian Status */}
      <Box sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h4" component="h1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
            <Security sx={{ mr: 2, color: 'primary.main' }} />
            Centro de Compliance LGPD
            {guardianMode && (
              <Fade in={guardianMode}>
                <Chip 
                  label="🛡️ Guardião Ativo" 
                  color="success" 
                  icon={<Shield />}
                  sx={{ 
                    ml: 2,
                    animation: 'glow 3s ease-in-out infinite alternate',
                    '@keyframes glow': {
                      from: { boxShadow: '0 0 5px rgba(76, 175, 80, 0.5)' },
                      to: { boxShadow: '0 0 20px rgba(76, 175, 80, 0.8)' },
                    },
                  }}
                />
              </Fade>
            )}
          </Typography>
          
          {/* Adaptive UI Status */}
          {shouldSimplify && (
            <Alert severity="info" icon={<Psychology />}>
              Interface simplificada ativa - Carga cognitiva elevada detectada
            </Alert>
          )}
        </Box>
        
        <Typography variant="body1" color="text.secondary">
          {guardianMode ? 
            "🧠 Modo Guardião: Monitoramento neuro-simbólico ativo para proteção de dados" :
            "Gerencie a conformidade com a Lei Geral de Proteção de Dados (LGPD)"
          }
        </Typography>
      </Box>

      {/* Navigation Tabs - Adaptive based on cognitive load */}
      <Paper sx={{ mb: 4 }}>
        <Box sx={{ display: 'flex', overflow: 'auto' }}>
          {[
            { key: 'overview', label: 'Visão Geral', icon: <Shield /> },
            { key: 'subjects', label: 'Titulares', icon: <AccountBox /> },
            ...(adaptationStrategy.hideAdvancedFeatures ? [] : [
              { key: 'consent', label: 'Consentimentos', icon: <Policy /> },
              { key: 'datamap', label: 'Mapa de Dados', icon: <Map /> },
              { key: 'rights', label: 'Direitos', icon: <VpnKey /> },
            ]),
          ].map((tab) => (
            <Button
              key={tab.key}
              onClick={() => setActiveTab(tab.key as any)}
              sx={{
                minWidth: 'auto',
                p: adaptationStrategy.reduceAnimations ? 1 : 2,
                borderRadius: 0,
                backgroundColor: activeTab === tab.key ? 'action.selected' : 'transparent',
                borderBottom: activeTab === tab.key ? 2 : 0,
                borderColor: 'primary.main',
                border: adaptationStrategy.highlightPrimaryActions && activeTab === tab.key ? 2 : 0,
                transition: adaptationStrategy.reduceAnimations ? 'none' : 'all 0.3s ease',
              }}
              startIcon={tab.icon}
            >
              {tab.label}
              {adaptationStrategy.showHelpHints && activeTab === tab.key && (
                <Chip label="Ativo" size="small" color="primary" sx={{ ml: 1 }} />
              )}
            </Button>
          ))}
        </Box>
      </Paper>

      {/* Tab Content */}
      {activeTab === 'overview' && renderOverview()}
      {activeTab === 'subjects' && renderSubjects()}
      {activeTab === 'datamap' && renderDataMap()}

      {/* Rights Dialog */}
      <Dialog
        open={rightsDialogOpen}
        onClose={() => setRightsDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          Direitos do Titular - {selectedSubject?.name}
        </DialogTitle>
        <DialogContent>
          {selectedSubject && (
            <Box>
              <Alert severity="info" sx={{ mb: 3 }}>
                Os titulares têm os seguintes direitos garantidos pela LGPD
              </Alert>
              
              <List>
                <ListItem>
                  <ListItemIcon>
                    <Visibility color={selectedSubject.rights.access ? 'success' : 'disabled'} />
                  </ListItemIcon>
                  <ListItemText
                    primary="Direito de Acesso"
                    secondary="Visualizar quais dados pessoais são processados"
                  />
                  <ListItemSecondaryAction>
                    <Switch checked={selectedSubject.rights.access} />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <Edit color={selectedSubject.rights.rectification ? 'success' : 'disabled'} />
                  </ListItemIcon>
                  <ListItemText
                    primary="Direito de Retificação"
                    secondary="Corrigir dados incompletos, inexatos ou desatualizados"
                  />
                  <ListItemSecondaryAction>
                    <Switch checked={selectedSubject.rights.rectification} />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <Delete color={selectedSubject.rights.erasure ? 'success' : 'disabled'} />
                  </ListItemIcon>
                  <ListItemText
                    primary="Direito de Eliminação"
                    secondary="Solicitar a exclusão de dados pessoais"
                  />
                  <ListItemSecondaryAction>
                    <Switch checked={selectedSubject.rights.erasure} />
                  </ListItemSecondaryAction>
                </ListItem>
                
                <ListItem>
                  <ListItemIcon>
                    <Download color={selectedSubject.rights.portability ? 'success' : 'disabled'} />
                  </ListItemIcon>
                  <ListItemText
                    primary="Direito de Portabilidade"
                    secondary="Exportar dados em formato estruturado"
                  />
                  <ListItemSecondaryAction>
                    <Switch checked={selectedSubject.rights.portability} />
                  </ListItemSecondaryAction>
                </ListItem>
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setRightsDialogOpen(false)}>
            Fechar
          </Button>
          <Button variant="contained">
            Atualizar Direitos
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default LGPDComplianceCenter;