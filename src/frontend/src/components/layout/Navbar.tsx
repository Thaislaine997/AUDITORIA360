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
} from '@mui/material';
import { 
  Menu as MenuIcon, 
  AccountCircle as AccountIcon,
  Star,
  Settings,
  Person,
  ExitToApp,
} from '@mui/icons-material';
import NotificationCenter from '../ui/NotificationCenter';
import { useUIStore } from '../../stores/uiStore';
import { useAuthStore } from '../../stores/authStore';

const Navbar: React.FC = () => {
  const { toggleSidebar } = useUIStore();
  const { user, logout } = useAuthStore();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);

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

  const getUserLevel = () => {
    return user?.xp_points ? Math.floor(user.xp_points / 1000) + 1 : 1;
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
          {/* Notification Center */}
          <NotificationCenter />
          
          {/* User Level Badge */}
          {user?.xp_points && (
            <Chip
              icon={<Star />}
              label={`Nível ${getUserLevel()}`}
              size="small"
              sx={{
                bgcolor: 'warning.main',
                color: 'warning.contrastText',
                fontWeight: 'bold',
              }}
            />
          )}
          
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
                alt={user.full_name || 'User'}
                sx={{ width: 32, height: 32 }}
              />
            ) : (
              <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
                {user?.full_name ? getUserInitials(user.full_name) : <AccountIcon />}
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
                  {user?.full_name || 'Usuário'}
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
            {user?.xp_points && (
              <>
                <MenuItem disabled>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                    <Star color="primary" />
                    <Box>
                      <Typography variant="body2">
                        Nível {getUserLevel()} • {user.xp_points} XP
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {user.total_missions_completed || 0} missões completadas
                      </Typography>
                    </Box>
                  </Box>
                </MenuItem>
                <Divider />
              </>
            )}
            
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
    </AppBar>
  );
};

export default Navbar;