import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  IconButton,
  Badge,
  List,
  ListItem,
  ListItemAvatar,
  ListItemText,
  ListItemSecondaryAction,
  Avatar,
  Chip,
  Menu,
  MenuItem,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Switch,
  FormControlLabel,
  Divider,
  Select,
  FormControl,
  InputLabel,
  Grid,
  Tabs,
  Tab,
  TextField,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  Alert,
} from '@mui/material';
import {
  Notifications,
  NotificationsActive,
  Settings,
  Clear,
  MoreVert,
  CheckCircle,
  Error,
  Warning,
  Info,
  Star,
  TrendingUp,
  Security,
  Email,
  Sms,
  WhatsApp,
  ExpandMore,
  VolumeUp,
  Schedule,
} from '@mui/icons-material';

interface Notification {
  id: number;
  title: string;
  message: string;
  type: 'system' | 'client_activity' | 'configuration' | 'compliance' | 'achievement' | 'churn_alert' | 'anomaly';
  priority: 'low' | 'medium' | 'high' | 'critical';
  status: 'unread' | 'read' | 'dismissed';
  timestamp: Date;
  actionUrl?: string;
  icon?: React.ReactNode;
  canBeDismissed: boolean;
}

interface NotificationPreferences {
  emailEnabled: boolean;
  emailCriticalOnly: boolean;
  emailDigestFrequency: 'instant' | 'daily' | 'weekly' | 'never';
  
  notifySuccessSends: boolean;
  notifyFailureSends: boolean;
  notifyClientActivity: boolean;
  notifyConfigurationChanges: boolean;
  notifyComplianceAlerts: boolean;
  notifyChurnRisks: boolean;
  notifyAnomalyDetection: boolean;
  notifyAchievements: boolean;
  notifySystemUpdates: boolean;
  
  groupSimilarNotifications: boolean;
  maxNotificationsPerDigest: number;
  autoDismissReadNotifications: boolean;
  
  enableSoundNotifications: boolean;
  enableDesktopNotifications: boolean;
  preferredSound: string;
}

const NotificationCenter: React.FC = () => {
  const [anchorEl, setAnchorEl] = useState<null | HTMLElement>(null);
  const [preferencesOpen, setPreferencesOpen] = useState(false);
  const [activeTab, setActiveTab] = useState(0);
  const [notifications, setNotifications] = useState<Notification[]>([
    {
      id: 1,
      title: 'Cliente com risco de churn detectado',
      message: 'Cliente ABC Ltda apresenta 85% de risco de cancelamento. Sugerimos uma ação de contato.',
      type: 'churn_alert',
      priority: 'high',
      status: 'unread',
      timestamp: new Date(Date.now() - 300000),
      icon: <TrendingUp />,
      canBeDismissed: true,
    },
    {
      id: 2,
      title: 'Anomalia de compliance detectada',
      message: 'O envio do documento "DARF" para o Cliente XYZ foi interrompido, divergindo do padrão histórico.',
      type: 'anomaly',
      priority: 'critical',
      status: 'unread',
      timestamp: new Date(Date.now() - 600000),
      icon: <Security />,
      canBeDismissed: true,
    },
    {
      id: 3,
      title: 'Nova conquista desbloqueada!',
      message: 'Parabéns! Você desbloqueou a conquista "Mestre da Configuração" (+250 XP)',
      type: 'achievement',
      priority: 'medium',
      status: 'unread',
      timestamp: new Date(Date.now() - 1800000),
      icon: <Star />,
      canBeDismissed: true,
    },
    {
      id: 4,
      title: '1.000 envios realizados com sucesso',
      message: 'Milestone atingido! Todos os envios foram concluídos sem falhas hoje.',
      type: 'system',
      priority: 'low',
      status: 'read',
      timestamp: new Date(Date.now() - 3600000),
      icon: <CheckCircle />,
      canBeDismissed: true,
    },
  ]);

  const [preferences, setPreferences] = useState<NotificationPreferences>({
    emailEnabled: true,
    emailCriticalOnly: false,
    emailDigestFrequency: 'daily',
    
    notifySuccessSends: false,
    notifyFailureSends: true,
    notifyClientActivity: true,
    notifyConfigurationChanges: true,
    notifyComplianceAlerts: true,
    notifyChurnRisks: true,
    notifyAnomalyDetection: true,
    notifyAchievements: true,
    notifySystemUpdates: false,
    
    groupSimilarNotifications: true,
    maxNotificationsPerDigest: 10,
    autoDismissReadNotifications: false,
    
    enableSoundNotifications: true,
    enableDesktopNotifications: true,
    preferredSound: 'default',
  });

  const unreadCount = notifications.filter(n => n.status === 'unread').length;

  const getNotificationIcon = (notification: Notification) => {
    if (notification.icon) return notification.icon;
    
    switch (notification.priority) {
      case 'critical':
        return <Error color="error" />;
      case 'high':
        return <Warning color="warning" />;
      case 'medium':
        return <Info color="info" />;
      default:
        return <CheckCircle color="success" />;
    }
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      default:
        return 'success';
    }
  };

  const handleNotificationClick = (notification: Notification) => {
    if (notification.status === 'unread') {
      setNotifications(prev => 
        prev.map(n => 
          n.id === notification.id 
            ? { ...n, status: 'read' as const }
            : n
        )
      );
    }
    
    if (notification.actionUrl) {
      window.location.href = notification.actionUrl;
    }
  };

  const handleDismissNotification = (notificationId: number) => {
    setNotifications(prev => 
      prev.map(n => 
        n.id === notificationId 
          ? { ...n, status: 'dismissed' as const }
          : n
      )
    );
  };

  const handleMarkAllAsRead = () => {
    setNotifications(prev => 
      prev.map(n => ({ ...n, status: 'read' as const }))
    );
    setAnchorEl(null);
  };

  const handleClearAll = () => {
    setNotifications(prev => 
      prev.filter(n => !n.canBeDismissed).map(n => ({ ...n, status: 'dismissed' as const }))
    );
    setAnchorEl(null);
  };

  const filteredNotifications = notifications.filter(n => {
    if (activeTab === 0) return n.status !== 'dismissed'; // All
    if (activeTab === 1) return n.status === 'unread'; // Unread
    if (activeTab === 2) return n.priority === 'critical' || n.priority === 'high'; // Important
    return true;
  });

  const TabPanel: React.FC<{ children: React.ReactNode; value: number; index: number }> = ({ 
    children, 
    value, 
    index 
  }) => (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 2 }}>{children}</Box>}
    </div>
  );

  return (
    <>
      {/* Notification Bell */}
      <IconButton
        onClick={(e) => setAnchorEl(e.currentTarget)}
        color="inherit"
      >
        <Badge badgeContent={unreadCount} color="error">
          {unreadCount > 0 ? <NotificationsActive /> : <Notifications />}
        </Badge>
      </IconButton>

      {/* Notification Menu */}
      <Menu
        anchorEl={anchorEl}
        open={Boolean(anchorEl)}
        onClose={() => setAnchorEl(null)}
        PaperProps={{
          sx: { width: 400, maxHeight: 600 }
        }}
      >
        {/* Header */}
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
            <Typography variant="h6">
              Notificações
            </Typography>
            <Box>
              <IconButton 
                size="small" 
                onClick={() => setPreferencesOpen(true)}
                title="Configurar notificações"
              >
                <Settings />
              </IconButton>
              <IconButton 
                size="small" 
                onClick={(e) => {
                  e.stopPropagation();
                  // Show submenu
                }}
                title="Mais opções"
              >
                <MoreVert />
              </IconButton>
            </Box>
          </Box>
          
          {/* Tabs */}
          <Tabs
            value={activeTab}
            onChange={(_, newValue) => setActiveTab(newValue)}
            variant="fullWidth"
            sx={{ mt: 1 }}
          >
            <Tab label="Todas" />
            <Tab label={`Não lidas (${unreadCount})`} />
            <Tab label="Importantes" />
          </Tabs>
        </Box>

        {/* Quick Actions */}
        <Box sx={{ p: 1, borderBottom: 1, borderColor: 'divider' }}>
          <Button
            size="small"
            onClick={handleMarkAllAsRead}
            disabled={unreadCount === 0}
          >
            Marcar todas como lidas
          </Button>
          <Button
            size="small"
            onClick={handleClearAll}
            color="warning"
            sx={{ ml: 1 }}
          >
            Limpar todas
          </Button>
        </Box>

        {/* Notification Tabs Content */}
        <TabPanel value={activeTab} index={0}>
          <List sx={{ maxHeight: 400, overflow: 'auto' }}>
            {filteredNotifications.length === 0 ? (
              <ListItem>
                <ListItemText primary="Nenhuma notificação" />
              </ListItem>
            ) : (
              filteredNotifications.map((notification) => (
                <ListItem
                  key={notification.id}
                  button
                  onClick={() => handleNotificationClick(notification)}
                  sx={{
                    backgroundColor: notification.status === 'unread' ? 'action.hover' : 'transparent',
                    borderLeft: notification.status === 'unread' ? 3 : 0,
                    borderColor: `${getPriorityColor(notification.priority)}.main`,
                  }}
                >
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: `${getPriorityColor(notification.priority)}.main` }}>
                      {getNotificationIcon(notification)}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="subtitle2" noWrap>
                          {notification.title}
                        </Typography>
                        <Chip
                          label={notification.priority}
                          size="small"
                          color={getPriorityColor(notification.priority) as any}
                          variant="outlined"
                        />
                      </Box>
                    }
                    secondary={
                      <>
                        <Typography variant="body2" color="text.secondary" noWrap>
                          {notification.message}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {notification.timestamp.toLocaleTimeString()}
                        </Typography>
                      </>
                    }
                  />
                  {notification.canBeDismissed && (
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        aria-label="dismiss"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDismissNotification(notification.id);
                        }}
                      >
                        <Clear />
                      </IconButton>
                    </ListItemSecondaryAction>
                  )}
                </ListItem>
              ))
            )}
          </List>
        </TabPanel>

        <TabPanel value={activeTab} index={1}>
          <List sx={{ maxHeight: 400, overflow: 'auto' }}>
            {filteredNotifications.length === 0 ? (
              <ListItem>
                <ListItemText primary="Nenhuma notificação não lida" />
              </ListItem>
            ) : (
              filteredNotifications.map((notification) => (
                <ListItem
                  key={notification.id}
                  button
                  onClick={() => handleNotificationClick(notification)}
                  sx={{
                    backgroundColor: 'action.hover',
                    borderLeft: 3,
                    borderColor: `${getPriorityColor(notification.priority)}.main`,
                  }}
                >
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: `${getPriorityColor(notification.priority)}.main` }}>
                      {getNotificationIcon(notification)}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="subtitle2" noWrap>
                          {notification.title}
                        </Typography>
                        <Chip
                          label={notification.priority}
                          size="small"
                          color={getPriorityColor(notification.priority) as any}
                          variant="outlined"
                        />
                      </Box>
                    }
                    secondary={
                      <>
                        <Typography variant="body2" color="text.secondary" noWrap>
                          {notification.message}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {notification.timestamp.toLocaleTimeString()}
                        </Typography>
                      </>
                    }
                  />
                  {notification.canBeDismissed && (
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        aria-label="dismiss"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDismissNotification(notification.id);
                        }}
                      >
                        <Clear />
                      </IconButton>
                    </ListItemSecondaryAction>
                  )}
                </ListItem>
              ))
            )}
          </List>
        </TabPanel>

        <TabPanel value={activeTab} index={2}>
          <List sx={{ maxHeight: 400, overflow: 'auto' }}>
            {filteredNotifications.length === 0 ? (
              <ListItem>
                <ListItemText primary="Nenhuma notificação importante" />
              </ListItem>
            ) : (
              filteredNotifications.map((notification) => (
                <ListItem
                  key={notification.id}
                  button
                  onClick={() => handleNotificationClick(notification)}
                  sx={{
                    backgroundColor: notification.status === 'unread' ? 'action.hover' : 'transparent',
                    borderLeft: 3,
                    borderColor: `${getPriorityColor(notification.priority)}.main`,
                  }}
                >
                  <ListItemAvatar>
                    <Avatar sx={{ bgcolor: `${getPriorityColor(notification.priority)}.main` }}>
                      {getNotificationIcon(notification)}
                    </Avatar>
                  </ListItemAvatar>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="subtitle2" noWrap>
                          {notification.title}
                        </Typography>
                        <Chip
                          label={notification.priority}
                          size="small"
                          color={getPriorityColor(notification.priority) as any}
                          variant="outlined"
                        />
                      </Box>
                    }
                    secondary={
                      <>
                        <Typography variant="body2" color="text.secondary" noWrap>
                          {notification.message}
                        </Typography>
                        <Typography variant="caption" color="text.secondary">
                          {notification.timestamp.toLocaleTimeString()}
                        </Typography>
                      </>
                    }
                  />
                  {notification.canBeDismissed && (
                    <ListItemSecondaryAction>
                      <IconButton
                        edge="end"
                        aria-label="dismiss"
                        onClick={(e) => {
                          e.stopPropagation();
                          handleDismissNotification(notification.id);
                        }}
                      >
                        <Clear />
                      </IconButton>
                    </ListItemSecondaryAction>
                  )}
                </ListItem>
              ))
            )}
          </List>
        </TabPanel>
      </Menu>

      {/* Notification Preferences Dialog */}
      <Dialog
        open={preferencesOpen}
        onClose={() => setPreferencesOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Preferências de Notificação</DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 3 }}>
            Configure como e quando você deseja receber notificações. Suas preferências são salvas automaticamente.
          </Alert>

          {/* Email Settings */}
          <Accordion defaultExpanded>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Email sx={{ mr: 1 }} />
                <Typography variant="h6">Configurações de Email</Typography>
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.emailEnabled}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          emailEnabled: e.target.checked
                        }))}
                      />
                    }
                    label="Receber notificações por email"
                  />
                </Grid>
                
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.emailCriticalOnly}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          emailCriticalOnly: e.target.checked
                        }))}
                        disabled={!preferences.emailEnabled}
                      />
                    }
                    label="Apenas falhas críticas por email"
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  <FormControl fullWidth disabled={!preferences.emailEnabled}>
                    <InputLabel>Frequência do resumo</InputLabel>
                    <Select
                      value={preferences.emailDigestFrequency}
                      label="Frequência do resumo"
                      onChange={(e) => setPreferences(prev => ({
                        ...prev,
                        emailDigestFrequency: e.target.value as any
                      }))}
                    >
                      <MenuItem value="instant">Instantâneo</MenuItem>
                      <MenuItem value="daily">Resumo diário</MenuItem>
                      <MenuItem value="weekly">Resumo semanal</MenuItem>
                      <MenuItem value="never">Nunca</MenuItem>
                    </Select>
                  </FormControl>
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>

          {/* Notification Types */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Notifications sx={{ mr: 1 }} />
                <Typography variant="h6">Tipos de Notificação</Typography>
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={1}>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.notifySuccessSends}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          notifySuccessSends: e.target.checked
                        }))}
                      />
                    }
                    label="Notificar sobre envios bem-sucedidos"
                  />
                </Grid>
                
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.notifyFailureSends}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          notifyFailureSends: e.target.checked
                        }))}
                      />
                    }
                    label="Notificar sobre falhas de envio"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.notifyClientActivity}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          notifyClientActivity: e.target.checked
                        }))}
                      />
                    }
                    label="Notificar sobre atividade de clientes"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.notifyChurnRisks}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          notifyChurnRisks: e.target.checked
                        }))}
                      />
                    }
                    label="Alertas de risco de churn de clientes"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.notifyAnomalyDetection}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          notifyAnomalyDetection: e.target.checked
                        }))}
                      />
                    }
                    label="Detecção de anomalias de compliance"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.notifyAchievements}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          notifyAchievements: e.target.checked
                        }))}
                      />
                    }
                    label="Conquistas e marcos"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.notifySystemUpdates}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          notifySystemUpdates: e.target.checked
                        }))}
                      />
                    }
                    label="Atualizações do sistema"
                  />
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>

          {/* Advanced Settings */}
          <Accordion>
            <AccordionSummary expandIcon={<ExpandMore />}>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Settings sx={{ mr: 1 }} />
                <Typography variant="h6">Configurações Avançadas</Typography>
              </Box>
            </AccordionSummary>
            <AccordionDetails>
              <Grid container spacing={2}>
                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.groupSimilarNotifications}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          groupSimilarNotifications: e.target.checked
                        }))}
                      />
                    }
                    label="Agrupar notificações similares"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.autoDismissReadNotifications}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          autoDismissReadNotifications: e.target.checked
                        }))}
                      />
                    }
                    label="Dispensar automaticamente notificações lidas"
                  />
                </Grid>

                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Máximo por resumo"
                    type="number"
                    value={preferences.maxNotificationsPerDigest}
                    onChange={(e) => setPreferences(prev => ({
                      ...prev,
                      maxNotificationsPerDigest: parseInt(e.target.value) || 10
                    }))}
                    inputProps={{ min: 1, max: 50 }}
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.enableSoundNotifications}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          enableSoundNotifications: e.target.checked
                        }))}
                      />
                    }
                    label="Sons de notificação"
                  />
                </Grid>

                <Grid item xs={12}>
                  <FormControlLabel
                    control={
                      <Switch
                        checked={preferences.enableDesktopNotifications}
                        onChange={(e) => setPreferences(prev => ({
                          ...prev,
                          enableDesktopNotifications: e.target.checked
                        }))}
                      />
                    }
                    label="Notificações no desktop"
                  />
                </Grid>
              </Grid>
            </AccordionDetails>
          </Accordion>
        </DialogContent>
        
        <DialogActions>
          <Button onClick={() => setPreferencesOpen(false)}>
            Cancelar
          </Button>
          <Button variant="contained" onClick={() => setPreferencesOpen(false)}>
            Salvar Preferências
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default NotificationCenter;