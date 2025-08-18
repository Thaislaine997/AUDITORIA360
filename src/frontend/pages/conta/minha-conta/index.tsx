import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  Grid,
  Card,
  CardContent,
  TextField,
  Button,
  Avatar,
  Divider,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Switch,
  FormControlLabel,
  Alert,
  Tab,
  Tabs,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import {
  Person,
  Email,
  Phone,
  Lock,
  Notifications,
  Security,
  Visibility,
  Save,
  Edit,
} from "@mui/icons-material";
import { useAuthStore } from "../../stores/authStore";

const MinhaConta: React.FC = () => {
  const { user } = useAuthStore();
  const [tabValue, setTabValue] = useState(0);
  const [openPasswordDialog, setOpenPasswordDialog] = useState(false);
  const [notifications, setNotifications] = useState({
    email: true,
    push: false,
    sms: false,
  });

  const [userInfo, setUserInfo] = useState({
    nome: user?.name || "",
    email: user?.email || "",
    telefone: "(11) 99999-9999",
    cargo: "Administrador",
    empresa: "AUDITORIA360",
  });

  const handleSave = () => {
    // Save user information
    console.log("Salvando informações do usuário:", userInfo);
  };

  const handleNotificationChange = (setting: string) => {
    setNotifications(prev => ({
      ...prev,
      [setting]: !prev[setting as keyof typeof prev],
    }));
  };

  const securitySettings = [
    {
      title: "Autenticação de Dois Fatores",
      description: "Adicione uma camada extra de segurança à sua conta",
      enabled: false,
      icon: <Security />,
    },
    {
      title: "Sessões Ativas",
      description: "Gerencie seus dispositivos conectados",
      enabled: true,
      icon: <Visibility />,
    },
  ];

  const auditLog = [
    { action: "Login realizado", timestamp: "2024-01-15 14:30", ip: "192.168.1.100" },
    { action: "Perfil atualizado", timestamp: "2024-01-14 16:45", ip: "192.168.1.100" },
    { action: "Senha alterada", timestamp: "2024-01-10 09:15", ip: "192.168.1.100" },
  ];

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Minha Conta
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Gerencie seu perfil e configurações de conta.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, textAlign: "center" }}>
            <Avatar
              sx={{ 
                width: 120, 
                height: 120, 
                margin: "0 auto 16px",
                fontSize: "3rem"
              }}
            >
              {user?.name?.charAt(0)?.toUpperCase() || "U"}
            </Avatar>
            <Typography variant="h6" gutterBottom>
              {user?.name || "Usuário"}
            </Typography>
            <Typography variant="body2" color="text.secondary" gutterBottom>
              {user?.email || "email@exemplo.com"}
            </Typography>
            <Typography variant="caption" color="text.secondary">
              {user?.role === "super_admin" ? "Super Administrador" : 
               user?.role === "contabilidade" ? "Gestor" : "Cliente"}
            </Typography>
            <Box sx={{ mt: 2 }}>
              <Button variant="outlined" startIcon={<Edit />} fullWidth>
                Alterar Foto
              </Button>
            </Box>
          </Paper>
        </Grid>

        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Tabs 
              value={tabValue} 
              onChange={(_, newValue) => setTabValue(newValue)}
              sx={{ mb: 3 }}
            >
              <Tab label="Informações Pessoais" />
              <Tab label="Segurança" />
              <Tab label="Notificações" />
              <Tab label="Atividades" />
            </Tabs>

            {/* Informações Pessoais */}
            {tabValue === 0 && (
              <Box>
                <Grid container spacing={2}>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Nome Completo"
                      value={userInfo.nome}
                      onChange={(e) => setUserInfo(prev => ({ ...prev, nome: e.target.value }))}
                      InputProps={{
                        startAdornment: <Person sx={{ mr: 1, color: "action.active" }} />,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Email"
                      value={userInfo.email}
                      onChange={(e) => setUserInfo(prev => ({ ...prev, email: e.target.value }))}
                      InputProps={{
                        startAdornment: <Email sx={{ mr: 1, color: "action.active" }} />,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Telefone"
                      value={userInfo.telefone}
                      onChange={(e) => setUserInfo(prev => ({ ...prev, telefone: e.target.value }))}
                      InputProps={{
                        startAdornment: <Phone sx={{ mr: 1, color: "action.active" }} />,
                      }}
                    />
                  </Grid>
                  <Grid item xs={12} md={6}>
                    <TextField
                      fullWidth
                      label="Cargo"
                      value={userInfo.cargo}
                      disabled
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      label="Empresa"
                      value={userInfo.empresa}
                      disabled
                    />
                  </Grid>
                </Grid>
                
                <Box sx={{ mt: 3, display: "flex", gap: 2 }}>
                  <Button variant="contained" startIcon={<Save />} onClick={handleSave}>
                    Salvar Alterações
                  </Button>
                  <Button variant="outlined">
                    Cancelar
                  </Button>
                </Box>
              </Box>
            )}

            {/* Segurança */}
            {tabValue === 1 && (
              <Box>
                <Card sx={{ mb: 3 }}>
                  <CardContent>
                    <Typography variant="h6" gutterBottom>
                      Alterar Senha
                    </Typography>
                    <Typography variant="body2" color="text.secondary" gutterBottom>
                      É recomendado alterar sua senha regularmente para manter a segurança da conta.
                    </Typography>
                    <Button 
                      variant="outlined" 
                      startIcon={<Lock />}
                      onClick={() => setOpenPasswordDialog(true)}
                    >
                      Alterar Senha
                    </Button>
                  </CardContent>
                </Card>

                <List>
                  {securitySettings.map((setting, index) => (
                    <ListItem key={index} divider>
                      <ListItemIcon>
                        {setting.icon}
                      </ListItemIcon>
                      <ListItemText
                        primary={setting.title}
                        secondary={setting.description}
                      />
                      <Switch
                        checked={setting.enabled}
                        onChange={() => {}}
                        color="primary"
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}

            {/* Notificações */}
            {tabValue === 2 && (
              <Box>
                <Typography variant="h6" gutterBottom>
                  Preferências de Notificação
                </Typography>
                <List>
                  <ListItem>
                    <ListItemIcon>
                      <Email />
                    </ListItemIcon>
                    <ListItemText
                      primary="Notificações por Email"
                      secondary="Receber alertas e atualizações por email"
                    />
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notifications.email}
                          onChange={() => handleNotificationChange("email")}
                        />
                      }
                      label=""
                    />
                  </ListItem>
                  <Divider />
                  <ListItem>
                    <ListItemIcon>
                      <Notifications />
                    </ListItemIcon>
                    <ListItemText
                      primary="Notificações Push"
                      secondary="Receber notificações no navegador"
                    />
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notifications.push}
                          onChange={() => handleNotificationChange("push")}
                        />
                      }
                      label=""
                    />
                  </ListItem>
                  <Divider />
                  <ListItem>
                    <ListItemIcon>
                      <Phone />
                    </ListItemIcon>
                    <ListItemText
                      primary="Notificações SMS"
                      secondary="Receber alertas importantes via SMS"
                    />
                    <FormControlLabel
                      control={
                        <Switch
                          checked={notifications.sms}
                          onChange={() => handleNotificationChange("sms")}
                        />
                      }
                      label=""
                    />
                  </ListItem>
                </List>
              </Box>
            )}

            {/* Atividades */}
            {tabValue === 3 && (
              <Box>
                <Typography variant="h6" gutterBottom>
                  Log de Atividades
                </Typography>
                <List>
                  {auditLog.map((log, index) => (
                    <ListItem key={index} divider>
                      <ListItemText
                        primary={log.action}
                        secondary={`${log.timestamp} - IP: ${log.ip}`}
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Password Change Dialog */}
      <Dialog open={openPasswordDialog} onClose={() => setOpenPasswordDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Alterar Senha</DialogTitle>
        <DialogContent>
          <Box sx={{ pt: 2 }}>
            <TextField
              fullWidth
              label="Senha Atual"
              type="password"
              margin="normal"
            />
            <TextField
              fullWidth
              label="Nova Senha"
              type="password"
              margin="normal"
            />
            <TextField
              fullWidth
              label="Confirmar Nova Senha"
              type="password"
              margin="normal"
            />
            <Alert severity="info" sx={{ mt: 2 }}>
              A senha deve ter pelo menos 8 caracteres, incluindo letras e números.
            </Alert>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenPasswordDialog(false)}>
            Cancelar
          </Button>
          <Button variant="contained" onClick={() => setOpenPasswordDialog(false)}>
            Alterar Senha
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default MinhaConta;
