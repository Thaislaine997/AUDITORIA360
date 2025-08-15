import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  Avatar,
  Chip,
  IconButton,
  Tooltip,
  CircularProgress,
  Divider,
} from '@mui/material';
import {
  Refresh as RefreshIcon,
  MoreVert as MoreVertIcon,
  Person,
  Assignment,
  Description,
  Warning,
  CheckCircle,
  Error,
} from '@mui/icons-material';

export interface ActivityItem {
  id: string;
  type: 'user_action' | 'system' | 'audit' | 'document' | 'alert';
  title: string;
  description: string;
  timestamp: Date;
  user?: string;
  status?: 'success' | 'warning' | 'error' | 'info';
  link?: string;
}

interface ActivityFeedWidgetProps {
  title: string;
  activities: ActivityItem[];
  loading?: boolean;
  onRefresh?: () => void;
  maxItems?: number;
  height?: number;
}

const ActivityFeedWidget: React.FC<ActivityFeedWidgetProps> = ({
  title,
  activities,
  loading = false,
  onRefresh,
  maxItems = 10,
  height = 400,
}) => {
  const getActivityIcon = (type: string, status?: string) => {
    switch (type) {
      case 'user_action':
        return <Person />;
      case 'audit':
        return <Assignment />;
      case 'document':
        return <Description />;
      case 'alert':
        switch (status) {
          case 'error':
            return <Error color="error" />;
          case 'warning':
            return <Warning color="warning" />;
          case 'success':
            return <CheckCircle color="success" />;
          default:
            return <Warning />;
        }
      default:
        return <Assignment />;
    }
  };

  const getActivityColor = (type: string, status?: string) => {
    if (type === 'alert') {
      switch (status) {
        case 'error':
          return 'error.main';
        case 'warning':
          return 'warning.main';
        case 'success':
          return 'success.main';
        default:
          return 'info.main';
      }
    }
    return 'primary.main';
  };

  const getStatusChip = (status?: string) => {
    if (!status) return null;

    const statusConfig = {
      success: { label: 'Sucesso', color: 'success' as const },
      warning: { label: 'Atenção', color: 'warning' as const },
      error: { label: 'Erro', color: 'error' as const },
      info: { label: 'Info', color: 'info' as const },
    };

    const config = statusConfig[status as keyof typeof statusConfig];
    if (!config) return null;

    return (
      <Chip
        label={config.label}
        size="small"
        color={config.color}
        sx={{ height: 20, fontSize: '0.7rem' }}
      />
    );
  };

  const formatTimestamp = (timestamp: Date) => {
    const now = new Date();
    const diff = now.getTime() - timestamp.getTime();
    const minutes = Math.floor(diff / 60000);
    const hours = Math.floor(diff / 3600000);
    const days = Math.floor(diff / 86400000);

    if (minutes < 1) return 'Agora';
    if (minutes < 60) return `${minutes}min atrás`;
    if (hours < 24) return `${hours}h atrás`;
    if (days < 7) return `${days}d atrás`;
    
    return timestamp.toLocaleDateString('pt-BR', {
      day: '2-digit',
      month: '2-digit',
      year: '2-digit',
    });
  };

  const displayedActivities = activities.slice(0, maxItems);

  return (
    <Card sx={{ height, display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ pb: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
          <Typography variant="h6" component="h2" fontWeight={600}>
            {title}
          </Typography>
          <Box>
            {onRefresh && (
              <Tooltip title="Atualizar atividades">
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
        ) : displayedActivities.length === 0 ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: 300 }}>
            <Typography variant="body2" color="text.secondary">
              Nenhuma atividade recente
            </Typography>
          </Box>
        ) : (
          <Box sx={{ flex: 1, overflow: 'auto' }}>
            <List disablePadding>
              {displayedActivities.map((activity, index) => (
                <React.Fragment key={activity.id}>
                  <ListItem
                    alignItems="flex-start"
                    sx={{
                      px: 0,
                      py: 1,
                      cursor: activity.link ? 'pointer' : 'default',
                      '&:hover': activity.link ? { bgcolor: 'action.hover' } : {},
                    }}
                    onClick={activity.link ? () => window.open(activity.link, '_blank') : undefined}
                  >
                    <ListItemAvatar>
                      <Avatar
                        sx={{
                          bgcolor: getActivityColor(activity.type, activity.status),
                          width: 36,
                          height: 36,
                        }}
                      >
                        {getActivityIcon(activity.type, activity.status)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                          <Typography variant="body2" fontWeight={500}>
                            {activity.title}
                          </Typography>
                          {getStatusChip(activity.status)}
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary" sx={{ mb: 0.5 }}>
                            {activity.description}
                          </Typography>
                          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                            <Typography variant="caption" color="text.secondary">
                              {formatTimestamp(activity.timestamp)}
                            </Typography>
                            {activity.user && (
                              <>
                                <Typography variant="caption" color="text.secondary">
                                  •
                                </Typography>
                                <Typography variant="caption" color="text.secondary">
                                  por {activity.user}
                                </Typography>
                              </>
                            )}
                          </Box>
                        </Box>
                      }
                    />
                  </ListItem>
                  {index < displayedActivities.length - 1 && <Divider variant="inset" component="li" />}
                </React.Fragment>
              ))}
            </List>
            
            {activities.length > maxItems && (
              <Box sx={{ p: 1, textAlign: 'center' }}>
                <Typography variant="caption" color="text.secondary">
                  Mostrando {maxItems} de {activities.length} atividades
                </Typography>
              </Box>
            )}
          </Box>
        )}
      </CardContent>
    </Card>
  );
};

export default ActivityFeedWidget;