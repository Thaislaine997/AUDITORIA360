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


];

const Sidebar: React.FC = () => {
  const navigate = useNavigate();
  const location = useLocation();


  const isActiveRoute = (itemPath: string, exact?: boolean) => {
    if (exact) {
      return location.pathname === itemPath;
    }
    return location.pathname.startsWith(itemPath);
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

        </Box>
      )}
    </Drawer>
  );
};

export default Sidebar;