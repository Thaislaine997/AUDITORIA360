import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
  Box,
  Divider,
  IconButton,
  Collapse,
  Chip,
  Tooltip,
} from '@mui/material';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import {
  Dashboard as DashboardIcon,
  Payment as PaymentIcon,
  Description as DocumentIcon,
  Gavel as GavelIcon,
  Assessment as AuditIcon,
  Chat as ChatIcon,
  Assignment as ReportIcon,
  Star as StarIcon,
  StarBorder as StarBorderIcon,
  History as HistoryIcon,
  ExpandLess,
  ExpandMore,
  ChevronLeft,
  ChevronRight,
} from '@mui/icons-material';
import { useUIStore } from '../../stores/uiStore';
import { useNavigationStore } from '../../stores/navigationStore';

const drawerWidth = 240;
const collapsedWidth = 60;

const getIconByName = (iconName: string) => {
  const iconMap: Record<string, React.ReactNode> = {
    'DashboardIcon': <DashboardIcon />,
    'PaymentIcon': <PaymentIcon />,
    'DocumentIcon': <DocumentIcon />,
    'GavelIcon': <GavelIcon />,
    'AuditIcon': <AuditIcon />,
    'ChatIcon': <ChatIcon />,
    'ReportIcon': <ReportIcon />,
  };
  return iconMap[iconName] || <DashboardIcon />;
};

const menuItems = [
  { path: '/dashboard', label: 'Dashboard', icon: 'DashboardIcon', exact: true },
  { path: '/payroll', label: 'Folha de Pagamento', icon: 'PaymentIcon' },
  { path: '/documents', label: 'Documentos', icon: 'DocumentIcon' },
  { path: '/cct', label: 'CCT', icon: 'GavelIcon' },
  { path: '/audit', label: 'Auditoria', icon: 'AuditIcon' },
  { path: '/reports/templates', label: 'Modelos de Relatório', icon: 'ReportIcon', exact: true },
  { path: '/chatbot', label: 'Chatbot', icon: 'ChatIcon', exact: true },
];

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { sidebarOpen, setSidebarOpen } = useUIStore();
  const { 
    favorites, 
    recentlyAccessed, 
    sidebarCollapsed, 
    addToFavorites, 
    removeFromFavorites, 
    isFavorite, 
    recordAccess,
    setSidebarCollapsed,
    getRecentlyAccessed
  } = useNavigationStore();
  
  const [favoritesExpanded, setFavoritesExpanded] = React.useState(true);
  const [recentExpanded, setRecentExpanded] = React.useState(true);
  
  const currentWidth = sidebarCollapsed ? collapsedWidth : drawerWidth;

  const isActiveRoute = (itemPath: string, exact?: boolean) => {
    if (exact) {
      return location.pathname === itemPath;
    }
    return location.pathname.startsWith(itemPath);
  };

  const handleNavigation = (path: string, label: string, icon: string) => {
    // Record access for analytics and recent items
    recordAccess({ path, label, icon, accessCount: 0 });
    navigate(path);
  };

  const handleFavoriteToggle = (item: typeof menuItems[0], event: React.MouseEvent) => {
    event.preventDefault();
    event.stopPropagation();
    
    const navItem = { path: item.path, label: item.label, icon: item.icon, accessCount: 0 };
    
    if (isFavorite(item.path)) {
      removeFromFavorites(item.path);
    } else {
      addToFavorites(navItem);
    }
  };

  const toggleSidebarCollapse = () => {
    setSidebarCollapsed(!sidebarCollapsed);
  };

  const recentItems = getRecentlyAccessed(3);

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: sidebarOpen ? currentWidth : 0,
        flexShrink: 0,
        transition: 'width 0.3s ease',
        [`& .MuiDrawer-paper`]: { 
          width: sidebarOpen ? currentWidth : 0,
          boxSizing: 'border-box',
          transition: 'width 0.3s ease',
          overflow: 'hidden',
        },
      }}
    >
      <Toolbar />
      
      {sidebarOpen && (
        <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
          {/* Collapse/Expand Button */}
          <Box sx={{ display: 'flex', justifyContent: 'flex-end', p: 1 }}>
            <Tooltip title={sidebarCollapsed ? 'Expandir Menu' : 'Recolher Menu'}>
              <IconButton 
                onClick={toggleSidebarCollapse}
                size="small"
                sx={{ color: 'text.secondary' }}
              >
                {sidebarCollapsed ? <ChevronRight /> : <ChevronLeft />}
              </IconButton>
            </Tooltip>
          </Box>

          <Box sx={{ overflow: 'auto', flex: 1 }}>
            {/* Favorites Section */}
            {!sidebarCollapsed && favorites.length > 0 && (
              <>
                <ListItem disablePadding>
                  <ListItemButton onClick={() => setFavoritesExpanded(!favoritesExpanded)}>
                    <ListItemIcon>
                      <StarIcon color="warning" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Favoritos" 
                      primaryTypographyProps={{ variant: 'subtitle2', fontWeight: 600 }}
                    />
                    {favoritesExpanded ? <ExpandLess /> : <ExpandMore />}
                  </ListItemButton>
                </ListItem>
                <Collapse in={favoritesExpanded} timeout="auto" unmountOnExit>
                  <List component="div" disablePadding>
                    {favorites.map((item) => (
                      <ListItem key={`fav-${item.path}`} disablePadding sx={{ pl: 2 }}>
                        <ListItemButton
                          component={Link}
                          to={item.path}
                          selected={isActiveRoute(item.path)}
                          onClick={() => handleNavigation(item.path, item.label, item.icon)}
                          sx={{
                            '&.Mui-selected': {
                              backgroundColor: 'primary.main',
                              color: 'primary.contrastText',
                              '& .MuiListItemIcon-root': {
                                color: 'primary.contrastText',
                              },
                            },
                          }}
                        >
                          <ListItemIcon sx={{ minWidth: 40 }}>
                            {getIconByName(item.icon)}
                          </ListItemIcon>
                          <ListItemText 
                            primary={item.label}
                            primaryTypographyProps={{ fontSize: '0.875rem' }}
                          />
                        </ListItemButton>
                      </ListItem>
                    ))}
                  </List>
                </Collapse>
                <Divider />
              </>
            )}

            {/* Recent Access Section */}
            {!sidebarCollapsed && recentItems.length > 0 && (
              <>
                <ListItem disablePadding>
                  <ListItemButton onClick={() => setRecentExpanded(!recentExpanded)}>
                    <ListItemIcon>
                      <HistoryIcon color="action" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Recente" 
                      primaryTypographyProps={{ variant: 'subtitle2', fontWeight: 600 }}
                    />
                    {recentExpanded ? <ExpandLess /> : <ExpandMore />}
                  </ListItemButton>
                </ListItem>
                <Collapse in={recentExpanded} timeout="auto" unmountOnExit>
                  <List component="div" disablePadding>
                    {recentItems.map((item, index) => (
                      <ListItem key={`recent-${item.path}-${index}`} disablePadding sx={{ pl: 2 }}>
                        <ListItemButton
                          component={Link}
                          to={item.path}
                          selected={isActiveRoute(item.path)}
                          onClick={() => handleNavigation(item.path, item.label, item.icon)}
                          sx={{
                            '&.Mui-selected': {
                              backgroundColor: 'primary.main',
                              color: 'primary.contrastText',
                              '& .MuiListItemIcon-root': {
                                color: 'primary.contrastText',
                              },
                            },
                          }}
                        >
                          <ListItemIcon sx={{ minWidth: 40 }}>
                            {getIconByName(item.icon)}
                          </ListItemIcon>
                          <ListItemText 
                            primary={item.label}
                            primaryTypographyProps={{ fontSize: '0.875rem' }}
                          />
                          <Chip 
                            label={item.accessCount} 
                            size="small" 
                            sx={{ ml: 1, height: 16, fontSize: '0.65rem' }}
                          />
                        </ListItemButton>
                      </ListItem>
                    ))}
                  </List>
                </Collapse>
                <Divider />
              </>
            )}

            {/* Main Navigation */}
            <List>
              {!sidebarCollapsed && (
                <ListItem disablePadding>
                  <ListItemText 
                    primary="Navegação Principal" 
                    primaryTypographyProps={{ 
                      variant: 'subtitle2', 
                      fontWeight: 600, 
                      pl: 2,
                      py: 1,
                      color: 'text.secondary'
                    }}
                  />
                </ListItem>
              )}
              
              {menuItems.map((item) => (
                <ListItem key={item.path} disablePadding>
                  <ListItemButton
                    component={Link}
                    to={item.path}
                    selected={isActiveRoute(item.path, item.exact)}
                    onClick={() => handleNavigation(item.path, item.label, item.icon)}
                    sx={{
                      justifyContent: sidebarCollapsed ? 'center' : 'flex-start',
                      px: sidebarCollapsed ? 1 : 2,
                      '&.Mui-selected': {
                        backgroundColor: 'primary.main',
                        color: 'primary.contrastText',
                        '&:hover': {
                          backgroundColor: 'primary.dark',
                        },
                        '& .MuiListItemIcon-root': {
                          color: 'primary.contrastText',
                        },
                      },
                    }}
                    aria-label={`Navegar para ${item.label}`}
                  >
                    <ListItemIcon 
                      sx={{ 
                        minWidth: sidebarCollapsed ? 'auto' : 56,
                        justifyContent: 'center'
                      }}
                    >
                      {getIconByName(item.icon)}
                    </ListItemIcon>
                    
                    {!sidebarCollapsed && (
                      <>
                        <ListItemText 
                          primary={item.label}
                          primaryTypographyProps={{
                            fontWeight: isActiveRoute(item.path, item.exact) ? 600 : 400,
                          }}
                        />
                        
                        <Tooltip title={isFavorite(item.path) ? 'Remover dos favoritos' : 'Adicionar aos favoritos'}>
                          <IconButton
                            size="small"
                            onClick={(e) => handleFavoriteToggle(item, e)}
                            sx={{ 
                              opacity: 0.7,
                              '&:hover': { opacity: 1 },
                              color: 'inherit'
                            }}
                          >
                            {isFavorite(item.path) ? (
                              <StarIcon sx={{ fontSize: 16, color: 'warning.main' }} />
                            ) : (
                              <StarBorderIcon sx={{ fontSize: 16 }} />
                            )}
                          </IconButton>
                        </Tooltip>
                      </>
                    )}
                  </ListItemButton>
                </ListItem>
              ))}
            </List>
          </Box>
        </Box>
      )}
    </Drawer>
  );
};

export default Sidebar;