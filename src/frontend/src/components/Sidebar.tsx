import React from 'react';
import {
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
} from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import {
  Dashboard as DashboardIcon,
  Payment as PaymentIcon,
  Description as DocumentIcon,
  Gavel as GavelIcon,
  Assessment as AuditIcon,
  Chat as ChatIcon,
} from '@mui/icons-material';

const drawerWidth = 240;

const menuItems = [
  { path: '/dashboard', label: 'Dashboard', icon: <DashboardIcon /> },
  { path: '/payroll', label: 'Folha de Pagamento', icon: <PaymentIcon /> },
  { path: '/documents', label: 'Documentos', icon: <DocumentIcon /> },
  { path: '/cct', label: 'CCT', icon: <GavelIcon /> },
  { path: '/audit', label: 'Auditoria', icon: <AuditIcon /> },
  { path: '/chatbot', label: 'Chatbot', icon: <ChatIcon /> },
];

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <Drawer
      variant="permanent"
      sx={{
        width: drawerWidth,
        flexShrink: 0,
        [`& .MuiDrawer-paper`]: { width: drawerWidth, boxSizing: 'border-box' },
      }}
    >
      <Toolbar />
      <List>
        {menuItems.map((item) => (
          <ListItem key={item.path} disablePadding>
            <ListItemButton
              selected={location.pathname.startsWith(item.path)}
              onClick={() => navigate(item.path)}
            >
              <ListItemIcon>{item.icon}</ListItemIcon>
              <ListItemText primary={item.label} />
            </ListItemButton>
          </ListItem>
        ))}
      </List>
    </Drawer>
  );
};

export default Sidebar;