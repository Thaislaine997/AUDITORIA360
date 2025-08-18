import React, { useState } from 'react';
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
import { useNotificationsStore } from '../../stores/notificationsStore';


import { Dialog, DialogTitle, DialogContent, InputBase, Paper, List, ListItem, ListItemText, IconButton as MuiIconButton } from '@mui/material';
import { useGlobalSearch } from '../../lib/hooks/useGlobalSearch';

const Navbar: React.FC = () => {
  const { toggleSidebar } = useUIStore();
  const { user, logout } = useAuthStore();
  const { unreadCount, setCenterOpen, centerOpen } = useNotificationsStore();
  const [anchorEl, setAnchorEl] = React.useState<null | HTMLElement>(null);
  const [commandPaletteOpen, setCommandPaletteOpen] = React.useState(false);
  const [globalSearchOpen, setGlobalSearchOpen] = useState(false);
  const [globalSearch, setGlobalSearch] = useState('');
  // Busca global real
  const globalResults = useGlobalSearch(globalSearch);
  // Atalho Ctrl+Shift+F para abrir busca global
  React.useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.key.toLowerCase() === 'f') {
        event.preventDefault();
        setGlobalSearchOpen(true);
      }
    };
    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, []);

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
          {/* Pesquisa Global */}
          <Tooltip title="Busca global (Ctrl+Shift+F)">
            <MuiIconButton color="inherit" onClick={() => setGlobalSearchOpen(true)}>
              <SearchIcon />
            </MuiIconButton>
          </Tooltip>
      {/* Modal de Pesquisa Global */}
      <Dialog open={globalSearchOpen} onClose={() => setGlobalSearchOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Pesquisa Global</DialogTitle>
        <DialogContent>
          <Paper sx={{ p: 1, mb: 2, display: 'flex', alignItems: 'center' }}>
            <SearchIcon sx={{ mr: 1 }} />
            <InputBase
              autoFocus
              placeholder="Digite para buscar em tickets, auditorias, relatórios..."
              value={globalSearch}
              onChange={e => setGlobalSearch(e.target.value)}
              fullWidth
              sx={{ fontSize: 18 }}
            />
          </Paper>
          <List>
            {globalResults.length === 0 && globalSearch && (
              <ListItem><ListItemText primary="Nenhum resultado encontrado." /></ListItem>
            )}
            {globalResults.map(r => (
              <ListItem button component="a" href={r.path} key={r.path} onClick={() => setGlobalSearchOpen(false)}>
                <ListItemText primary={r.label} />
              </ListItem>
            ))}
          </List>
        </DialogContent>
      </Dialog>
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
          
          {/* Chip de gamificação removido */}
          
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
            <Avatar sx={{ width: 32, height: 32, bgcolor: 'secondary.main' }}>
              {user?.name ? getUserInitials(user.name) : <AccountIcon />}
            </Avatar>
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
            
            {/* Info de XP/Nível removida */}
            
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