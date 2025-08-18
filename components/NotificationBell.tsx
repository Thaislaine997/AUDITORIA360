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
import { useUIStore } from "../stores/uiStore";

const NotificationBell: React.FC = () => {
  const [anchorEl, setAnchorEl] = useState<HTMLButtonElement | null>(null);
  const [loading, setLoading] = useState(false);
  const { notifications, addNotification, removeNotification, clearNotifications } = useUIStore();

  // Mock data for demonstration - TODO: Replace with actual API calls
  useEffect(() => {
    // Add some demo notifications
    addNotification({
      message: "A contabilidade 'Escritório Santos & Associados' se cadastrou na plataforma",
      type: "info",
    });
    addNotification({
      message: "Cliente 'Empresa ABC Ltda' enviou um novo documento",
      type: "warning",
    });
    addNotification({
      message: "Relatório financeiro de dezembro/2023 foi gerado",
      type: "success",
    });
  }, [addNotification]);

  const unreadCount = notifications.length;

  const handleClick = (event: React.MouseEvent<HTMLButtonElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleMarkAsRead = async (notificationId: string) => {
    removeNotification(notificationId);
  };

  const handleMarkAllAsRead = async () => {
    setLoading(true);
    setTimeout(() => {
      clearNotifications();
      setLoading(false);
    }, 500);
  };

  const getPriorityColor = (type: string) => {
    switch (type) {
      case "error":
        return "error";
      case "warning":
        return "warning";
      case "success":
        return "success";
      case "info":
      default:
        return "info";
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

  const formatTimeAgo = (date: Date) => {
    const now = new Date();
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
                      bgcolor: "action.hover",
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
                          <Typography variant="subtitle2" sx={{ fontWeight: 600 }}>
                            Notificação
                          </Typography>
                          <Box sx={{ display: "flex", gap: 1, alignItems: "center" }}>
                            <Chip
                              label={notification.type}
                              size="small"
                              color={getPriorityColor(notification.type) as any}
                              variant="outlined"
                            />
                            <Typography variant="caption" color="text.secondary">
                              {formatTimeAgo(notification.timestamp)}
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
                            <Button
                              size="small"
                              onClick={() => handleMarkAsRead(notification.id)}
                            >
                              Marcar como lida
                            </Button>
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