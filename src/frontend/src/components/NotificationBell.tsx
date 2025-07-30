import React, { useState, useEffect } from "react";
import {
  IconButton,
  Badge,
  Popover,
  List,
  ListItem,
  ListItemText,
  ListItemAvatar,
  Avatar,
  Typography,
  Button,
  Box,
  Divider,
  Chip,
} from "@mui/material";
import {
  Notifications as NotificationsIcon,
  Info as InfoIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
  CheckCircle as CheckCircleIcon,
} from "@mui/icons-material";

interface Notification {
  id: number;
  title: string;
  message: string;
  type: string;
  priority: string;
  status: string;
  action_url?: string;
  action_text?: string;
  created_at: string;
  read_at?: string;
}

const NotificationBell: React.FC = () => {
  const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);
  const [notifications, setNotifications] = useState<Notification[]>([]);
  const [unreadCount, setUnreadCount] = useState(0);
  const [loading, setLoading] = useState(false);

  // Mock data for now - TODO: Replace with actual API calls
  useEffect(() => {
    // Simulate fetching unread count
    setUnreadCount(3);
    
    // Simulate fetching notifications
    setNotifications([
      {
        id: 1,
        title: "Nova Contabilidade Cadastrada",
        message: "A contabilidade 'Escritório Santos & Associados' se cadastrou na plataforma",
        type: "system",
        priority: "medium",
        status: "pending",
        action_url: "/admin/contabilidades/123",
        action_text: "Ver Detalhes",
        created_at: "2024-01-10T09:30:00Z",
      },
      {
        id: 2,
        title: "Novo Documento Recebido",
        message: "Cliente 'Empresa ABC Ltda' enviou um novo documento",
        type: "system",
        priority: "high",
        status: "pending",
        action_url: "/documents/456",
        action_text: "Ver Documento",
        created_at: "2024-01-10T14:15:00Z",
      },
      {
        id: 3,
        title: "Relatório Gerado",
        message: "Relatório financeiro de dezembro/2023 foi gerado",
        type: "system",
        priority: "medium",
        status: "pending",
        action_url: "/reports/101",
        action_text: "Ver Relatório",
        created_at: "2024-01-10T16:20:00Z",
      },
    ]);
  }, []);

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleMarkAsRead = async (notificationId: number) => {
    // TODO: Implement actual API call
    setNotifications(prev =>
      prev.map(notif =>
        notif.id === notificationId
          ? { ...notif, status: "read", read_at: new Date().toISOString() }
          : notif
      )
    );
    setUnreadCount(prev => Math.max(0, prev - 1));
  };

  const handleMarkAllAsRead = async () => {
    // TODO: Implement actual API call
    setLoading(true);
    setTimeout(() => {
      setNotifications(prev =>
        prev.map(notif => ({ ...notif, status: "read", read_at: new Date().toISOString() }))
      );
      setUnreadCount(0);
      setLoading(false);
    }, 500);
  };

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case "high":
        return "error";
      case "medium":
        return "warning";
      case "low":
        return "info";
      default:
        return "default";
    }
  };

  const getTypeIcon = (type: string) => {
    switch (type) {
      case "error":
        return <ErrorIcon color="error" />;
      case "warning":
        return <WarningIcon color="warning" />;
      case "success":
        return <CheckCircleIcon color="success" />;
      default:
        return <InfoIcon color="info" />;
    }
  };

  const formatTimeAgo = (dateString: string) => {
    const now = new Date();
    const date = new Date(dateString);
    const diffInHours = Math.floor((now.getTime() - date.getTime()) / (1000 * 60 * 60));
    
    if (diffInHours < 1) return "Agora";
    if (diffInHours < 24) return `${diffInHours}h atrás`;
    return `${Math.floor(diffInHours / 24)}d atrás`;
  };

  const open = Boolean(anchorEl);

  return (
    <>
      <IconButton
        color="inherit"
        onClick={handleClick}
        aria-label={`${unreadCount} notificações não lidas`}
      >
        <Badge badgeContent={unreadCount} color="error">
          <NotificationsIcon />
        </Badge>
      </IconButton>

      <Popover
        open={open}
        anchorEl={anchorEl}
        onClose={handleClose}
        anchorOrigin={{
          vertical: "bottom",
          horizontal: "right",
        }}
        transformOrigin={{
          vertical: "top",
          horizontal: "right",
        }}
        sx={{
          mt: 1,
          "& .MuiPopover-paper": {
            width: 400,
            maxHeight: 600,
          },
        }}
      >
        <Box sx={{ p: 2 }}>
          <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 1 }}>
            <Typography variant="h6">Notificações</Typography>
            {unreadCount > 0 && (
              <Button
                size="small"
                onClick={handleMarkAllAsRead}
                disabled={loading}
              >
                Marcar todas como lidas
              </Button>
            )}
          </Box>
          
          {notifications.length === 0 ? (
            <Typography variant="body2" color="text.secondary" sx={{ textAlign: "center", py: 4 }}>
              Nenhuma notificação
            </Typography>
          ) : (
            <List sx={{ maxHeight: 400, overflow: "auto" }}>
              {notifications.map((notification, index) => (
                <React.Fragment key={notification.id}>
                  <ListItem
                    alignItems="flex-start"
                    sx={{
                      bgcolor: notification.status === "pending" ? "action.hover" : "transparent",
                      borderRadius: 1,
                      mb: 1,
                    }}
                  >
                    <ListItemAvatar>
                      <Avatar sx={{ bgcolor: "transparent" }}>
                        {getTypeIcon(notification.type)}
                      </Avatar>
                    </ListItemAvatar>
                    <ListItemText
                      primary={
                        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                          <Typography variant="subtitle2" sx={{ fontWeight: notification.status === "pending" ? 600 : 400 }}>
                            {notification.title}
                          </Typography>
                          <Box sx={{ display: "flex", gap: 1, alignItems: "center" }}>
                            <Chip
                              label={notification.priority}
                              size="small"
                              color={getPriorityColor(notification.priority) as any}
                              variant="outlined"
                            />
                            <Typography variant="caption" color="text.secondary">
                              {formatTimeAgo(notification.created_at)}
                            </Typography>
                          </Box>
                        </Box>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="text.secondary" sx={{ mt: 0.5 }}>
                            {notification.message}
                          </Typography>
                          <Box sx={{ mt: 1, display: "flex", gap: 1 }}>
                            {notification.action_url && (
                              <Button
                                size="small"
                                variant="outlined"
                                onClick={() => {
                                  // TODO: Implement navigation
                                  console.log("Navigate to:", notification.action_url);
                                  handleMarkAsRead(notification.id);
                                }}
                              >
                                {notification.action_text || "Ver"}
                              </Button>
                            )}
                            {notification.status === "pending" && (
                              <Button
                                size="small"
                                onClick={() => handleMarkAsRead(notification.id)}
                              >
                                Marcar como lida
                              </Button>
                            )}
                          </Box>
                        </Box>
                      }
                    />
                  </ListItem>
                  {index < notifications.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          )}
        </Box>
      </Popover>
    </>
  );
};

export default NotificationBell;