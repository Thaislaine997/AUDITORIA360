import React, { useState } from 'react';
import {
  Box,
  Paper,
  Typography,
  Avatar,
  Chip,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Divider,
  Fade,
  Slide
} from '@mui/material';
import {
  Psychology,
  TrendingUp,
  MessageOutlined,
  Close,
  VideoCall,
  SmartToy
} from '@mui/icons-material';

// AI Consultant definitions based on the manifesto
interface AIConsultant {
  id: string;
  name: string;
  title: string;
  specialization: string;
  description: string;
  personality: string;
  color: string;
  avatar: string;
  icon: React.ReactNode;
  capabilities: string[];
}

const aiConsultants: AIConsultant[] = [
  {
    id: 'kairos',
    name: 'Kairós',
    title: 'Estrategista de Risco',
    specialization: 'Análise Preditiva e Gestão de Riscos',
    description: 'Avatar calmo e analítico especializado em identificação de riscos e previsão de cenários futuros.',
    personality: 'Analítico, metódico, visionário. Fala de forma pausada e precisa.',
    color: '#ff6b6b',
    avatar: '🎯',
    icon: <Psychology />,
    capabilities: [
      'Análise preditiva de churn de clientes',
      'Mapeamento de riscos de compliance',
      'Identificação de padrões críticos',
      'Projeção de cenários futuros',
      'Análise de vulnerabilidades'
    ]
  },
  {
    id: 'metis',
    name: 'Métis',
    title: 'Oráculo da Eficiência',
    specialization: 'Otimização de Processos e Automação',
    description: 'Avatar rápido e energético focado na maximização de eficiência operacional.',
    personality: 'Dinâmica, entusiasta, solucionadora. Fala com energia e propõe ações.',
    color: '#4ecdc4',
    avatar: '⚡',
    icon: <TrendingUp />,
    capabilities: [
      'Otimização de fluxos de trabalho',
      'Sugestões de automação',
      'Análise de gargalos',
      'Redesenho de processos',
      'Métricas de performance'
    ]
  },
  {
    id: 'hermes',
    name: 'Hermes',
    title: 'Emissário de Comunicação',
    specialization: 'Estratégias de Comunicação e Relacionamento',
    description: 'Especialista em linguagem e comunicação, criando campanhas personalizadas.',
    personality: 'Carismático, persuasivo, adaptável. Modula tom conforme o público.',
    color: '#45b7d1',
    avatar: '📢',
    icon: <MessageOutlined />,
    capabilities: [
      'Geração de campanhas de comunicação',
      'Personalização de mensagens',
      'Análise de tom e linguagem',
      'Estratégias de engajamento',
      'Templates de comunicação'
    ]
  }
];

interface ChronosAIPanteaoProps {
  open: boolean;
  onClose: () => void;
  onConsultantSelect?: (consultant: AIConsultant) => void;
}

const ChronosAIPanteao: React.FC<ChronosAIPanteaoProps> = ({
  open,
  onClose,
  onConsultantSelect
}) => {
  const [selectedConsultant, setSelectedConsultant] = useState<AIConsultant | null>(null);
  const [meetingMode, setMeetingMode] = useState(false);

  const handleConsultantClick = (consultant: AIConsultant) => {
    setSelectedConsultant(consultant);
    onConsultantSelect?.(consultant);
  };

  const startMeeting = () => {
    setMeetingMode(true);
  };

  return (
    <>
      {/* Main Panteão Dialog */}
      <Dialog
        open={open}
        onClose={onClose}
        maxWidth="lg"
        fullWidth
        PaperProps={{
          sx: {
            background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
            color: 'white',
            borderRadius: 3,
            minHeight: '600px'
          }
        }}
      >
        <DialogTitle sx={{ textAlign: 'center', pb: 1 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 2 }}>
            <SmartToy sx={{ fontSize: 40, color: '#4ecdc4' }} />
            <Typography variant="h4" sx={{ fontWeight: 'bold' }}>
              Panteão IA
            </Typography>
          </Box>
          <Typography variant="subtitle1" sx={{ opacity: 0.8, mt: 1 }}>
            Conselho de Consultores Digitais Especializados
          </Typography>
        </DialogTitle>

        <DialogContent>
          <Box sx={{ display: 'flex', gap: 3, height: '450px' }}>
            {/* Consultants List */}
            <Box sx={{ flex: 1 }}>
              <Typography variant="h6" gutterBottom sx={{ mb: 2 }}>
                Membros do Conselho
              </Typography>
              
              <List sx={{ p: 0 }}>
                {aiConsultants.map((consultant, index) => (
                  <Fade in key={consultant.id} timeout={300 + index * 200}>
                    <ListItem
                      sx={{
                        mb: 2,
                        bgcolor: selectedConsultant?.id === consultant.id 
                          ? 'rgba(255,255,255,0.1)' 
                          : 'rgba(255,255,255,0.05)',
                        borderRadius: 2,
                        cursor: 'pointer',
                        border: selectedConsultant?.id === consultant.id 
                          ? `2px solid ${consultant.color}` 
                          : '2px solid transparent',
                        transition: 'all 0.3s ease',
                        '&:hover': {
                          bgcolor: 'rgba(255,255,255,0.1)',
                          transform: 'scale(1.02)'
                        }
                      }}
                      onClick={() => handleConsultantClick(consultant)}
                    >
                      <ListItemAvatar>
                        <Avatar
                          sx={{
                            bgcolor: consultant.color,
                            fontSize: '1.5rem',
                            width: 56,
                            height: 56
                          }}
                        >
                          {consultant.avatar}
                        </Avatar>
                      </ListItemAvatar>
                      
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="h6" sx={{ color: consultant.color }}>
                              {consultant.name}
                            </Typography>
                            {consultant.icon}
                          </Box>
                        }
                        secondary={
                          <Box>
                            <Typography variant="body2" sx={{ color: 'white', opacity: 0.9 }}>
                              {consultant.title}
                            </Typography>
                            <Typography variant="caption" sx={{ opacity: 0.7 }}>
                              {consultant.specialization}
                            </Typography>
                          </Box>
                        }
                      />
                    </ListItem>
                  </Fade>
                ))}
              </List>
            </Box>

            <Divider orientation="vertical" flexItem sx={{ borderColor: 'rgba(255,255,255,0.2)' }} />

            {/* Consultant Details */}
            <Box sx={{ flex: 1.5, pl: 2 }}>
              {selectedConsultant ? (
                <Fade in>
                  <Box>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                      <Avatar
                        sx={{
                          bgcolor: selectedConsultant.color,
                          fontSize: '2rem',
                          width: 80,
                          height: 80
                        }}
                      >
                        {selectedConsultant.avatar}
                      </Avatar>
                      <Box>
                        <Typography variant="h4" sx={{ color: selectedConsultant.color }}>
                          {selectedConsultant.name}
                        </Typography>
                        <Typography variant="h6" sx={{ opacity: 0.8 }}>
                          {selectedConsultant.title}
                        </Typography>
                      </Box>
                    </Box>

                    <Typography variant="body1" paragraph sx={{ mb: 3 }}>
                      {selectedConsultant.description}
                    </Typography>

                    <Box sx={{ mb: 3 }}>
                      <Typography variant="h6" gutterBottom>
                        Personalidade
                      </Typography>
                      <Typography variant="body2" sx={{ opacity: 0.8, fontStyle: 'italic' }}>
                        {selectedConsultant.personality}
                      </Typography>
                    </Box>

                    <Box sx={{ mb: 3 }}>
                      <Typography variant="h6" gutterBottom>
                        Capacidades Especializadas
                      </Typography>
                      <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1, mt: 1 }}>
                        {selectedConsultant.capabilities.map((capability) => (
                          <Chip
                            key={capability}
                            label={capability}
                            size="small"
                            sx={{
                              bgcolor: `${selectedConsultant.color}20`,
                              color: selectedConsultant.color,
                              border: `1px solid ${selectedConsultant.color}40`
                            }}
                          />
                        ))}
                      </Box>
                    </Box>

                    <Box sx={{ display: 'flex', gap: 2, mt: 4 }}>
                      <Button
                        variant="contained"
                        startIcon={<MessageOutlined />}
                        sx={{
                          bgcolor: selectedConsultant.color,
                          '&:hover': { bgcolor: selectedConsultant.color + 'dd' }
                        }}
                      >
                        Consultar {selectedConsultant.name}
                      </Button>
                      <Button
                        variant="outlined"
                        startIcon={<VideoCall />}
                        onClick={startMeeting}
                        sx={{
                          borderColor: selectedConsultant.color,
                          color: selectedConsultant.color
                        }}
                      >
                        Sala de Reunião
                      </Button>
                    </Box>
                  </Box>
                </Fade>
              ) : (
                <Box
                  sx={{
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100%',
                    opacity: 0.5
                  }}
                >
                  <SmartToy sx={{ fontSize: 80, mb: 2 }} />
                  <Typography variant="h6" textAlign="center">
                    Selecione um consultor para ver detalhes
                  </Typography>
                  <Typography variant="body2" textAlign="center" sx={{ mt: 1 }}>
                    Clique em um dos membros do Panteão
                  </Typography>
                </Box>
              )}
            </Box>
          </Box>
        </DialogContent>

        <DialogActions sx={{ justifyContent: 'space-between', p: 3 }}>
          <Button
            onClick={startMeeting}
            variant="contained"
            startIcon={<VideoCall />}
            disabled={!selectedConsultant}
            sx={{
              bgcolor: '#4ecdc4',
              '&:hover': { bgcolor: '#45a29e' }
            }}
          >
            Iniciar Reunião Estratégica
          </Button>
          
          <Button
            onClick={onClose}
            startIcon={<Close />}
            sx={{ color: 'white' }}
          >
            Fechar Panteão
          </Button>
        </DialogActions>
      </Dialog>

      {/* Meeting Room Dialog */}
      <Dialog
        open={meetingMode}
        onClose={() => setMeetingMode(false)}
        maxWidth="xl"
        fullWidth
        PaperProps={{
          sx: {
            background: 'linear-gradient(135deg, #0f0f23 0%, #1a1a3e 100%)',
            color: 'white',
            minHeight: '80vh'
          }
        }}
      >
        <DialogTitle>
          <Typography variant="h5" sx={{ textAlign: 'center' }}>
            🏛️ Sala de Reunião Virtual - Debate Estratégico
          </Typography>
        </DialogTitle>
        
        <DialogContent>
          <Box sx={{ textAlign: 'center', py: 8 }}>
            <Typography variant="h6" gutterBottom>
              Funcionalidade em Desenvolvimento
            </Typography>
            <Typography variant="body1" sx={{ opacity: 0.7 }}>
              Em breve: Debate entre múltiplas IAs especializadas com visualização em tempo real
            </Typography>
          </Box>
        </DialogContent>
        
        <DialogActions>
          <Button onClick={() => setMeetingMode(false)}>
            Fechar
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default ChronosAIPanteao;