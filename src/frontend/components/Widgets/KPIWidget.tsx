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
} from '@mui/material';
import {
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  Refresh as RefreshIcon,
  MoreVert as MoreVertIcon,
} from '@mui/icons-material';

export interface KPIData {
  title: string;
  value: string | number;
  change?: number;
  changeType?: 'increase' | 'decrease' | 'neutral';
  format?: 'currency' | 'percentage' | 'number';
  icon?: React.ReactNode;
  subtitle?: string;
}

interface KPIWidgetProps {
  title: string;
  data: KPIData[];
  loading?: boolean;
  onRefresh?: () => void;
  height?: number;
}

const KPIWidget: React.FC<KPIWidgetProps> = ({
  title,
  data,
  loading = false,
  onRefresh,
  height = 300,
}) => {
  const formatValue = (value: string | number, format?: string) => {
    if (typeof value === 'string') return value;
    
    switch (format) {
      case 'currency':
        return new Intl.NumberFormat('pt-BR', {
          style: 'currency',
          currency: 'BRL',
        }).format(value);
      case 'percentage':
        return `${value}%`;
      default:
        return value.toLocaleString('pt-BR');
    }
  };

  const getTrendIcon = (changeType?: string) => {
    switch (changeType) {
      case 'increase':
        return <TrendingUp sx={{ color: 'success.main', fontSize: 16 }} />;
      case 'decrease':
        return <TrendingDown sx={{ color: 'error.main', fontSize: 16 }} />;
      case 'neutral':
        return <TrendingFlat sx={{ color: 'warning.main', fontSize: 16 }} />;
      default:
        return null;
    }
  };

  const getTrendColor = (changeType?: string) => {
    switch (changeType) {
      case 'increase':
        return 'success.main';
      case 'decrease':
        return 'error.main';
      case 'neutral':
        return 'warning.main';
      default:
        return 'text.secondary';
    }
  };

  return (
    <Card sx={{ height, display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ pb: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" component="h2" fontWeight={600}>
            {title}
          </Typography>
          <Box>
            {onRefresh && (
              <Tooltip title="Atualizar dados">
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
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 200 }}>
            <CircularProgress />
          </Box>
        ) : (
          <Grid container spacing={2}>
            {data.map((kpi, index) => (
              <Grid item xs={12} sm={6} md={data.length > 2 ? 6 : 12} key={index}>
                <Box
                  sx={{
                    p: 2,
                    borderRadius: 1,
                    bgcolor: 'background.paper',
                    border: 1,
                    borderColor: 'divider',
                    height: '100%',
                    display: 'flex',
                    flexDirection: 'column',
                    justifyContent: 'center',
                  }}
                >
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    {kpi.icon && (
                      <Box sx={{ mr: 1, color: 'primary.main' }}>
                        {kpi.icon}
                      </Box>
                    )}
                    <Typography variant="body2" color="text.secondary" fontWeight={500}>
                      {kpi.title}
                    </Typography>
                  </Box>
                  
                  <Typography variant="h4" fontWeight={700} sx={{ mb: 0.5 }}>
                    {formatValue(kpi.value, kpi.format)}
                  </Typography>
                  
                  {kpi.subtitle && (
                    <Typography variant="caption" color="text.secondary">
                      {kpi.subtitle}
                    </Typography>
                  )}
                  
                  {kpi.change !== undefined && (
                    <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                      {getTrendIcon(kpi.changeType)}
                      <Typography
                        variant="body2"
                        sx={{
                          ml: 0.5,
                          color: getTrendColor(kpi.changeType),
                          fontWeight: 500,
                        }}
                      >
                        {kpi.change > 0 ? '+' : ''}{kpi.change}%
                      </Typography>
                      <Typography variant="caption" color="text.secondary" sx={{ ml: 1 }}>
                        vs mês anterior
                      </Typography>
                    </Box>
                  )}
                </Box>
              </Grid>
            ))}
          </Grid>
        )}
      </CardContent>
    </Card>
  );
};

export default KPIWidget;