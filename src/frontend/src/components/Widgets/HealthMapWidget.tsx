import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Grid,
  IconButton,
  Tooltip,
  CircularProgress,
  Chip,
  LinearProgress,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  MoreVert as MoreVertIcon,
  CheckCircle,
  Warning,
  Error,
  Info,
  Assignment,
} from '@mui/icons-material';

export interface HealthMapItem {
  id: string;
  title: string;
  status: 'healthy' | 'warning' | 'critical' | 'unknown';
  description: string;
  value?: number;
  maxValue?: number;
  lastUpdate: Date;
  category: 'compliance' | 'performance' | 'security' | 'quality';
}

interface HealthMapWidgetProps {
  title: string;
  items: HealthMapItem[];
  loading?: boolean;
  onRefresh?: () => void;
  height?: number;
}

const HealthMapWidget: React.FC<HealthMapWidgetProps> = ({
  title,
  items,
  loading = false,
  onRefresh,
  height = 400,
}) => {
  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'healthy':
        return <CheckCircle color="success" />;
      case 'warning':
        return <Warning color="warning" />;
      case 'critical':
        return <Error color="error" />;
      case 'unknown':
        return <Info color="disabled" />;
      default:
        return <Assignment color="disabled" />;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'success.main';
      case 'warning':
        return 'warning.main';
      case 'critical':
        return 'error.main';
      case 'unknown':
        return 'grey.500';
      default:
        return 'grey.500';
    }
  };

  const getStatusLabel = (status: string) => {
    switch (status) {
      case 'healthy':
        return 'Saudável';
      case 'warning':
        return 'Atenção';
      case 'critical':
        return 'Crítico';
      case 'unknown':
        return 'Desconhecido';
      default:
        return 'N/A';
    }
  };

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case 'compliance':
        return 'Conformidade';
      case 'performance':
        return 'Performance';
      case 'security':
        return 'Segurança';
      case 'quality':
        return 'Qualidade';
      default:
        return category;
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case 'compliance':
        return 'primary';
      case 'performance':
        return 'secondary';
      case 'security':
        return 'error';
      case 'quality':
        return 'info';
      default:
        return 'default';
    }
  };

  const formatTimestamp = (timestamp: Date) => {
    return timestamp.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
    });
  };

  const getProgressPercentage = (value?: number, maxValue?: number) => {
    if (value === undefined || maxValue === undefined) return undefined;
    return Math.round((value / maxValue) * 100);
  };

  // Group items by category
  const groupedItems = items.reduce((acc, item) => {
    if (!acc[item.category]) {
      acc[item.category] = [];
    }
    acc[item.category].push(item);
    return acc;
  }, {} as Record<string, HealthMapItem[]>);

  return (
    <Card sx={{ height, display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ pb: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" component="h2" fontWeight={600}>
            {title}
          </Typography>
          <Box>
            {onRefresh && (
              <Tooltip title="Atualizar status">
                <IconButton size="small" onClick={onRefresh} disabled={loading}>
                  <RefreshIcon sx={{ fontSize: 18 }} />
                </IconButton>
              </Tooltip>
            )}
            <Tooltip title="Mais opções">
              <IconButton size="small">
                <MoreVertIcon sx={{ fontSize: 18 }} />
              </IconButton>
            </Tooltip>
          </Box>
        </Box>

        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
            <CircularProgress />
          </Box>
        ) : Object.keys(groupedItems).length === 0 ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
            <Typography variant="body2" color="text.secondary">
              Nenhum dado de saúde disponível
            </Typography>
          </Box>
        ) : (
          <Box sx={{ flex: 1, overflow: 'auto' }}>
            {Object.entries(groupedItems).map(([category, categoryItems]) => (
              <Box key={category} sx={{ mb: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Chip
                    label={getCategoryLabel(category)}
                    color={getCategoryColor(category) as any}
                    size="small"
                    sx={{ mr: 2 }}
                  />
                  <Typography variant="subtitle2" color="text.secondary">
                    {categoryItems.length} item{categoryItems.length !== 1 ? 's' : ''}
                  </Typography>
                </Box>

                <Grid container spacing={2}>
                  {categoryItems.map((item) => (
                    <Grid item xs={12} sm={6} key={item.id}>
                      <Box
                        sx={{
                          p: 2,
                          borderRadius: 1,
                          border: 1,
                          borderColor: getStatusColor(item.status),
                          bgcolor: 'background.paper',
                          position: 'relative',
                        }}
                      >
                        <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 1 }}>
                          <Box sx={{ mr: 2, mt: 0.5 }}>
                            {getStatusIcon(item.status)}
                          </Box>
                          <Box sx={{ flex: 1 }}>
                            <Typography variant="body1" fontWeight={500} sx={{ mb: 0.5 }}>
                              {item.title}
                            </Typography>
                            <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                              {item.description}
                            </Typography>
                          </Box>
                          <Chip
                            label={getStatusLabel(item.status)}
                            size="small"
                            sx={{
                              bgcolor: getStatusColor(item.status),
                              color: 'white',
                              fontWeight: 500,
                              height: 24,
                            }}
                          />
                        </Box>

                        {item.value !== undefined && item.maxValue !== undefined && (
                          <Box sx={{ mb: 1 }}>
                            <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 0.5 }}>
                              <Typography variant="caption" color="text.secondary">
                                Progresso
                              </Typography>
                              <Typography variant="caption" color="text.secondary">
                                {item.value}/{item.maxValue} ({getProgressPercentage(item.value, item.maxValue)}%)
                              </Typography>
                            </Box>
                            <LinearProgress
                              variant="determinate"
                              value={getProgressPercentage(item.value, item.maxValue)}
                              sx={{
                                height: 6,
                                borderRadius: 3,
                                bgcolor: 'grey.200',
                                '& .MuiLinearProgress-bar': {
                                  bgcolor: getStatusColor(item.status),
                                },
                              }}
                            />
                          </Box>
                        )}

                        <Typography variant="caption" color="text.secondary">
                          Atualizado em {formatTimestamp(item.lastUpdate)}
                        </Typography>
                      </Box>
                    </Grid>
                  ))}
                </Grid>
              </Box>
            ))}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default HealthMapWidget;