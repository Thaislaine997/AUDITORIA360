import React, { useState } from 'react';
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
  Collapse,
  Divider,
} from '@mui/material';
import { NavLink, useLocation } from 'react-router-dom';
import {
  Dashboard as DashboardIcon,
  Business as BusinessIcon,
  Assignment as AssignmentIcon,
  Psychology as PsychologyIcon,
  People as PeopleIcon,
  AccountBalance as AccountBalanceIcon,
  Assessment as AssessmentIcon,
  Settings as SettingsIcon,
  AccountCircle as AccountCircleIcon,
  Description as DescriptionIcon,
  Gavel as GavelIcon,
  SmartToy as SmartToyIcon,
  ExpandLess,
  ExpandMore,
} from '@mui/icons-material';
import { useUIStore } from '../../stores/uiStore';
import { useNavigationStore } from '../../stores/navigationStore';
import { useAuthStore } from '../../stores/authStore';

const drawerWidth = 240;
const collapsedWidth = 60;

interface MenuItem {
  label: string;
  path?: string;
  icon: React.ReactNode;
  children?: MenuItem[];
  roles?: string[]; // roles that can access this item
}

const navigationItems: MenuItem[] = [
  {
    label: 'OPERAÇÃO',
    icon: <BusinessIcon />,
    children: [
      {
        label: 'Dashboard',
        path: '/dashboard',
        icon: <DashboardIcon />,
      },
      {
        label: 'Portal de Demandas',
        path: '/demandas',
        icon: <AssignmentIcon />,
      },
      {
        label: 'Consultor de Riscos',
        path: '/consultor-riscos',
        icon: <PsychologyIcon />,
      },
      {
        label: 'Gestão de Legislação',
        path: '/gestao-legislacao',
        icon: <GavelIcon />,
      },
      {
        label: 'Validação de IA',
        path: '/validacao-ia',
        icon: <SmartToyIcon />,
      },
    ],
  },
  {
    label: 'GESTÃO',
    icon: <PeopleIcon />,
    children: [
      {
        label: 'Contabilidades',
        path: '/gestao/contabilidades',
        icon: <AccountBalanceIcon />,
        roles: ['super_admin'], // Only super admin can access
      },
      {
        label: 'Clientes',
        path: '/gestao/clientes',
        icon: <BusinessIcon />,
        roles: ['super_admin', 'contabilidade'], // Gestors and super admin
      },
      {
        label: 'Usuários',
        path: '/gestao/usuarios',
        icon: <PeopleIcon />,
        roles: ['super_admin'], // Only super admin can manage users
      },
    ],
  },
  {
    label: 'RELATÓRIOS',
    icon: <AssessmentIcon />,
    children: [
      {
        label: 'Relatórios Avançados',
        path: '/relatorios/avancados',
        icon: <AssessmentIcon />,
      },
    ],
  },
  {
    label: 'CONFIGURAÇÕES',
    icon: <SettingsIcon />,
    children: [
      {
        label: 'Minha Conta',
        path: '/configuracoes/minha-conta',
        icon: <AccountCircleIcon />,
      },
      {
        label: 'Templates',
        path: '/configuracoes/templates',
        icon: <DescriptionIcon />,
        roles: ['super_admin', 'contabilidade'], // Gestors and super admin
      },
    ],
  },
];

const Sidebar: React.FC = () => {
  const location = useLocation();
  const { sidebarOpen } = useUIStore();
  const { sidebarCollapsed } = useNavigationStore();
  const { user } = useAuthStore();
  
  const [expandedItems, setExpandedItems] = useState<string[]>(['OPERAÇÃO']); // Default expand operation

  const currentWidth = sidebarCollapsed ? collapsedWidth : drawerWidth;

  const isActiveRoute = (itemPath: string, exact?: boolean) => {
    if (exact) {
      return location.pathname === itemPath;
    }
    return location.pathname.startsWith(itemPath);
  };

  const hasPermission = (item: MenuItem): boolean => {
    if (!item.roles || item.roles.length === 0) {
      return true; // No role restriction
    }
    
    if (!user?.role) {
      return false; // User has no role
    }
    
    return item.roles.includes(user.role);
  };

  const toggleExpanded = (label: string) => {
    setExpandedItems(prev => 
      prev.includes(label) 
        ? prev.filter(item => item !== label)
        : [...prev, label]
    );
  };

  const getActiveParent = (): string | null => {
    for (const item of navigationItems) {
      if (item.children) {
        for (const child of item.children) {
          if (child.path && isActiveRoute(child.path)) {
            return item.label;
          }
        }
      }
    }
    return null;
  };

  React.useEffect(() => {
    // Auto-expand parent of active route
    const activeParent = getActiveParent();
    if (activeParent && !expandedItems.includes(activeParent)) {
      setExpandedItems(prev => [...prev, activeParent]);
    }
  }, [location.pathname]);

  const renderMenuItem = (item: MenuItem, depth = 0) => {
    const isExpanded = expandedItems.includes(item.label);
    const hasChildren = item.children && item.children.length > 0;
    const isParentActive = hasChildren && item.children.some(child => 
      child.path && isActiveRoute(child.path)
    );

    // Filter children based on permissions
    const allowedChildren = item.children?.filter(hasPermission) || [];

    if (item.path) {
      // Leaf item with direct path
      if (!hasPermission(item)) {
        return null; // Hide if no permission
      }

      return (
        <ListItem key={item.label} disablePadding sx={{ pl: depth * 2 }}>
          <ListItemButton
            component={NavLink}
            to={item.path}
            sx={{
              minHeight: 48,
              bgcolor: isActiveRoute(item.path, true) ? 'primary.main' : 'transparent',
              color: isActiveRoute(item.path, true) ? 'white' : 'text.primary',
              '&:hover': {
                bgcolor: isActiveRoute(item.path, true) ? 'primary.dark' : 'action.hover',
              },
              '&.active': {
                bgcolor: 'primary.main',
                color: 'white',
              },
            }}
          >
            <ListItemIcon
              sx={{
                minWidth: 40,
                color: isActiveRoute(item.path, true) ? 'white' : 'text.secondary',
              }}
            >
              {item.icon}
            </ListItemIcon>
            {!sidebarCollapsed && (
              <ListItemText 
                primary={item.label}
                primaryTypographyProps={{
                  fontSize: depth > 0 ? '0.875rem' : '1rem',
                  fontWeight: isActiveRoute(item.path, true) ? 600 : 400,
                }}
              />
            )}
          </ListItemButton>
        </ListItem>
      );
    }

    // Parent item with children
    if (allowedChildren.length === 0) {
      return null; // Hide if no accessible children
    }

    return (
      <React.Fragment key={item.label}>
        <ListItem disablePadding sx={{ pl: depth * 2 }}>
          <ListItemButton
            onClick={() => toggleExpanded(item.label)}
            sx={{
              minHeight: 48,
              bgcolor: isParentActive ? 'action.selected' : 'transparent',
              '&:hover': {
                bgcolor: 'action.hover',
              },
            }}
          >
            <ListItemIcon sx={{ minWidth: 40, color: 'text.secondary' }}>
              {item.icon}
            </ListItemIcon>
            {!sidebarCollapsed && (
              <>
                <ListItemText 
                  primary={item.label}
                  primaryTypographyProps={{
                    fontSize: '0.875rem',
                    fontWeight: 600,
                    color: 'text.secondary',
                    letterSpacing: '0.1em',
                  }}
                />
                {isExpanded ? <ExpandLess /> : <ExpandMore />}
              </>
            )}
          </ListItemButton>
        </ListItem>
        
        {!sidebarCollapsed && (
          <Collapse in={isExpanded} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {allowedChildren.map(child => renderMenuItem(child, depth + 1))}
            </List>
          </Collapse>
        )}
      </React.Fragment>
    );
  };

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
        <Box sx={{ overflow: 'auto', height: '100%' }}>
          <List sx={{ pt: 1 }}>
            {navigationItems.map(item => renderMenuItem(item))}
          </List>
        </Box>
      )}
    </Drawer>
  );
};

export default Sidebar;