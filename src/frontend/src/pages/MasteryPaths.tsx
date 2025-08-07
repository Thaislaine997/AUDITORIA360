import React, { useState, useEffect } from 'react';
import {
  Container,
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  LinearProgress,
  Chip,
  Button,
  Avatar,
  Stepper,
  Step,
  StepLabel,
  StepContent,
  Paper,
  Alert,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import {
  School,
  EmojiEvents,
  TrendingUp,
  CheckCircle,
  Lock,
  Star,
  Psychology,
  Security,
  Assessment,
  Timeline,
  Close,
  PlayArrow,
  Quiz,
} from '@mui/icons-material';

/**
 * MasteryPaths - Gamificação 2.0: Caminhos de Mestria
 * 
 * Sistema de engajamento focado no desenvolvimento de competências e motivação intrínseca.
 * Implementa caminhos de aprendizagem estruturados com desafios e reconhecimento.
 * 
 * Parte da Grande Síntese: Initiative III - Product Intelligence Evolution
 */

interface MasteryPath {
  id: string;
  name: string;
  description: string;
  icon: React.ReactNode;
  color: string;
  totalSteps: number;
  completedSteps: number;
  estimatedTime: string;
  difficulty: 'Iniciante' | 'Intermédio' | 'Avançado' | 'Especialista';
  rewards: string[];
  prerequisites?: string[];
  locked?: boolean;
}

interface Challenge {
  id: string;
  title: string;
  description: string;
  type: 'practical' | 'quiz' | 'analysis' | 'creation';
  points: number;
  timeEstimate: string;
  completed: boolean;
  tools: string[];
}

const MasteryPaths: React.FC = () => {
  const [paths, setPaths] = useState<MasteryPath[]>([]);
  const [selectedPath, setSelectedPath] = useState<MasteryPath | null>(null);
  const [challenges, setChallenges] = useState<Challenge[]>([]);
  const [showChallengeDialog, setShowChallengeDialog] = useState(false);
  const [currentChallenge, setCurrentChallenge] = useState<Challenge | null>(null);
  const [userProgress, setUserProgress] = useState({
    totalPoints: 1250,
    level: 'Auditor Intermédio',
    streak: 7,
    achievements: ['Primeiro Relatório', 'Mestre da Conformidade', 'Analista Experiente']
  });

  useEffect(() => {
    // Initialize mastery paths
    const initialPaths: MasteryPath[] = [
      {
        id: 'compliance_master',
        name: 'Mestre da Conformidade',
        description: 'Domine as técnicas de auditoria de conformidade e análise de riscos regulamentares.',
        icon: <Security />,
        color: '#10B981',
        totalSteps: 8,
        completedSteps: 3,
        estimatedTime: '4-6 semanas',
        difficulty: 'Intermédio',
        rewards: ['Badge Mestre da Conformidade', '+500 pontos', 'Acesso a relatórios avançados'],
        prerequisites: ['Conhecimentos básicos de auditoria']
      },
      {
        id: 'ai_consultant_expert',
        name: 'Especialista em Consultor IA',
        description: 'Torne-se um especialista na utilização da IA para análise de riscos e recomendações.',
        icon: <Psychology />,
        color: '#0077FF',
        totalSteps: 6,
        completedSteps: 1,
        estimatedTime: '3-4 semanas',
        difficulty: 'Avançado',
        rewards: ['Badge IA Expert', '+750 pontos', 'Acesso a modelos IA avançados'],
        prerequisites: ['Mestre da Conformidade']
      },
      {
        id: 'analytics_wizard',
        name: 'Mago da Analítica',
        description: 'Desenvolva competências avançadas em análise de dados e criação de relatórios insights.',
        icon: <Assessment />,
        color: '#F59E0B',
        totalSteps: 10,
        completedSteps: 0,
        estimatedTime: '6-8 semanas',
        difficulty: 'Especialista',
        rewards: ['Badge Mago Analítico', '+1000 pontos', 'Ferramentas de análise exclusivas'],
        prerequisites: ['Mestre da Conformidade', 'Especialista em Consultor IA'],
        locked: true
      },
      {
        id: 'payroll_ninja',
        name: 'Ninja da Folha de Pagamento',
        description: 'Expertise completa em processamento de folhas de pagamento e conformidade trabalhista.',
        icon: <Timeline />,
        color: '#8B5CF6',
        totalSteps: 7,
        completedSteps: 5,
        estimatedTime: '3-5 semanas',
        difficulty: 'Intermédio',
        rewards: ['Badge Ninja Payroll', '+600 pontos', 'Calculadora avançada de folhas']
      }
    ];

    setPaths(initialPaths);
    setSelectedPath(initialPaths[0]);
    loadChallenges(initialPaths[0].id);
  }, []);

  const loadChallenges = (pathId: string) => {
    // Mock challenges based on selected path
    const challengesByPath: Record<string, Challenge[]> = {
      compliance_master: [
        {
          id: 'c1',
          title: 'Criar Checklist de Conformidade',
          description: 'Use as ferramentas de auditoria para criar um checklist personalizado de conformidade.',
          type: 'creation',
          points: 150,
          timeEstimate: '30 min',
          completed: true,
          tools: ['Audit Templates', 'Risk Assessment']
        },
        {
          id: 'c2',
          title: 'Identificar Riscos Regulamentares',
          description: 'Analise um cenário empresarial e identifique os principais riscos de conformidade.',
          type: 'analysis',
          points: 200,
          timeEstimate: '45 min',
          completed: true,
          tools: ['Risk Consultant AI', 'Regulatory Database']
        },
        {
          id: 'c3',
          title: 'Quiz: Normas de Auditoria',
          description: 'Teste seus conhecimentos sobre as principais normas e regulamentações.',
          type: 'quiz',
          points: 100,
          timeEstimate: '15 min',
          completed: true,
          tools: ['Knowledge Base']
        },
        {
          id: 'c4',
          title: 'Relatório de Auditoria Completo',
          description: 'Crie um relatório completo de auditoria usando dados reais simulados.',
          type: 'practical',
          points: 300,
          timeEstimate: '2 horas',
          completed: false,
          tools: ['Report Builder', 'Data Analytics', 'Risk Consultant AI']
        }
      ],
      ai_consultant_expert: [
        {
          id: 'ai1',
          title: 'Otimizar Prompts de IA',
          description: 'Aprenda a criar prompts eficazes para o Consultor de Riscos.',
          type: 'practical',
          points: 200,
          timeEstimate: '45 min',
          completed: true,
          tools: ['AI Consultant', 'Prompt Library']
        },
        {
          id: 'ai2',
          title: 'Interpretar Análises de Confiança',
          description: 'Compreenda e interprete os níveis de confiança das recomendações da IA.',
          type: 'analysis',
          points: 250,
          timeEstimate: '60 min',
          completed: false,
          tools: ['AI Consultant', 'Confidence Metrics']
        }
      ]
    };

    setChallenges(challengesByPath[pathId] || []);
  };

  const handleStartChallenge = (challenge: Challenge) => {
    setCurrentChallenge(challenge);
    setShowChallengeDialog(true);
  };

  const handleCompleteChallenge = () => {
    if (currentChallenge) {
      setChallenges(prev => 
        prev.map(c => 
          c.id === currentChallenge.id ? { ...c, completed: true } : c
        )
      );
      
      // Update user progress
      setUserProgress(prev => ({
        ...prev,
        totalPoints: prev.totalPoints + currentChallenge.points,
        streak: prev.streak + 1
      }));
      
      // Update path progress
      if (selectedPath) {
        setPaths(prev => 
          prev.map(p => 
            p.id === selectedPath.id 
              ? { ...p, completedSteps: p.completedSteps + 1 }
              : p
          )
        );
        
        setSelectedPath(prev => prev ? {
          ...prev,
          completedSteps: prev.completedSteps + 1
        } : null);
      }
    }
    
    setShowChallengeDialog(false);
    setCurrentChallenge(null);
  };

  const getProgressPercentage = (path: MasteryPath) => {
    return (path.completedSteps / path.totalSteps) * 100;
  };

  const getDifficultyColor = (difficulty: MasteryPath['difficulty']) => {
    switch (difficulty) {
      case 'Iniciante': return '#10B981';
      case 'Intermédio': return '#F59E0B';
      case 'Avançado': return '#EF4444';
      case 'Especialista': return '#8B5CF6';
      default: return '#6B7280';
    }
  };

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      {/* Header with user progress */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h3" gutterBottom sx={{ fontWeight: 'bold' }}>
          🎓 Caminhos de Mestria
        </Typography>
        <Typography variant="h6" color="text.secondary" paragraph>
          Desenvolva suas competências através de desafios estruturados e reconhecimento de conquistas.
        </Typography>
        
        {/* User Progress Card */}
        <Card sx={{ mb: 4, background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
          <CardContent>
            <Grid container alignItems="center" spacing={3}>
              <Grid item>
                <Avatar sx={{ width: 64, height: 64, bgcolor: 'rgba(255,255,255,0.2)' }}>
                  <EmojiEvents sx={{ fontSize: 32 }} />
                </Avatar>
              </Grid>
              <Grid item xs>
                <Typography variant="h5" gutterBottom>
                  {userProgress.level}
                </Typography>
                <Typography variant="body1" sx={{ opacity: 0.9 }}>
                  {userProgress.totalPoints} pontos • {userProgress.streak} dias consecutivos
                </Typography>
                <Box sx={{ display: 'flex', gap: 1, mt: 1, flexWrap: 'wrap' }}>
                  {userProgress.achievements.map((achievement, index) => (
                    <Chip 
                      key={index}
                      label={achievement} 
                      size="small" 
                      sx={{ bgcolor: 'rgba(255,255,255,0.2)', color: 'white' }}
                      icon={<Star sx={{ color: 'gold !important' }} />}
                    />
                  ))}
                </Box>
              </Grid>
            </Grid>
          </CardContent>
        </Card>
      </Box>

      <Grid container spacing={4}>
        {/* Mastery Paths List */}
        <Grid item xs={12} md={6}>
          <Typography variant="h5" gutterBottom>
            Caminhos Disponíveis
          </Typography>
          
          {paths.map((path) => (
            <Card 
              key={path.id}
              sx={{ 
                mb: 2, 
                cursor: path.locked ? 'not-allowed' : 'pointer',
                opacity: path.locked ? 0.6 : 1,
                border: selectedPath?.id === path.id ? `2px solid ${path.color}` : 'none',
                '&:hover': {
                  boxShadow: path.locked ? 'none' : '0 8px 25px rgba(0,0,0,0.15)',
                  transform: path.locked ? 'none' : 'translateY(-2px)'
                },
                transition: 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)'
              }}
              onClick={() => {
                if (!path.locked) {
                  setSelectedPath(path);
                  loadChallenges(path.id);
                }
              }}
            >
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'flex-start', gap: 2 }}>
                  <Avatar sx={{ bgcolor: path.color }}>
                    {path.locked ? <Lock /> : path.icon}
                  </Avatar>
                  <Box flex={1}>
                    <Typography variant="h6" gutterBottom>
                      {path.name}
                      {path.locked && <Lock sx={{ ml: 1, fontSize: 16, opacity: 0.6 }} />}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {path.description}
                    </Typography>
                    
                    <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                      <Chip 
                        label={path.difficulty} 
                        size="small" 
                        sx={{ bgcolor: getDifficultyColor(path.difficulty), color: 'white' }}
                      />
                      <Chip label={path.estimatedTime} size="small" variant="outlined" />
                    </Box>
                    
                    {!path.locked && (
                      <>
                        <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                          <Typography variant="body2" sx={{ mr: 1 }}>
                            Progresso:
                          </Typography>
                          <LinearProgress 
                            variant="determinate" 
                            value={getProgressPercentage(path)}
                            sx={{ 
                              flex: 1, 
                              mr: 1,
                              '& .MuiLinearProgress-bar': { bgcolor: path.color }
                            }}
                          />
                          <Typography variant="body2" fontWeight="bold">
                            {path.completedSteps}/{path.totalSteps}
                          </Typography>
                        </Box>
                        
                        <Typography variant="caption" color="text.secondary">
                          Recompensas: {path.rewards.join(', ')}
                        </Typography>
                      </>
                    )}
                    
                    {path.prerequisites && (
                      <Alert severity="info" sx={{ mt: 2 }}>
                        <Typography variant="caption">
                          Pré-requisitos: {path.prerequisites.join(', ')}
                        </Typography>
                      </Alert>
                    )}
                  </Box>
                </Box>
              </CardContent>
            </Card>
          ))}
        </Grid>

        {/* Selected Path Challenges */}
        <Grid item xs={12} md={6}>
          {selectedPath && (
            <>
              <Typography variant="h5" gutterBottom>
                {selectedPath.name} - Desafios
              </Typography>
              
              <Stepper orientation="vertical">
                {challenges.map((challenge, index) => (
                  <Step key={challenge.id} active={true}>
                    <StepLabel 
                      StepIconComponent={() => (
                        <Avatar 
                          sx={{ 
                            width: 32, 
                            height: 32, 
                            bgcolor: challenge.completed ? '#10B981' : '#6B7280' 
                          }}
                        >
                          {challenge.completed ? (
                            <CheckCircle sx={{ fontSize: 20 }} />
                          ) : (
                            <Typography variant="caption">{index + 1}</Typography>
                          )}
                        </Avatar>
                      )}
                    >
                      <Typography variant="h6">
                        {challenge.title}
                        <Chip 
                          label={`${challenge.points} pts`} 
                          size="small" 
                          sx={{ ml: 1, bgcolor: selectedPath.color, color: 'white' }}
                        />
                      </Typography>
                    </StepLabel>
                    <StepContent>
                      <Typography variant="body2" paragraph>
                        {challenge.description}
                      </Typography>
                      
                      <Box sx={{ display: 'flex', gap: 1, mb: 2, flexWrap: 'wrap' }}>
                        <Chip 
                          label={challenge.type === 'quiz' ? 'Quiz' : challenge.type === 'practical' ? 'Prático' : challenge.type === 'analysis' ? 'Análise' : 'Criação'}
                          size="small" 
                          icon={challenge.type === 'quiz' ? <Quiz /> : <PlayArrow />}
                        />
                        <Chip label={challenge.timeEstimate} size="small" variant="outlined" />
                      </Box>
                      
                      <Typography variant="caption" color="text.secondary" display="block" sx={{ mb: 2 }}>
                        Ferramentas: {challenge.tools.join(', ')}
                      </Typography>
                      
                      {!challenge.completed ? (
                        <Button 
                          variant="contained" 
                          startIcon={<PlayArrow />}
                          sx={{ bgcolor: selectedPath.color }}
                          onClick={() => handleStartChallenge(challenge)}
                        >
                          Iniciar Desafio
                        </Button>
                      ) : (
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <CheckCircle sx={{ color: '#10B981' }} />
                          <Typography variant="body2" sx={{ color: '#10B981', fontWeight: 'bold' }}>
                            Concluído! +{challenge.points} pontos
                          </Typography>
                        </Box>
                      )}
                    </StepContent>
                  </Step>
                ))}
              </Stepper>
            </>
          )}
        </Grid>
      </Grid>

      {/* Challenge Dialog */}
      <Dialog 
        open={showChallengeDialog} 
        onClose={() => setShowChallengeDialog(false)}
        maxWidth="sm"
        fullWidth
      >
        <DialogTitle sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="h6">
            {currentChallenge?.title}
          </Typography>
          <IconButton onClick={() => setShowChallengeDialog(false)}>
            <Close />
          </IconButton>
        </DialogTitle>
        
        <DialogContent>
          <Typography variant="body1" paragraph>
            {currentChallenge?.description}
          </Typography>
          
          <Alert severity="info" sx={{ mb: 2 }}>
            Este é um desafio simulado. Em uma implementação completa, aqui seria apresentado o 
            conteúdo interativo específico do desafio, como interfaces de quiz, simuladores de 
            auditoria, ou ferramentas de análise.
          </Alert>
          
          <Typography variant="body2" color="text.secondary">
            Pontos a ganhar: {currentChallenge?.points} • 
            Tempo estimado: {currentChallenge?.timeEstimate}
          </Typography>
        </DialogContent>
        
        <DialogActions>
          <Button onClick={() => setShowChallengeDialog(false)}>
            Cancelar
          </Button>
          <Button 
            variant="contained" 
            onClick={handleCompleteChallenge}
            startIcon={<CheckCircle />}
          >
            Marcar como Concluído
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default MasteryPaths;