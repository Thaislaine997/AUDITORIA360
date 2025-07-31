import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  LinearProgress,
  Grid,
  Avatar,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  IconButton,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Tooltip,
  Badge,
  Divider,
  Button,
} from '@mui/material';
import {
  Star,
  Close,
  EmojiEvents,
  TrendingUp,
  WhatsApp,
  Settings,
  Group,
  Speed,
  Security,
  CheckCircle,
  AutoAwesome,
} from '@mui/icons-material';
import { useAuthStore } from '../../stores/authStore';

interface Achievement {
  id: number;
  name: string;
  description: string;
  icon: string;
  badgeClass: string;
  xpReward: number;
  isUnlocked: boolean;
  unlockedAt?: Date;
  progress?: number;
  maxProgress?: number;
}

interface Skill {
  id: number;
  name: string;
  description: string;
  icon: string;
  category: string;
  currentProgress: number;
  requiredActions: number;
  isUnlocked: boolean;
  unlockedAt?: Date;
}

interface GamificationData {
  currentXP: number;
  currentLevel: number;
  xpToNextLevel: number;
  totalMissionsCompleted: number;
  achievements: Achievement[];
  skills: Skill[];
  recentActivity: {
    action: string;
    xpGained: number;
    timestamp: Date;
  }[];
}

const GamificationSystem: React.FC = () => {
  const { user } = useAuthStore();
  const [achievementDialogOpen, setAchievementDialogOpen] = useState(false);
  const [skillTreeDialogOpen, setSkillTreeDialogOpen] = useState(false);
  const [gamificationData, setGamificationData] = useState<GamificationData>({
    currentXP: 1250,
    currentLevel: 3,
    xpToNextLevel: 750,
    totalMissionsCompleted: 8,
    achievements: [
      {
        id: 1,
        name: 'Primeiro Cliente',
        description: 'Cadastrou seu primeiro cliente no sistema',
        icon: 'first_client',
        badgeClass: 'bronze',
        xpReward: 100,
        isUnlocked: true,
        unlockedAt: new Date('2024-01-15'),
      },
      {
        id: 2,
        name: 'Mestre da Configuração',
        description: 'Completou uma configuração completa de envio',
        icon: 'configuration_master',
        badgeClass: 'silver',
        xpReward: 250,
        isUnlocked: true,
        unlockedAt: new Date('2024-01-16'),
      },
      {
        id: 3,
        name: 'Invencível',
        description: '1.000 envios sem nenhuma falha!',
        icon: 'invincible',
        badgeClass: 'gold',
        xpReward: 500,
        isUnlocked: false,
        progress: 847,
        maxProgress: 1000,
      },
      {
        id: 4,
        name: 'Expansão Rápida',
        description: '10 novos clientes cadastrados em uma semana!',
        icon: 'rapid_expansion',
        badgeClass: 'platinum',
        xpReward: 750,
        isUnlocked: false,
        progress: 7,
        maxProgress: 10,
      },
    ],
    skills: [
      {
        id: 1,
        name: 'Especialista em WhatsApp',
        description: 'Configurou 50+ clientes com envio via WhatsApp',
        icon: 'whatsapp_expert',
        category: 'Comunicação',
        currentProgress: 34,
        requiredActions: 50,
        isUnlocked: false,
      },
      {
        id: 2,
        name: 'Mago da Automação',
        description: 'Criou 5+ templates de configuração',
        icon: 'automation_wizard',
        category: 'Automação',
        currentProgress: 3,
        requiredActions: 5,
        isUnlocked: false,
      },
      {
        id: 3,
        name: 'Líder de Equipe',
        description: 'Gerenciou uma equipe de 10+ pessoas',
        icon: 'team_leader',
        category: 'Liderança',
        currentProgress: 6,
        requiredActions: 10,
        isUnlocked: false,
      },
      {
        id: 4,
        name: 'Guardião da Segurança',
        description: 'Implementou todas as configurações de segurança',
        icon: 'security_guardian',
        category: 'Segurança',
        currentProgress: 4,
        requiredActions: 6,
        isUnlocked: false,
      },
    ],
    recentActivity: [
      { action: 'Cliente configurado com sucesso', xpGained: 50, timestamp: new Date() },
      { action: 'Template criado', xpGained: 100, timestamp: new Date(Date.now() - 3600000) },
      { action: 'Missão de onboarding completada', xpGained: 150, timestamp: new Date(Date.now() - 7200000) },
    ],
  });

  const getAchievementIcon = (iconName: string) => {
    const iconMap: Record<string, React.ReactNode> = {
      first_client: <EmojiEvents />,
      configuration_master: <Settings />,
      invincible: <Star />,
      rapid_expansion: <TrendingUp />,
    };
    return iconMap[iconName] || <EmojiEvents />;
  };

  const getSkillIcon = (iconName: string) => {
    const iconMap: Record<string, React.ReactNode> = {
      whatsapp_expert: <WhatsApp />,
      automation_wizard: <AutoAwesome />,
      team_leader: <Group />,
      security_guardian: <Security />,
    };
    return iconMap[iconName] || <Star />;
  };

  const getBadgeColor = (badgeClass: string) => {
    const colorMap: Record<string, string> = {
      bronze: '#CD7F32',
      silver: '#C0C0C0',
      gold: '#FFD700',
      platinum: '#E5E4E2',
    };
    return colorMap[badgeClass] || '#CD7F32';
  };

  const getLevelColor = (level: number) => {
    if (level >= 10) return 'primary';
    if (level >= 5) return 'secondary';
    return 'info';
  };

  const calculateLevelProgress = () => {
    const currentLevelXP = gamificationData.currentXP % 1000; // Assuming each level is 1000 XP
    return (currentLevelXP / 1000) * 100;
  };

  return (
    <Box>
      {/* Level and XP Display */}
      <Card sx={{ mb: 2 }}>
        <CardContent>
          <Grid container spacing={2} alignItems="center">
            <Grid item>
              <Avatar 
                sx={{ 
                  bgcolor: getLevelColor(gamificationData.currentLevel) + '.main',
                  width: 56,
                  height: 56,
                  fontSize: '1.5rem',
                  fontWeight: 'bold'
                }}
              >
                {gamificationData.currentLevel}
              </Avatar>
            </Grid>
            <Grid item xs>
              <Typography variant="h6">
                Nível {gamificationData.currentLevel} - {user?.full_name}
              </Typography>
              <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                <LinearProgress
                  variant="determinate"
                  value={calculateLevelProgress()}
                  sx={{ flexGrow: 1, mr: 2, height: 8, borderRadius: 4 }}
                />
                <Typography variant="body2" color="text.secondary">
                  {gamificationData.currentXP} XP
                </Typography>
              </Box>
              <Typography variant="caption" color="text.secondary">
                {gamificationData.xpToNextLevel} XP para o próximo nível
              </Typography>
            </Grid>
            <Grid item>
              <Chip 
                icon={<Star />} 
                label={`${gamificationData.totalMissionsCompleted} missões`}
                color="primary"
                variant="outlined"
              />
            </Grid>
          </Grid>
        </CardContent>
      </Card>

      {/* Quick Stats */}
      <Grid container spacing={2} sx={{ mb: 2 }}>
        <Grid item xs={12} sm={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" color="primary">
                    {gamificationData.achievements.filter(a => a.isUnlocked).length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Conquistas Desbloqueadas
                  </Typography>
                </Box>
                <IconButton onClick={() => setAchievementDialogOpen(true)}>
                  <Badge 
                    badgeContent={gamificationData.achievements.filter(a => !a.isUnlocked && a.progress).length}
                    color="secondary"
                  >
                    <EmojiEvents fontSize="large" />
                  </Badge>
                </IconButton>
              </Box>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} sm={6}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <Box>
                  <Typography variant="h4" color="secondary">
                    {gamificationData.skills.filter(s => s.isUnlocked).length}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Habilidades Desbloqueadas
                  </Typography>
                </Box>
                <IconButton onClick={() => setSkillTreeDialogOpen(true)}>
                  <Badge 
                    badgeContent={gamificationData.skills.filter(s => !s.isUnlocked && s.currentProgress > 0).length}
                    color="warning"
                  >
                    <Speed fontSize="large" />
                  </Badge>
                </IconButton>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Activity */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Atividade Recente
          </Typography>
          <List>
            {gamificationData.recentActivity.map((activity, index) => (
              <ListItem key={index}>
                <ListItemAvatar>
                  <Avatar sx={{ bgcolor: 'success.main' }}>
                    <CheckCircle />
                  </Avatar>
                </ListItemAvatar>
                <ListItemText
                  primary={activity.action}
                  secondary={`+${activity.xpGained} XP • ${activity.timestamp.toLocaleTimeString()}`}
                />
              </ListItem>
            ))}
          </List>
        </CardContent>
      </Card>

      {/* Achievements Dialog */}
      <Dialog
        open={achievementDialogOpen}
        onClose={() => setAchievementDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h6">Conquistas</Typography>
            <IconButton onClick={() => setAchievementDialogOpen(false)}>
              <Close />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2}>
            {gamificationData.achievements.map((achievement) => (
              <Grid item xs={12} sm={6} key={achievement.id}>
                <Card 
                  variant={achievement.isUnlocked ? "elevation" : "outlined"}
                  sx={{ 
                    opacity: achievement.isUnlocked ? 1 : 0.7,
                    border: achievement.isUnlocked ? `2px solid ${getBadgeColor(achievement.badgeClass)}` : undefined
                  }}
                >
                  <CardContent>
                    <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                      <Avatar 
                        sx={{ 
                          bgcolor: achievement.isUnlocked ? getBadgeColor(achievement.badgeClass) : 'grey.400',
                          mr: 2 
                        }}
                      >
                        {getAchievementIcon(achievement.icon)}
                      </Avatar>
                      <Box>
                        <Typography variant="h6">
                          {achievement.name}
                        </Typography>
                        <Chip 
                          label={`+${achievement.xpReward} XP`}
                          size="small"
                          color={achievement.isUnlocked ? "success" : "default"}
                        />
                      </Box>
                    </Box>
                    
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {achievement.description}
                    </Typography>
                    
                    {!achievement.isUnlocked && achievement.progress !== undefined && (
                      <Box>
                        <LinearProgress
                          variant="determinate"
                          value={(achievement.progress / achievement.maxProgress!) * 100}
                          sx={{ mb: 1 }}
                        />
                        <Typography variant="caption">
                          {achievement.progress} / {achievement.maxProgress}
                        </Typography>
                      </Box>
                    )}
                    
                    {achievement.isUnlocked && achievement.unlockedAt && (
                      <Typography variant="caption" color="success.main">
                        Desbloqueado em {achievement.unlockedAt.toLocaleDateString()}
                      </Typography>
                    )}
                  </CardContent>
                </Card>
              </Grid>
            ))}
          </Grid>
        </DialogContent>
      </Dialog>

      {/* Skill Tree Dialog */}
      <Dialog
        open={skillTreeDialogOpen}
        onClose={() => setSkillTreeDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h6">Árvore de Habilidades</Typography>
            <IconButton onClick={() => setSkillTreeDialogOpen(false)}>
              <Close />
            </IconButton>
          </Box>
        </DialogTitle>
        <DialogContent>
          {/* Group by category */}
          {Array.from(new Set(gamificationData.skills.map(s => s.category))).map(category => (
            <Box key={category} sx={{ mb: 3 }}>
              <Typography variant="h6" gutterBottom color="primary">
                {category}
              </Typography>
              <Grid container spacing={2}>
                {gamificationData.skills
                  .filter(skill => skill.category === category)
                  .map((skill) => (
                    <Grid item xs={12} sm={6} key={skill.id}>
                      <Card 
                        variant={skill.isUnlocked ? "elevation" : "outlined"}
                        sx={{ opacity: skill.isUnlocked ? 1 : 0.8 }}
                      >
                        <CardContent>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                            <Avatar 
                              sx={{ 
                                bgcolor: skill.isUnlocked ? 'secondary.main' : 'grey.400',
                                mr: 2 
                              }}
                            >
                              {getSkillIcon(skill.icon)}
                            </Avatar>
                            <Typography variant="h6">
                              {skill.name}
                            </Typography>
                          </Box>
                          
                          <Typography variant="body2" color="text.secondary" paragraph>
                            {skill.description}
                          </Typography>
                          
                          <Box>
                            <LinearProgress
                              variant="determinate"
                              value={(skill.currentProgress / skill.requiredActions) * 100}
                              sx={{ mb: 1 }}
                              color={skill.isUnlocked ? "success" : "primary"}
                            />
                            <Typography variant="caption">
                              Progresso: {skill.currentProgress} / {skill.requiredActions}
                            </Typography>
                          </Box>
                          
                          {skill.isUnlocked && skill.unlockedAt && (
                            <Typography variant="caption" color="success.main" sx={{ mt: 1, display: 'block' }}>
                              Desbloqueado em {skill.unlockedAt.toLocaleDateString()}
                            </Typography>
                          )}
                        </CardContent>
                      </Card>
                    </Grid>
                  ))}
              </Grid>
              {category !== Array.from(new Set(gamificationData.skills.map(s => s.category))).pop() && (
                <Divider sx={{ mt: 2 }} />
              )}
            </Box>
          ))}
        </DialogContent>
      </Dialog>
    </Box>
  );
};

export default GamificationSystem;