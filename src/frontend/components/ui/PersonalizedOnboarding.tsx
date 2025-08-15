import React, { useState, useEffect } from 'react';
import {
  Box,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Button,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Chip,
  Avatar,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  VideoFrame,
} from '@mui/material';
import {
  CheckCircle,
  RadioButtonUnchecked,
  Star,
  TrendingUp,
  Settings,
  Group,
} from '@mui/icons-material';
import { useAuthStore } from '../../stores/authStore';

interface OnboardingMission {
  id: number;
  name: string;
  description: string;
  instructions: string;
  xpReward: number;
  badgeReward?: string;
  isCompleted: boolean;
  videoUrl?: string;
  actionButton?: {
    text: string;
    action: () => void;
  };
}

interface OnboardingProps {
  userProfile: 'gestor' | 'analista';
  onComplete: () => void;
}

const PersonalizedOnboarding: React.FC<OnboardingProps> = ({ userProfile, onComplete }) => {
  const { user } = useAuthStore();
  const [activeStep, setActiveStep] = useState(0);
  const [videoDialogOpen, setVideoDialogOpen] = useState(false);
  const [currentVideoUrl, setCurrentVideoUrl] = useState('');
  const [totalXP, setTotalXP] = useState(0);

  // Missions customized by user profile
  const gestorMissions: OnboardingMission[] = [
    {
      id: 1,
      name: 'Configure seu primeiro cliente',
      description: 'Aprenda a cadastrar e configurar um cliente no sistema',
      instructions: 'Clique no botão "Cadastrar Cliente" e preencha as informações básicas. O sistema irá guiá-lo através do processo.',
      xpReward: 100,
      badgeReward: 'Primeiro Cliente',
      isCompleted: false,
      videoUrl: '/videos/gestor-cadastro-cliente.mp4',
      actionButton: {
        text: 'Cadastrar primeiro cliente',
        action: () => {
          // Navigate to client registration
          window.location.href = '/clients/new';
        }
      }
    },
    {
      id: 2,
      name: 'Configure a automação de envios',
      description: 'Configure o envio automático de documentos para seu cliente',
      instructions: 'Acesse a configuração do cliente e defina os documentos que devem ser enviados automaticamente e os canais de envio (Email, WhatsApp).',
      xpReward: 250,
      badgeReward: 'Mestre da Configuração',
      isCompleted: false,
      videoUrl: '/videos/gestor-automacao-envios.mp4'
    },
    {
      id: 3,
      name: 'Convide sua equipe',
      description: 'Adicione analistas à sua equipe para colaboração',
      instructions: 'Use a área de gerenciamento de usuários para convidar analistas e definir suas permissões.',
      xpReward: 150,
      badgeReward: 'Líder de Equipe',
      isCompleted: false,
      videoUrl: '/videos/gestor-gestao-equipe.mp4'
    },
    {
      id: 4,
      name: 'Explore o Dashboard Executivo',
      description: 'Conheça as métricas e indicadores disponíveis',
      instructions: 'Navegue pelo dashboard e personalize os widgets de acordo com suas necessidades de gestão.',
      xpReward: 100,
      isCompleted: false,
      videoUrl: '/videos/gestor-dashboard.mp4'
    }
  ];

  const analistaMissions: OnboardingMission[] = [
    {
      id: 1,
      name: 'Faça seu primeiro envio',
      description: 'Aprenda a enviar documentos para um cliente',
      instructions: 'Selecione um cliente e use a funcionalidade de envio para mandar documentos via email ou WhatsApp.',
      xpReward: 100,
      badgeReward: 'Primeiro Envio',
      isCompleted: false,
      videoUrl: '/videos/analista-primeiro-envio.mp4'
    },
    {
      id: 2,
      name: 'Configure destinatários',
      description: 'Adicione novos destinatários para um cliente',
      instructions: 'Acesse a configuração do cliente e adicione contatos que devem receber os documentos.',
      xpReward: 150,
      badgeReward: 'Organizador',
      isCompleted: false,
      videoUrl: '/videos/analista-destinatarios.mp4'
    },
    {
      id: 3,
      name: 'Use os templates de configuração',
      description: 'Aprenda a usar templates para agilizar configurações',
      instructions: 'Explore os templates disponíveis e aplique um template adequado ao perfil do cliente.',
      xpReward: 200,
      badgeReward: 'Eficiência',
      isCompleted: false,
      videoUrl: '/videos/analista-templates.mp4'
    },
    {
      id: 4,
      name: 'Monitore os envios',
      description: 'Acompanhe o status dos envios e resolva problemas',
      instructions: 'Use a área de logs para monitorar envios e identificar possíveis falhas.',
      xpReward: 100,
      isCompleted: false,
      videoUrl: '/videos/analista-monitoramento.mp4'
    }
  ];

  const missions = userProfile === 'gestor' ? gestorMissions : analistaMissions;

  const handleNext = () => {
    setActiveStep((prevActiveStep) => prevActiveStep + 1);
  };

  const handleBack = () => {
    setActiveStep((prevActiveStep) => prevActiveStep - 1);
  };

  const handleMissionComplete = (missionId: number) => {
    const mission = missions.find(m => m.id === missionId);
    if (mission && !mission.isCompleted) {
      mission.isCompleted = true;
      setTotalXP(totalXP + mission.xpReward);
      
      // TODO: Call API to update mission completion
      // await missionService.completeMission(missionId, mission.xpReward);
      
      if (activeStep < missions.length - 1) {
        handleNext();
      } else {
        onComplete();
      }
    }
  };

  const openVideo = (videoUrl: string) => {
    setCurrentVideoUrl(videoUrl);
    setVideoDialogOpen(true);
  };

  const getProfileIcon = () => {
    if (userProfile === 'gestor') {
      return <Group color="primary" />;
    }
    return <TrendingUp color="secondary" />;
  };

  const getProfileTitle = () => {
    if (userProfile === 'gestor') {
      return 'Onboarding para Gestores';
    }
    return 'Onboarding para Analistas';
  };

  const getWelcomeMessage = () => {
    if (userProfile === 'gestor') {
      return 'Como gestor, você terá acesso a ferramentas de administração, relatórios executivos e gerenciamento de equipe.';
    }
    return 'Como analista, você focará nas operações diárias, configuração de clientes e monitoramento de envios.';
  };

  return (
    <Box sx={{ maxWidth: 800, mx: 'auto', p: 3 }}>
      {/* Header */}
      <Card sx={{ mb: 3 }}>
        <CardContent>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
              {getProfileIcon()}
            </Avatar>
            <Box>
              <Typography variant="h5" component="h1">
                {getProfileTitle()}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Bem-vindo(a), {user?.full_name}!
              </Typography>
            </Box>
          </Box>
          
          <Typography variant="body1" paragraph>
            {getWelcomeMessage()}
          </Typography>
          
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Chip 
              icon={<Star />} 
              label={`${totalXP} XP Ganhos`} 
              color="primary" 
              variant="outlined"
            />
            <Chip 
              label={`${missions.filter(m => m.isCompleted).length}/${missions.length} Missões`}
              color="success"
              variant="outlined"
            />
          </Box>
        </CardContent>
      </Card>

      {/* Progress */}
      <Box sx={{ mb: 3 }}>
        <Typography variant="h6" gutterBottom>
          Progresso do Onboarding
        </Typography>
        <LinearProgress 
          variant="determinate" 
          value={(missions.filter(m => m.isCompleted).length / missions.length) * 100}
          sx={{ height: 8, borderRadius: 4 }}
        />
      </Box>

      {/* Missions Stepper */}
      <Stepper activeStep={activeStep} orientation="vertical">
        {missions.map((mission, index) => (
          <Step key={mission.id} completed={mission.isCompleted}>
            <StepLabel 
              optional={
                mission.isCompleted ? (
                  <Chip 
                    icon={<CheckCircle />} 
                    label={`+${mission.xpReward} XP`} 
                    size="small" 
                    color="success"
                  />
                ) : (
                  <Chip 
                    icon={<RadioButtonUnchecked />} 
                    label={`${mission.xpReward} XP`} 
                    size="small" 
                    variant="outlined"
                  />
                )
              }
            >
              <Typography variant="h6">{mission.name}</Typography>
            </StepLabel>
            
            <StepContent>
              <Card variant="outlined" sx={{ p: 2, mb: 2 }}>
                <Typography variant="body1" paragraph>
                  {mission.description}
                </Typography>
                
                <Typography variant="body2" color="text.secondary" paragraph>
                  {mission.instructions}
                </Typography>
                
                <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                  {mission.videoUrl && (
                    <Button
                      variant="outlined"
                      size="small"
                      onClick={() => openVideo(mission.videoUrl!)}
                    >
                      Ver Vídeo Tutorial
                    </Button>
                  )}
                  
                  {mission.actionButton && (
                    <Button
                      variant="contained"
                      size="small"
                      onClick={mission.actionButton.action}
                    >
                      {mission.actionButton.text}
                    </Button>
                  )}
                  
                  <Button
                    variant="contained"
                    color="success"
                    size="small"
                    onClick={() => handleMissionComplete(mission.id)}
                    disabled={mission.isCompleted}
                  >
                    {mission.isCompleted ? 'Concluída' : 'Marcar como Concluída'}
                  </Button>
                </Box>
                
                {mission.badgeReward && (
                  <Box sx={{ mt: 2 }}>
                    <Chip 
                      label={`Badge: ${mission.badgeReward}`}
                      color="warning"
                      variant="outlined"
                      size="small"
                    />
                  </Box>
                )}
              </Card>
              
              <Box sx={{ mb: 1 }}>
                <Button
                  disabled={index === 0}
                  onClick={handleBack}
                  sx={{ mt: 1, mr: 1 }}
                >
                  Anterior
                </Button>
                <Button
                  variant="contained"
                  onClick={handleNext}
                  sx={{ mt: 1, mr: 1 }}
                  disabled={index === missions.length - 1}
                >
                  Próxima
                </Button>
              </Box>
            </StepContent>
          </Step>
        ))}
      </Stepper>

      {/* Completion */}
      {missions.every(m => m.isCompleted) && (
        <Card sx={{ mt: 3, textAlign: 'center' }}>
          <CardContent>
            <Typography variant="h4" color="success.main" gutterBottom>
              🎉 Parabéns!
            </Typography>
            <Typography variant="h6" gutterBottom>
              Você completou o onboarding!
            </Typography>
            <Typography variant="body1" paragraph>
              Total de XP ganho: <strong>{totalXP} XP</strong>
            </Typography>
            <Button
              variant="contained"
              size="large"
              onClick={onComplete}
            >
              Começar a usar o sistema
            </Button>
          </CardContent>
        </Card>
      )}

      {/* Video Dialog */}
      <Dialog
        open={videoDialogOpen}
        onClose={() => setVideoDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Vídeo Tutorial</DialogTitle>
        <DialogContent>
          {currentVideoUrl && (
            <Box sx={{ position: 'relative', paddingTop: '56.25%' }}>
              <video
                controls
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                }}
              >
                <source src={currentVideoUrl} type="video/mp4" />
                Seu navegador não suporta o elemento de vídeo.
              </video>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setVideoDialogOpen(false)}>
            Fechar
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default PersonalizedOnboarding;