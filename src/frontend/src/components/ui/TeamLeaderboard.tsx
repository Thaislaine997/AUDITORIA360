import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Avatar,
  Chip,
  LinearProgress,
  Paper,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  ToggleButtonGroup,
  ToggleButton,
  Tooltip,
  Badge,
  Alert,
} from '@mui/material';
import {
  EmojiEvents,
  Star,
  TrendingUp,
  Speed,
  Person,
  Group,
  Assignment,
  CheckCircle,
  Error,
  Timeline,
} from '@mui/icons-material';
import { useAuthStore } from '../../stores/authStore';

interface TeamMember {
  id: number;
  full_name: string;
  email: string;
  position: string;
  xp_points: number;
  level: number;
  total_missions_completed: number;
  avatar?: string;
  
  // Performance metrics
  configurations_completed: number;
  successful_sends: number;
  failed_sends: number;
  clients_managed: number;
  anomalies_resolved: number;
  
  // Weekly/Monthly stats
  weekly_xp: number;
  monthly_xp: number;
  
  // Achievement highlights
  recent_achievements: string[];
  skill_specializations: string[];
}

interface TeamStats {
  total_members: number;
  average_xp: number;
  total_clients: number;
  success_rate: number;
  monthly_growth: number;
}

interface TeamLeaderboardProps {
  departmentFilter?: string;
}

const TeamLeaderboard: React.FC<TeamLeaderboardProps> = ({ departmentFilter }) => {
  const { user } = useAuthStore();
  const [timeframe, setTimeframe] = useState<'weekly' | 'monthly' | 'alltime'>('monthly');
  const [metricType, setMetricType] = useState<'xp' | 'configurations' | 'success_rate'>('xp');
  const [teamMembers, setTeamMembers] = useState<TeamMember[]>([]);
  const [teamStats, setTeamStats] = useState<TeamStats | null>(null);
  const [loading, setLoading] = useState(true);

  // Mock data - in reality this would come from the API
  useEffect(() => {
    const mockTeamMembers: TeamMember[] = [
      {
        id: 1,
        full_name: 'Ana Silva Santos',
        email: 'ana.silva@company.com',
        position: 'Analista Sênior',
        xp_points: 2850,
        level: 3,
        total_missions_completed: 12,
        configurations_completed: 47,
        successful_sends: 1230,
        failed_sends: 23,
        clients_managed: 15,
        anomalies_resolved: 8,
        weekly_xp: 450,
        monthly_xp: 1200,
        recent_achievements: ['Mestre da Configuração', 'Especialista em WhatsApp'],
        skill_specializations: ['Comunicação', 'Automação'],
      },
      {
        id: 2,
        full_name: 'Carlos Roberto Lima',
        email: 'carlos.lima@company.com',
        position: 'Analista Pleno',
        xp_points: 2340,
        level: 2,
        total_missions_completed: 10,
        configurations_completed: 38,
        successful_sends: 980,
        failed_sends: 45,
        clients_managed: 12,
        anomalies_resolved: 5,
        weekly_xp: 320,
        monthly_xp: 890,
        recent_achievements: ['Primeiro Cliente', 'Organizador'],
        skill_specializations: ['Compliance'],
      },
      {
        id: 3,
        full_name: 'Mariana Costa Oliveira',
        email: 'mariana.costa@company.com',
        position: 'Analista Júnior',
        xp_points: 1890,
        level: 2,
        total_missions_completed: 8,
        configurations_completed: 29,
        successful_sends: 750,
        failed_sends: 12,
        clients_managed: 8,
        anomalies_resolved: 12,
        weekly_xp: 380,
        monthly_xp: 950,
        recent_achievements: ['Guardião da Segurança'],
        skill_specializations: ['Segurança', 'Compliance'],
      },
      {
        id: 4,
        full_name: 'João Pedro Ferreira',
        email: 'joao.ferreira@company.com',
        position: 'Analista Júnior',
        xp_points: 1650,
        level: 2,
        total_missions_completed: 7,
        configurations_completed: 22,
        successful_sends: 560,
        failed_sends: 18,
        clients_managed: 6,
        anomalies_resolved: 3,
        weekly_xp: 290,
        monthly_xp: 780,
        recent_achievements: ['Eficiência'],
        skill_specializations: ['Automação'],
      },
      {
        id: 5,
        full_name: 'Fernanda Alves Rodrigues',
        email: 'fernanda.alves@company.com',
        position: 'Analista Pleno',
        xp_points: 2120,
        level: 2,
        total_missions_completed: 9,
        configurations_completed: 35,
        successful_sends: 890,
        failed_sends: 31,
        clients_managed: 11,
        anomalies_resolved: 7,
        weekly_xp: 410,
        monthly_xp: 1050,
        recent_achievements: ['Mestre da Configuração'],
        skill_specializations: ['Comunicação', 'Análise'],
      },
    ];

    const mockTeamStats: TeamStats = {
      total_members: 5,
      average_xp: 2170,
      total_clients: 52,
      success_rate: 96.2,
      monthly_growth: 15.3,
    };

    // Simulate API call
    setTimeout(() => {
      setTeamMembers(mockTeamMembers);
      setTeamStats(mockTeamStats);
      setLoading(false);
    }, 1000);
  }, [timeframe, metricType]);

  const getSortedMembers = () => {
    return [...teamMembers].sort((a, b) => {
      switch (metricType) {
        case 'xp':
          return timeframe === 'weekly' ? b.weekly_xp - a.weekly_xp :
                 timeframe === 'monthly' ? b.monthly_xp - a.monthly_xp :
                 b.xp_points - a.xp_points;
        case 'configurations':
          return b.configurations_completed - a.configurations_completed;
        case 'success_rate':
          const aRate = a.successful_sends / (a.successful_sends + a.failed_sends);
          const bRate = b.successful_sends / (b.successful_sends + b.failed_sends);
          return bRate - aRate;
        default:
          return b.xp_points - a.xp_points;
      }
    });
  };

  const getRankingIcon = (rank: number) => {
    switch (rank) {
      case 1:
        return <EmojiEvents sx={{ color: '#FFD700' }} />;
      case 2:
        return <EmojiEvents sx={{ color: '#C0C0C0' }} />;
      case 3:
        return <EmojiEvents sx={{ color: '#CD7F32' }} />;
      default:
        return <Typography variant="body1" fontWeight="bold">{rank}</Typography>;
    }
  };

  const getSuccessRate = (member: TeamMember) => {
    const total = member.successful_sends + member.failed_sends;
    return total > 0 ? ((member.successful_sends / total) * 100).toFixed(1) : '0';
  };

  const getMetricValue = (member: TeamMember) => {
    switch (metricType) {
      case 'xp':
        return timeframe === 'weekly' ? member.weekly_xp :
               timeframe === 'monthly' ? member.monthly_xp :
               member.xp_points;
      case 'configurations':
        return member.configurations_completed;
      case 'success_rate':
        return `${getSuccessRate(member)}%`;
      default:
        return member.xp_points;
    }
  };

  const getMetricLabel = () => {
    switch (metricType) {
      case 'xp':
        return timeframe === 'weekly' ? 'XP Semanal' :
               timeframe === 'monthly' ? 'XP Mensal' :
               'XP Total';
      case 'configurations':
        return 'Configurações';
      case 'success_rate':
        return 'Taxa de Sucesso';
      default:
        return 'XP Total';
    }
  };

  const getUserInitials = (name: string) => {
    return name
      .split(' ')
      .map(part => part.charAt(0))
      .join('')
      .toUpperCase()
      .substring(0, 2);
  };

  if (user?.user_profile !== 'gestor' && user?.role !== 'ADMINISTRADOR') {
    return (
      <Alert severity="warning">
        Apenas gestores podem visualizar o placar da equipe.
      </Alert>
    );
  }

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <EmojiEvents sx={{ mr: 2, color: 'primary.main' }} />
          Placar da Equipe
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Acompanhe o desempenho e conquistas da sua equipe
        </Typography>
      </Box>

      {/* Team Stats Overview */}
      {teamStats && (
        <Grid container spacing={3} sx={{ mb: 4 }}>
          <Grid item xs={12} md={6} lg={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: 'primary.main', mr: 2 }}>
                    <Group />
                  </Avatar>
                  <Box>
                    <Typography variant="h4">{teamStats.total_members}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Membros da Equipe
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6} lg={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: 'success.main', mr: 2 }}>
                    <Star />
                  </Avatar>
                  <Box>
                    <Typography variant="h4">{teamStats.average_xp}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      XP Médio
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6} lg={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: 'info.main', mr: 2 }}>
                    <Person />
                  </Avatar>
                  <Box>
                    <Typography variant="h4">{teamStats.total_clients}</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Clientes Gerenciados
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6} lg={3}>
            <Card>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center' }}>
                  <Avatar sx={{ bgcolor: 'warning.main', mr: 2 }}>
                    <TrendingUp />
                  </Avatar>
                  <Box>
                    <Typography variant="h4">{teamStats.success_rate}%</Typography>
                    <Typography variant="body2" color="text.secondary">
                      Taxa de Sucesso
                    </Typography>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      )}

      {/* Controls */}
      <Box sx={{ mb: 3, display: 'flex', gap: 3, flexWrap: 'wrap', alignItems: 'center' }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel>Métrica</InputLabel>
          <Select
            value={metricType}
            label="Métrica"
            onChange={(e) => setMetricType(e.target.value as any)}
          >
            <MenuItem value="xp">XP e Gamificação</MenuItem>
            <MenuItem value="configurations">Configurações Concluídas</MenuItem>
            <MenuItem value="success_rate">Taxa de Sucesso</MenuItem>
          </Select>
        </FormControl>

        <ToggleButtonGroup
          value={timeframe}
          exclusive
          onChange={(_, newTimeframe) => newTimeframe && setTimeframe(newTimeframe)}
          aria-label="timeframe"
        >
          <ToggleButton value="weekly" aria-label="weekly">
            Semanal
          </ToggleButton>
          <ToggleButton value="monthly" aria-label="monthly">
            Mensal
          </ToggleButton>
          <ToggleButton value="alltime" aria-label="all time">
            Geral
          </ToggleButton>
        </ToggleButtonGroup>
      </Box>

      {/* Leaderboard Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Ranking - {getMetricLabel()}
          </Typography>
          
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell width="60px">Posição</TableCell>
                  <TableCell>Membro da Equipe</TableCell>
                  <TableCell align="center">Nível</TableCell>
                  <TableCell align="center">{getMetricLabel()}</TableCell>
                  <TableCell align="center">Especializações</TableCell>
                  <TableCell align="center">Conquistas Recentes</TableCell>
                  <TableCell align="center">Performance</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {getSortedMembers().map((member, index) => (
                  <TableRow 
                    key={member.id}
                    sx={{ 
                      backgroundColor: index < 3 ? 'action.hover' : 'transparent',
                      '&:hover': { backgroundColor: 'action.selected' }
                    }}
                  >
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                        {getRankingIcon(index + 1)}
                      </Box>
                    </TableCell>
                    
                    <TableCell>
                      <Box sx={{ display: 'flex', alignItems: 'center' }}>
                        <Avatar sx={{ mr: 2, bgcolor: 'secondary.main' }}>
                          {member.avatar ? (
                            <img src={member.avatar} alt={member.full_name} />
                          ) : (
                            getUserInitials(member.full_name)
                          )}
                        </Avatar>
                        <Box>
                          <Typography variant="subtitle2" fontWeight="bold">
                            {member.full_name}
                          </Typography>
                          <Typography variant="body2" color="text.secondary">
                            {member.position}
                          </Typography>
                        </Box>
                      </Box>
                    </TableCell>
                    
                    <TableCell align="center">
                      <Chip
                        icon={<Star />}
                        label={`Nível ${member.level}`}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                    </TableCell>
                    
                    <TableCell align="center">
                      <Typography variant="h6" color="primary">
                        {getMetricValue(member)}
                      </Typography>
                    </TableCell>
                    
                    <TableCell align="center">
                      <Box sx={{ display: 'flex', gap: 0.5, justifyContent: 'center', flexWrap: 'wrap' }}>
                        {member.skill_specializations.slice(0, 2).map((skill) => (
                          <Chip
                            key={skill}
                            label={skill}
                            size="small"
                            color="secondary"
                            variant="outlined"
                          />
                        ))}
                        {member.skill_specializations.length > 2 && (
                          <Tooltip title={member.skill_specializations.slice(2).join(', ')}>
                            <Chip
                              label={`+${member.skill_specializations.length - 2}`}
                              size="small"
                              color="info"
                            />
                          </Tooltip>
                        )}
                      </Box>
                    </TableCell>
                    
                    <TableCell align="center">
                      <Box sx={{ display: 'flex', gap: 0.5, justifyContent: 'center', flexWrap: 'wrap' }}>
                        {member.recent_achievements.slice(0, 2).map((achievement) => (
                          <Chip
                            key={achievement}
                            label={achievement}
                            size="small"
                            color="warning"
                            variant="outlined"
                            icon={<EmojiEvents />}
                          />
                        ))}
                      </Box>
                    </TableCell>
                    
                    <TableCell align="center">
                      <Box sx={{ minWidth: 120 }}>
                        <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 0.5 }}>
                          <Typography variant="caption">Taxa Sucesso</Typography>
                          <Typography variant="caption" fontWeight="bold">
                            {getSuccessRate(member)}%
                          </Typography>
                        </Box>
                        <LinearProgress
                          variant="determinate"
                          value={parseFloat(getSuccessRate(member))}
                          color={parseFloat(getSuccessRate(member)) >= 95 ? 'success' : 
                                 parseFloat(getSuccessRate(member)) >= 90 ? 'warning' : 'error'}
                          sx={{ height: 4, borderRadius: 2 }}
                        />
                        <Typography variant="caption" color="text.secondary" sx={{ mt: 0.5, display: 'block' }}>
                          {member.successful_sends + member.failed_sends} envios
                        </Typography>
                      </Box>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Additional Insights */}
      <Box sx={{ mt: 4 }}>
        <Grid container spacing={3}>
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <Timeline sx={{ mr: 1 }} />
                  Tendências da Equipe
                </Typography>
                <Box sx={{ height: 200, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'grey.100', borderRadius: 1 }}>
                  <Typography variant="body2" color="text.secondary">
                    Gráfico de tendências (XP, configurações, sucesso)
                  </Typography>
                </Box>
              </CardContent>
            </Card>
          </Grid>
          
          <Grid item xs={12} md={6}>
            <Card>
              <CardContent>
                <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                  <Assignment sx={{ mr: 1 }} />
                  Metas da Equipe
                </Typography>
                <Box sx={{ mt: 2 }}>
                  <Box sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Configurações do Mês</Typography>
                      <Typography variant="body2" fontWeight="bold">171/200</Typography>
                    </Box>
                    <LinearProgress variant="determinate" value={85.5} color="primary" />
                  </Box>
                  
                  <Box sx={{ mb: 2 }}>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Taxa de Sucesso</Typography>
                      <Typography variant="body2" fontWeight="bold">96.2/95%</Typography>
                    </Box>
                    <LinearProgress variant="determinate" value={100} color="success" />
                  </Box>
                  
                  <Box>
                    <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 1 }}>
                      <Typography variant="body2">Clientes Ativos</Typography>
                      <Typography variant="body2" fontWeight="bold">52/60</Typography>
                    </Box>
                    <LinearProgress variant="determinate" value={86.7} color="info" />
                  </Box>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>
    </Box>
  );
};

export default TeamLeaderboard;