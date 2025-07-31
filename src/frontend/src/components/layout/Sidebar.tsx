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
  Collapse,
  Divider,
} from '@mui/material';
import { useNavigate, useLocation, Link } from 'react-router-dom';
import {
  Dashboard as DashboardIcon,
  Assignment as AssignmentIcon,
  Psychology as PsychologyIcon,
  Business as BusinessIcon,
  People as PeopleIcon,
  PersonAdd as PersonAddIcon,
  Assessment as AssessmentIcon,
  AccountCircle as AccountCircleIcon,
  Description as DescriptionIcon,
  ExpandLess,
  ExpandMore,
  TrendingUp,
  Security,
  Settings,
  Assignment as ReportsIcon,
} from '@mui/icons-material';
import { useUIStore } from '../../stores/uiStore';
import { useAuthStore } from '../../stores/authStore';

const drawerWidth = 240;

interface MenuItem {
  path: string;
  label: string;
  icon: React.ReactNode;
  exact?: boolean;
  roles?: string[];
  children?: MenuItem[];
}

const menuItems: MenuItem[] = [
  {
    path: '/operacao',
    label: 'OPERAÇÃO',
    icon: <TrendingUp />,
    children: [
      { path: '/dashboard', label: 'Dashboard', icon: <DashboardIcon />, exact: true },
      { path: '/demandas', label: 'Portal de Demandas', icon: <AssignmentIcon /> },
      { path: '/consultor-riscos', label: 'Consultor de Riscos', icon: <PsychologyIcon /> },
    ],
  },
  {
    path: '/gestao',
    label: 'GESTÃO',
    icon: <Security />,
    children: [
      { 
        path: '/gestao/contabilidades', 
        label: 'Gestão de Contabilidades', 
        icon: <BusinessIcon />,
        roles: ['super_admin']
      },
      { 
        path: '/gestao/clientes', 
        label: 'Gestão de Clientes', 
        icon: <PeopleIcon />,
        roles: ['super_admin', 'contabilidade']
      },
      { 
        path: '/gestao/usuarios', 
        label: 'Gerenciamento de Usuários', 
        icon: <PersonAddIcon />,
        roles: ['super_admin', 'contabilidade']
      },
    ],
  },
  {
    path: '/relatorios',
    label: 'RELATÓRIOS',
    icon: <ReportsIcon />,
    children: [
      { path: '/relatorios/avancados', label: 'Relatórios Avançados', icon: <AssessmentIcon /> },
    ],
  },
  {
    path: '/configuracoes',
    label: 'CONFIGURAÇÕES',
    icon: <Settings />,
    children: [
      { path: '/configuracoes/minha-conta', label: 'Minha Conta', icon: <AccountCircleIcon /> },
      { path: '/configuracoes/templates', label: 'Templates', icon: <DescriptionIcon /> },
    ],
  },
];

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { sidebarOpen, setCurrentPage } = useUIStore();
  const { user } = useAuthStore();
  const [openSubmenus, setOpenSubmenus] = React.useState<{ [key: string]: boolean }>({
    '/operacao': true, // Start with operations open by default
  });

  const isActiveRoute = (itemPath: string, exact?: boolean) => {
    if (exact) {
      return location.pathname === itemPath;
    }
    return location.pathname.startsWith(itemPath);
  };

  const hasPermission = (roles?: string[]) => {
    if (!roles || roles.length === 0) return true;
    return roles.includes(user?.role || '');
  };

  const handleNavigation = (path: string) => {
    setCurrentPage(path);
    navigate(path);
  };

  const handleSubmenuToggle = (path: string) => {
    setOpenSubmenus(prev => ({
      ...prev,
      [path]: !prev[path],
    }));
  };

  const renderMenuItem = (item: MenuItem, isChild = false) => {
    if (!hasPermission(item.roles)) {
      return null;
    }

    const isActive = isActiveRoute(item.path, item.exact);
    const hasChildren = item.children && item.children.length > 0;
    const isSubmenuOpen = openSubmenus[item.path];

    if (hasChildren) {
      return (
        <React.Fragment key={item.path}>
          <ListItem disablePadding>
            <ListItemButton
              onClick={() => handleSubmenuToggle(item.path)}
              sx={{
                pl: isChild ? 4 : 2,
                '&:hover': {
                  backgroundColor: 'action.hover',
                },
              }}
            >
              <ListItemIcon sx={{ minWidth: 40 }}>
                {item.icon}
              </ListItemIcon>
              <ListItemText 
                primary={item.label}
                primaryTypographyProps={{
                  fontSize: isChild ? '0.875rem' : '0.875rem',
                  fontWeight: isChild ? 400 : 600,
                  color: isChild ? 'text.primary' : 'text.primary',
                }}
              />
              {isSubmenuOpen ? <ExpandLess /> : <ExpandMore />}
            </ListItemButton>
          </ListItem>
          <Collapse in={isSubmenuOpen} timeout="auto" unmountOnExit>
            <List component="div" disablePadding>
              {item.children?.map(child => renderMenuItem(child, true))}
            </List>
          </Collapse>
        </React.Fragment>
      );
    }

    return (
      <ListItem key={item.path} disablePadding>
        <ListItemButton
          component={Link}
          to={item.path}
          selected={isActive}
          onClick={() => handleNavigation(item.path)}
          sx={{
            pl: isChild ? 6 : 2,
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
            '&:hover': {
              backgroundColor: isActive ? 'primary.dark' : 'action.hover',
            },
          }}
          aria-label={`Navegar para ${item.label}`}
        >
          <ListItemIcon sx={{ minWidth: 40 }}>
            {item.icon}
          </ListItemIcon>
          <ListItemText 
            primary={item.label}
            primaryTypographyProps={{
              fontSize: '0.875rem',
              fontWeight: isActive ? 600 : 400,
            }}
          />
        </ListItemButton>
      </ListItem>
    );
  };

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: sidebarOpen ? drawerWidth : 0,
        flexShrink: 0,
        transition: 'width 0.3s ease',
        [`& .MuiDrawer-paper`]: { 
          width: sidebarOpen ? drawerWidth : 0,
          boxSizing: 'border-box',
          transition: 'width 0.3s ease',
          overflow: 'hidden',
        },
      }}
    >
      <Toolbar />
      {sidebarOpen && (
        <Box sx={{ overflow: 'auto', flex: 1 }}>
          <Box sx={{ p: 2 }}>
            <Typography 
              variant="h6" 
              sx={{ 
                color: 'primary.main',
                fontWeight: 700,
                fontSize: '1rem',
                textAlign: 'center',
                borderBottom: 1,
                borderColor: 'divider',
                pb: 1,
                mb: 2,
              }}
            >
              📊 AUDITORIA360
            </Typography>
          </Box>
          <List>
            {menuItems.map(item => renderMenuItem(item))}
          </List>
        </Box>
      )}
    </Drawer>
  );
};

export default Sidebar;