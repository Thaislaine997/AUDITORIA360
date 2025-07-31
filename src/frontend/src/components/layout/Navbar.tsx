import React from 'react';
import { 
  AppBar, 
  Toolbar, 
  Typography, 
  Box, 
  IconButton,
  Avatar,
  Menu,
  MenuItem,
  Chip,
  Divider,
  Tooltip,
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  AccountCircle as AccountIcon,
  Star,
  Settings,
  Person,
  ExitToApp,
  Search as SearchIcon,
  Notifications as NotificationsIcon,
} from '@mui/icons-material';
import NotificationCenter from '../ui/NotificationCenter';
import CommandPalette from '../ui/CommandPalette';
import { useUIStore } from '../../stores/uiStore';
import { useAuthStore } from '../../stores/authStore';
import { useGamificationStore } from '../../stores/gamificationStore';
import { useNotificationsStore } from '../../stores/notificationsStore';

const Navbar: React.FC = () => {
  const { toggleSidebar } = useUIStore();
  const { user, logout } = useAuthStore();
  const { userProgress } = useGamificationStore();
  const { unreadCount, setCenterOpen, centerOpen } = useNotificationsStore();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [commandPaletteOpen, setCommandPaletteOpen] = React.useState(false);

  // Handle keyboard shortcut for command palette
  React.useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        setCommandPaletteOpen(true);
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

  const handleMenu = (event: React.MouseEvent<HTMLElement>) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  const handleLogout = () => {
    logout();
    handleClose();
  };

  const handleProfile = () => {
    // Navigate to profile page
    window.location.href = '/profile';
    handleClose();
  };

  const handleSettings = () => {
    // Navigate to settings page
    window.location.href = '/settings';
    handleClose();
  };

  const getUserInitials = (name: string) => {
    return name
      .split(' ')
      .map(part => part.charAt(0))
      .join('')
      .toUpperCase()
      .substring(0, 2);
  };

  const handleNotificationToggle = () => {
    setCenterOpen(!centerOpen);
  };

  return (
    <AppBar 
      position="fixed" 
      sx={{ 
        zIndex: (theme) => theme.zIndex.drawer + 1,
        backgroundColor: 'primary.main',
      }}
    >
      <Toolbar>
        <IconButton
          edge="start"
          color="inherit"
          aria-label="toggle sidebar"
          onClick={toggleSidebar}
          sx={{ mr: 2 }}
          title="Menu (Alt+M)"
        >
          <MenuIcon />
        </IconButton>
        
        <Typography 
          variant="h6" 
          noWrap 
          component="div" 
          sx={{ 
            flexGrow: 1,
            fontWeight: 600,
          }}
        >
          AUDITORIA360 - Portal de Gestão da Folha
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          {/* Command Palette Trigger */}
          <Tooltip title="Paleta de Comando (Ctrl+K)">
            <IconButton
              color="inherit"
              onClick={() => setCommandPaletteOpen(true)}
              aria-label="Abrir paleta de comando"
            >
              <SearchIcon />
            </IconButton>
          </Tooltip>

          {/* Notification Bell */}
          <Tooltip title="Central de Notificações">
            <IconButton
              color="inherit"
              onClick={handleNotificationToggle}
              aria-label="Notificações"
            >
              {unreadCount > 0 ? (
                <Box sx={{ position: 'relative' }}>
                  <NotificationsIcon />
                  <Box
                    sx={{
                      position: 'absolute',
                      top: -2,
                      right: -2,
                      minWidth: 16,
                      height: 16,
                      borderRadius: '50%',
                      backgroundColor: 'error.main',
                      color: 'error.contrastText',
                      fontSize: '0.7rem',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      fontWeight: 'bold',
                    }}
                  >
                    {unreadCount > 99 ? '99+' : unreadCount}
                  </Box>
                </Box>
              ) : (
                <NotificationsIcon />
              )}
            </IconButton>
          </Tooltip>
          
          {/* User Level Badge */}
          <Chip
            icon={<Star />}
            label={`Nível ${userProgress.level}`}
            size="small"
            sx={{
              bgcolor: 'warning.main',
              color: 'warning.contrastText',
              fontWeight: 'bold',
            }}
          />
          
          {/* User Menu */}
          <IconButton
            size="large"
            aria-label="account menu"
            aria-controls="menu-appbar"
            aria-haspopup="true"
            onClick={handleMenu}
            color="inherit"
            title="Menu do usuário"
          >
            {user?.avatar ? (
              <Avatar 
                src={user.avatar} 
                alt={user.name || 'User'}
                sx={{ width: 32, height: 32 }}
              />
            ) : (
              <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                {user?.name ? getUserInitials(user.name) : <AccountIcon />}
              </Avatar>
            )}
          </IconButton>
          
          <Menu
            id="menu-appbar"
            anchorEl={anchorEl}
            anchorOrigin={{
              vertical: 'bottom',
              horizontal: 'right',
            }}
            keepMounted
            transformOrigin={{
              vertical: 'top',
              horizontal: 'right',
            }}
            open={Boolean(anchorEl)}
            onClose={handleClose}
            PaperProps={{
              sx: { minWidth: 220 }
            }}
          >
            {/* User Info Header */}
            <MenuItem disabled>
              <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'flex-start' }}>
                <Typography variant="subtitle1" sx={{ fontWeight: 600 }}>
                  {user?.name || 'Usuário'}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  {user?.email}
                </Typography>
                {user?.role && (
                  <Chip 
                    label={user.role.replace('_', ' ')} 
                    size="small" 
                    variant="outlined"
                    sx={{ mt: 0.5 }}
                  />
                )}
              </Box>
            </MenuItem>
            
            <Divider />
            
            {/* XP and Level Info */}
            <MenuItem disabled>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                <Star color="primary" />
                <Box>
                  <Typography variant="body2">
                    Nível {userProgress.level} • {userProgress.currentXP} XP
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    {userProgress.currentXP}/{userProgress.xpToNextLevel} para próximo nível
                  </Typography>
                </Box>
              </Box>
            </MenuItem>
            <Divider />
            
            {/* Menu Items */}
            <MenuItem onClick={handleProfile}>
              <Person sx={{ mr: 1 }} />
              Perfil
            </MenuItem>
            <MenuItem onClick={handleSettings}>
              <Settings sx={{ mr: 1 }} />
              Configurações
            </MenuItem>
            
            <Divider />
            
            <MenuItem onClick={handleLogout}>
              <ExitToApp sx={{ mr: 1 }} />
              Sair
            </MenuItem>
          </Menu>
        </Box>
      </Toolbar>

      {/* Command Palette */}
      <CommandPalette
        open={commandPaletteOpen}
        onClose={() => setCommandPaletteOpen(false)}
      />

      {/* Notification Center */}
      <NotificationCenter />
    </AppBar>
  );
};

export default Navbar;