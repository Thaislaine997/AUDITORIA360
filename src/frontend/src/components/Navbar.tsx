import React from "react";
import { AppBar, Toolbar, Typography, Box } from "@mui/material";
import NotificationBell from "./NotificationBell";

const Navbar: React.FC = () => {
  return (
    <AppBar position="fixed" sx={{ zIndex: theme => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          AUDITORIA360 - Portal de Gestão da Folha
        </Typography>
        <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
          <NotificationBell />
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
