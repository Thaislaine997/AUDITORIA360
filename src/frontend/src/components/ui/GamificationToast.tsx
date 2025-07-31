import React from 'react';
import {
  Snackbar,
  Alert,
  Box,
  Typography,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  EmojiEvents,
  Star,
  TrendingUp,
  CheckCircle,
  Diamond,
  LocalFireDepartment,
} from '@mui/icons-material';

export interface Achievement {
  id: string;
  title: string;
  description: string;
  icon: React.ReactNode;
  color: 'primary' | 'secondary' | 'success' | 'warning' | 'error' | 'info';
  rarity: 'comum' | 'raro' | 'épico' | 'lendário';
  points: number;
  category: string;
}

interface GamificationToastProps {
  achievement: Achievement | null;
  open: boolean;
  onClose: () => void;
}

const rarityColors = {
  comum: '#9e9e9e',
  raro: '#2196f3',
  épico: '#9c27b0',
  lendário: '#ff9800',
};

const rarityIcons = {
  comum: <Star />,
  raro: <Diamond />,
  épico: <EmojiEvents />,
  lendário: <LocalFireDepartment />,
};

const GamificationToast: React.FC<GamificationToastProps> = ({
  achievement,
  open,
  onClose,
}) => {
  if (!achievement) return null;

  return (
    <Snackbar
      open={open}
      autoHideDuration={6000}
      onClose={onClose}
      anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
      sx={{ mt: 8 }}
    >
      <Alert
        severity="success"
        onClose={onClose}
        sx={{
          width: '100%',
          minWidth: 350,
          bgcolor: 'background.paper',
          color: 'text.primary',
          border: 2,
          borderColor: rarityColors[achievement.rarity],
          boxShadow: 3,
          '& .MuiAlert-icon': {
            color: rarityColors[achievement.rarity],
          },
        }}
        icon={<EmojiEvents />}
      >
        <Box>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <Typography variant="h6" component="div" sx={{ fontWeight: 600 }}>
              🎉 Conquista Desbloqueada!
            </Typography>
            <Chip
              icon={rarityIcons[achievement.rarity]}
              label={achievement.rarity.toUpperCase()}
              size="small"
              sx={{
                bgcolor: rarityColors[achievement.rarity],
                color: 'white',
                fontWeight: 'bold',
                textTransform: 'uppercase',
              }}
            />
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
            <Box sx={{ color: rarityColors[achievement.rarity] }}>
              {achievement.icon}
            </Box>
            <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
              {achievement.title}
            </Typography>
          </Box>

          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            {achievement.description}
          </Typography>

          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Chip
              label={`+${achievement.points} XP`}
              size="small"
              color="primary"
              icon={<TrendingUp />}
            />
            <Chip
              label={achievement.category}
              size="small"
              variant="outlined"
            />
          </Box>
        </Box>
      </Alert>
    </Snackbar>
  );
};

// Predefined achievements
export const achievements: Achievement[] = [
  {
    id: 'first_client_config',
    title: 'Mestre da Configuração',
    description: 'Configure seu primeiro cliente completamente!',
    icon: <CheckCircle />,
    color: 'success',
    rarity: 'comum',
    points: 50,
    category: 'Configuração',
  },
  {
    id: 'risk_analysis_master',
    title: 'Consultor Expert',
    description: 'Realizou 10 análises de risco com o Consultor IA',
    icon: <EmojiEvents />,
    color: 'primary',
    rarity: 'raro',
    points: 150,
    category: 'Análise',
  },
  {
    id: 'report_wizard',
    title: 'Mestre dos Relatórios',
    description: 'Gerou mais de 50 relatórios diferentes',
    icon: <TrendingUp />,
    color: 'info',
    rarity: 'épico',
    points: 300,
    category: 'Relatórios',
  },
  {
    id: 'automation_legend',
    title: 'Lenda da Automação',
    description: 'Automatizou 100% dos processos de um cliente',
    icon: <LocalFireDepartment />,
    color: 'warning',
    rarity: 'lendário',
    points: 500,
    category: 'Automação',
  },
  {
    id: 'first_login',
    title: 'Bem-vindo!',
    description: 'Fez seu primeiro login no sistema',
    icon: <Star />,
    color: 'primary',
    rarity: 'comum',
    points: 10,
    category: 'Início',
  },
  {
    id: 'team_player',
    title: 'Colaborador Exemplar',
    description: 'Ajudou 5 colegas com suas tarefas',
    icon: <EmojiEvents />,
    color: 'success',
    rarity: 'raro',
    points: 200,
    category: 'Colaboração',
  },
];

export default GamificationToast;