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
} from '@mui/icons-material';
import { useUIStore } from '../../stores/uiStore';

const drawerWidth = 240;

const menuItems = [
  { path: '/dashboard', label: 'Dashboard', icon: <DashboardIcon />, exact: true },
  { path: '/payroll', label: 'Folha de Pagamento', icon: <PaymentIcon /> },
  { path: '/documents', label: 'Documentos', icon: <DocumentIcon /> },
  { path: '/cct', label: 'CCT', icon: <GavelIcon /> },
  { path: '/audit', label: 'Auditoria', icon: <AuditIcon /> },
  { path: '/reports/templates', label: 'Modelos de Relatório', icon: <ReportIcon />, exact: true },
  { path: '/chatbot', label: 'Chatbot', icon: <ChatIcon />, exact: true },
];

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();
  const { sidebarOpen, setCurrentPage } = useUIStore();

  const isActiveRoute = (itemPath: string, exact?: boolean) => {
    if (exact) {
      return location.pathname === itemPath;
    }
    return location.pathname.startsWith(itemPath);
  };

  const handleNavigation = (path: string) => {
    setCurrentPage(path);
    navigate(path);
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
          <List>
            {menuItems.map((item) => (
              <ListItem key={item.path} disablePadding>
                <ListItemButton
                  component={Link}
                  to={item.path}
                  selected={isActiveRoute(item.path, item.exact)}
                  onClick={() => handleNavigation(item.path)}
                  sx={{
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
                  <ListItemIcon>{item.icon}</ListItemIcon>
                  <ListItemText 
                    primary={item.label}
                    primaryTypographyProps={{
                      fontWeight: isActiveRoute(item.path, item.exact) ? 600 : 400,
                    }}
                  />
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        </Box>
      )}
    </Drawer>
  );
};

export default Sidebar;