import React from "react";
import { AppBar, Toolbar, Typography, Box } from "@mui/material";

const Navbar: React.FC = () => {
  return (
    <AppBar position="fixed" sx={{ zIndex: theme => theme.zIndex.drawer + 1 }}>
      <Toolbar>
        <Typography variant="h6" noWrap component="div">
          AUDITORIA360 - Portal de Gestão da Folha
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Navbar;
