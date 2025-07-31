import React, { useState, useCallback } from 'react';
import {
  Box,
  Paper,
  Typography,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Chip,
  Grid,
  Card,
  CardContent,
  IconButton,
  Tooltip,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Avatar
} from '@mui/material';
import {
  Add,
  PlayArrow,
  Stop,
  Settings,
  Close,
  AccountTree,
  FlashOn,
  Message,
  Schedule,
  CheckCircle,
  Error,
  Build
} from '@mui/icons-material';

// Workflow node types
interface WorkflowNode {
  id: string;
  type: 'trigger' | 'condition' | 'action';
  title: string;
  description: string;
  icon: React.ReactNode;
  color: string;
  config?: any;
}

// Available workflow primitives
const workflowPrimitives: WorkflowNode[] = [
  // Triggers
  {
    id: 'whatsapp-message',
    type: 'trigger',
    title: 'Mensagem WhatsApp',
    description: 'Quando uma mensagem chegar no WhatsApp',
    icon: <Message />,
    color: '#25d366'
  },
  {
    id: 'schedule-trigger',
    type: 'trigger', 
    title: 'Agendamento',
    description: 'Em horário específico ou intervalo',
    icon: <Schedule />,
    color: '#2196f3'
  },
  {
    id: 'document-upload',
    type: 'trigger',
    title: 'Upload de Documento',
    description: 'Quando um documento for enviado',
    icon: <FlashOn />,
    color: '#ff9800'
  },
  
  // Conditions
  {
    id: 'contains-word',
    type: 'condition',
    title: 'Contém Palavra',
    description: 'Verificar se texto contém palavra específica',
    icon: <CheckCircle />,
    color: '#4caf50'
  },
  {
    id: 'client-type',
    type: 'condition',
    title: 'Tipo de Cliente',
    description: 'Verificar categoria do cliente',
    icon: <AccountTree />,
    color: '#9c27b0'
  },
  
  // Actions
  {
    id: 'create-demand',
    type: 'action',
    title: 'Criar Demanda',
    description: 'Criar nova demanda no sistema',
    icon: <Add />,
    color: '#f44336'
  },
  {
    id: 'assign-analyst',
    type: 'action',
    title: 'Atribuir Analista',
    description: 'Designar analista responsável',
    icon: <Build />,
    color: '#607d8b'
  },
  {
    id: 'call-ai-kairos',
    type: 'action',
    title: 'Convocar Kairós',
    description: 'Solicitar análise de risco inicial',
    icon: <FlashOn />,
    color: '#ff6b6b'
  }
];

// Sample workflow templates
const workflowTemplates = [
  {
    id: 'urgent-whatsapp',
    name: 'Urgência WhatsApp',
    description: 'Fluxo para mensagens urgentes no WhatsApp',
    nodes: ['whatsapp-message', 'contains-word', 'create-demand', 'assign-analyst']
  },
  {
    id: 'vip-onboarding',
    name: 'Onboarding VIP',
    description: 'Fluxo especial para clientes VIP',
    nodes: ['document-upload', 'client-type', 'call-ai-kairos', 'create-demand']
  }
];

interface ChronosWorkflowAltarProps {
  open: boolean;
  onClose: () => void;
}

const ChronosWorkflowAltar: React.FC<ChronosWorkflowAltarProps> = ({
  open,
  onClose
}) => {
  const [selectedNodes, setSelectedNodes] = useState<WorkflowNode[]>([]);
  const [isRunning, setIsRunning] = useState(false);

  const handleNodeAdd = useCallback((node: WorkflowNode) => {
    setSelectedNodes(prev => [...prev, { ...node, id: `${node.id}-${Date.now()}` }]);
  }, []);

  const handleNodeRemove = useCallback((nodeId: string) => {
    setSelectedNodes(prev => prev.filter(node => node.id !== nodeId));
  }, []);

  const handleTemplateApply = useCallback((template: typeof workflowTemplates[0]) => {
    const templateNodes = template.nodes.map(nodeId => {
      const primitive = workflowPrimitives.find(p => p.id === nodeId);
      return primitive ? { ...primitive, id: `${nodeId}-${Date.now()}` } : null;
    }).filter(Boolean) as WorkflowNode[];
    
    setSelectedNodes(templateNodes);
  }, []);

  const handleRunWorkflow = () => {
    setIsRunning(true);
    setTimeout(() => {
      setIsRunning(false);
      console.log('Workflow executed successfully!');
    }, 3000);
  };

  const getNodeTypeColor = (type: string) => {
    switch (type) {
      case 'trigger': return '#4caf50';
      case 'condition': return '#ff9800';
      case 'action': return '#f44336';
      default: return '#9e9e9e';
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="xl"
      fullWidth
      PaperProps={{
        sx: {
          background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
          color: 'white',
          minHeight: '80vh'
        }
      }}
    >
      <DialogTitle sx={{ textAlign: 'center', pb: 1 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2 }}>
          <AccountTree sx={{ fontSize: 40, color: '#4ecdc4' }} />
          <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
            ⚡ Altar da Automação
          </Typography>
        </Box>
        <Typography variant="subtitle1" sx={{ opacity: 0.8, mt: 1 }}>
          Sistema de Composição de Fluxos de Trabalho
        </Typography>
      </DialogTitle>

      <DialogContent>
        <Grid container spacing={3}>
          {/* Primitives Palette */}
          <Grid item xs={4}>
            <Paper sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.05)', height: 'fit-content' }}>
              <Typography variant="h6" gutterBottom>
                🔧 Primitivos Disponíveis
              </Typography>
              
              {['trigger', 'condition', 'action'].map(type => (
                <Box key={type} sx={{ mb: 3 }}>
                  <Typography 
                    variant="subtitle1" 
                    sx={{ 
                      color: getNodeTypeColor(type),
                      textTransform: 'capitalize',
                      mb: 1
                    }}
                  >
                    {type === 'trigger' ? '🚀 Gatilhos' : 
                     type === 'condition' ? '🔍 Condições' : '⚙️ Ações'}
                  </Typography>
                  
                  {workflowPrimitives
                    .filter(primitive => primitive.type === type)
                    .map(primitive => (
                    <Card 
                      key={primitive.id}
                      sx={{ 
                        mb: 1, 
                        bgcolor: 'rgba(255,255,255,0.05)',
                        cursor: 'pointer',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          bgcolor: 'rgba(255,255,255,0.1)',
                          transform: 'scale(1.02)'
                        }
                      }}
                      onClick={() => handleNodeAdd(primitive)}
                    >
                      <CardContent sx={{ p: 1.5 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Avatar 
                            sx={{ 
                              bgcolor: primitive.color, 
                              width: 32, 
                              height: 32 
                            }}
                          >
                            {primitive.icon}
                          </Avatar>
                          <Box>
                            <Typography variant="body2" sx={{ fontWeight: 'bold' }}>
                              {primitive.title}
                            </Typography>
                            <Typography variant="caption" sx={{ opacity: 0.7 }}>
                              {primitive.description}
                            </Typography>
                          </Box>
                        </Box>
                      </CardContent>
                    </Card>
                  ))}
                </Box>
              ))}
            </Paper>
          </Grid>

          {/* Workflow Canvas */}
          <Grid item xs={5}>
            <Paper sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.05)', minHeight: 400 }}>
              <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                <Typography variant="h6">
                  🎨 Canvas do Fluxo
                </Typography>
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <Button
                    variant="contained"
                    size="small"
                    onClick={handleRunWorkflow}
                    disabled={selectedNodes.length === 0 || isRunning}
                    startIcon={isRunning ? <Stop /> : <PlayArrow />}
                    sx={{
                      bgcolor: '#4caf50',
                      '&:hover': { bgcolor: '#45a049' }
                    }}
                  >
                    {isRunning ? 'Executando...' : 'Executar'}
                  </Button>
                  <Button
                    variant="outlined"
                    size="small"
                    onClick={() => setSelectedNodes([])}
                    sx={{ color: 'white', borderColor: 'white' }}
                  >
                    Limpar
                  </Button>
                </Box>
              </Box>

              {selectedNodes.length === 0 ? (
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: 300,
                    border: '2px dashed rgba(255,255,255,0.3)',
                    borderRadius: 2,
                    opacity: 0.5
                  }}
                >
                  <AccountTree sx={{ fontSize: 60, mb: 2 }} />
                  <Typography variant="h6">
                    Arraste primitivos para criar seu fluxo
                  </Typography>
                  <Typography variant="body2">
                    Comece com um gatilho, adicione condições e ações
                  </Typography>
                </Box>
              ) : (
                <Box>
                  {selectedNodes.map((node, index) => (
                    <Box key={node.id} sx={{ mb: 2 }}>
                      <Card
                        sx={{
                          bgcolor: `${node.color}20`,
                          border: `2px solid ${node.color}`,
                          position: 'relative'
                        }}
                      >
                        <CardContent sx={{ p: 2 }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
                            <Avatar sx={{ bgcolor: node.color }}>
                              {node.icon}
                            </Avatar>
                            <Box sx={{ flex: 1 }}>
                              <Typography variant="subtitle1" sx={{ fontWeight: 'bold' }}>
                                {index + 1}. {node.title}
                              </Typography>
                              <Typography variant="body2" sx={{ opacity: 0.8 }}>
                                {node.description}
                              </Typography>
                            </Box>
                            <IconButton
                              size="small"
                              onClick={() => handleNodeRemove(node.id)}
                              sx={{ color: 'white' }}
                            >
                              <Close />
                            </IconButton>
                          </Box>
                        </CardContent>
                      </Card>
                      
                      {index < selectedNodes.length - 1 && (
                        <Box sx={{ display: 'flex', justifyContent: 'center', my: 1 }}>
                          <Box
                            sx={{
                              width: 2,
                              height: 20,
                              bgcolor: '#4ecdc4',
                              position: 'relative',
                              '&::after': {
                                content: '""',
                                position: 'absolute',
                                bottom: -5,
                                left: -3,
                                width: 8,
                                height: 8,
                                bgcolor: '#4ecdc4',
                                borderRadius: '50%'
                              }
                            }}
                          />
                        </Box>
                      )}
                    </Box>
                  ))}
                </Box>
              )}
            </Paper>
          </Grid>

          {/* Templates */}
          <Grid item xs={3}>
            <Paper sx={{ p: 2, bgcolor: 'rgba(255,255,255,0.05)' }}>
              <Typography variant="h6" gutterBottom>
                📋 Templates Prontos
              </Typography>
              
              {workflowTemplates.map(template => (
                <Card
                  key={template.id}
                  sx={{
                    mb: 2,
                    bgcolor: 'rgba(255,255,255,0.05)',
                    cursor: 'pointer',
                    transition: 'all 0.3s ease',
                    '&:hover': {
                      bgcolor: 'rgba(255,255,255,0.1)',
                      transform: 'scale(1.02)'
                    }
                  }}
                  onClick={() => handleTemplateApply(template)}
                >
                  <CardContent>
                    <Typography variant="subtitle1" sx={{ fontWeight: 'bold', mb: 1 }}>
                      {template.name}
                    </Typography>
                    <Typography variant="body2" sx={{ opacity: 0.8, mb: 2 }}>
                      {template.description}
                    </Typography>
                    <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                      {template.nodes.map((nodeId, index) => (
                        <Chip
                          key={`${nodeId}-${index}`}
                          label={`${index + 1}`}
                          size="small"
                          sx={{
                            bgcolor: getNodeTypeColor(
                              workflowPrimitives.find(p => p.id === nodeId)?.type || 'action'
                            ),
                            color: 'white',
                            fontSize: '0.7rem'
                          }}
                        />
                      ))}
                    </Box>
                  </CardContent>
                </Card>
              ))}

              <Divider sx={{ my: 2, borderColor: 'rgba(255,255,255,0.2)' }} />
              
              <Typography variant="h6" gutterBottom>
                🎯 Status da Execução
              </Typography>
              
              {isRunning && (
                <Box sx={{ textAlign: 'center', py: 2 }}>
                  <Box
                    sx={{
                      width: 40,
                      height: 40,
                      border: '4px solid rgba(76, 175, 80, 0.3)',
                      borderTop: '4px solid #4caf50',
                      borderRadius: '50%',
                      animation: 'spin 1s linear infinite',
                      margin: '0 auto 1rem',
                      '@keyframes spin': {
                        '0%': { transform: 'rotate(0deg)' },
                        '100%': { transform: 'rotate(360deg)' }
                      }
                    }}
                  />
                  <Typography variant="body2">
                    Executando fluxo de trabalho...
                  </Typography>
                </Box>
              )}
            </Paper>
          </Grid>
        </Grid>
      </DialogContent>

      <DialogActions sx={{ justifyContent: 'space-between', p: 3 }}>
        <Button
          variant="contained"
          startIcon={<Build />}
          disabled={selectedNodes.length === 0}
          sx={{
            bgcolor: '#4ecdc4',
            '&:hover': { bgcolor: '#45a29e' }
          }}
        >
          Salvar como Aplicação
        </Button>
        
        <Button
          onClick={onClose}
          startIcon={<Close />}
          sx={{ color: 'white' }}
        >
          Fechar Altar
        </Button>
      </DialogActions>
    </Dialog>
  );
};

export default ChronosWorkflowAltar;