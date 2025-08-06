import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  Grid,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import {
  Add,
  Edit,
  Delete,
  Person,
  Visibility,
  Business,
} from "@mui/icons-material";
import { useAuthStore } from "../stores/authStore";
import { useGamificationStore } from "../stores/gamificationStore";

interface Cliente {
  id: string;
  nomeEmpresa: string;
  cnpj: string;
  responsavel: string;
  email: string;
  telefone: string;
  contabilidade: string;
  funcionarios: number;
  status: "ativo" | "inativo";
}

const GestaoClientes: React.FC = () => {
  const { user } = useAuthStore();
  const { unlockAchievement, addXP } = useGamificationStore();
  const [openDialog, setOpenDialog] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [systemStatus, setSystemStatus] = useState<any>(null);
  const [loadingSystemStatus, setLoadingSystemStatus] = useState(false);

  // Mock data - in real app this would be filtered by user role/permissions
  const [clientes, setClientes] = useState<Cliente[]>([
    {
      id: "1",
      nomeEmpresa: "TechCorp Soluções",
      cnpj: "11.222.333/0001-44",
      responsavel: "Carlos Oliveira",
      email: "carlos@techcorp.com.br",
      telefone: "(11) 99999-0000",
      contabilidade: "Contabilidade Alpha",
      funcionarios: 45,
      status: "ativo",
    },
    {
      id: "2",
      nomeEmpresa: "Inovação Ltda",
      cnpj: "55.666.777/0001-88",
      responsavel: "Ana Costa",
      email: "ana@inovacao.com.br",
      telefone: "(11) 88888-1111",
      contabilidade: "Beta Assessoria",
      funcionarios: 23,
      status: "ativo",
    },
  ]);

  // Check if user has permission (Gestor and Super Admin)
  const hasPermission = user?.role === "super_admin" || user?.role === "contabilidade";

  if (!hasPermission) {
    return (
      <Container maxWidth="xl">
        <Box sx={{ textAlign: "center", mt: 8 }}>
          <Typography variant="h5" color="error">
            Acesso Negado
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Esta funcionalidade é restrita a Gestores e Super Administradores.
          </Typography>
        </Box>
      </Container>
    );
  }

  const handleEdit = (id: string) => {
    setEditingId(id);
    setOpenDialog(true);
  };

  const handleAdd = () => {
    setEditingId(null);
    setOpenDialog(true);
  };

  const handleDelete = (id: string) => {
    if (confirm("Tem certeza que deseja excluir este cliente?")) {
      setClientes(prev => prev.filter(c => c.id !== id));
    }
  };

  const checkSystemHealth = async () => {
    try {
      setLoadingSystemStatus(true);
      const response = await fetch('http://localhost:8001/api/core/system/health');
      const data = await response.json();
      setSystemStatus(data);
    } catch (error) {
      console.error('Failed to check system health:', error);
      setSystemStatus({ success: false, error: 'Connection failed' });
    } finally {
      setLoadingSystemStatus(false);
    }
  };

  const activateBusinessFlow = async (clientId: string) => {
    try {
      const response = await fetch(`http://localhost:8001/api/core/business-flow/${clientId}`);
      const data = await response.json();
      
      if (data.success) {
        alert(`Business flow activated for ${data.data.client.name}! 
Context ID: ${data.data.system_health.context_id}
Available actions: ${data.data.available_actions.join(', ')}`);
      } else {
        alert(`Failed to activate business flow: ${data.message}`);
      }
    } catch (error) {
      alert(`Error: ${error}`);
    }
  };

  // Filter clients based on user role
  const filteredClientes = user?.role === "super_admin" 
    ? clientes 
    : clientes.filter(cliente => 
        // In real app, this would check if the client belongs to the user's contabilidade
        true 
      );

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Gestão de Clientes
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          {user?.role === "super_admin" 
            ? "Gerencie todos os clientes do sistema." 
            : "Gerencie os clientes da sua contabilidade."
          }
        </Typography>
      </Box>

      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
          <Typography variant="h6">
            Clientes Cadastrados ({filteredClientes.length})
          </Typography>
          <Box sx={{ display: "flex", gap: 2 }}>
            <Button
              variant="outlined"
              startIcon={loadingSystemStatus ? undefined : <Business />}
              onClick={checkSystemHealth}
              disabled={loadingSystemStatus}
              color="info"
            >
              {loadingSystemStatus ? "Verificando..." : "Status do Sistema"}
            </Button>
            <Button
              variant="contained"
              startIcon={<Add />}
              onClick={handleAdd}
            >
              Novo Cliente
            </Button>
          </Box>
        </Box>

        {/* System Status Display */}
        {systemStatus && (
          <Box sx={{ mb: 3, p: 2, bgcolor: systemStatus.success ? 'success.light' : 'error.light', borderRadius: 1 }}>
            <Typography variant="subtitle2" gutterBottom>
              Status do Sistema Integrado:
            </Typography>
            {systemStatus.success ? (
              <Typography variant="body2">
                ✅ Core System: {systemStatus.health.core_system.initialized ? 'Inicializado' : 'Não inicializado'} | 
                Cache: {systemStatus.health.components.cache} | 
                Auth: {systemStatus.health.components.authentication}
              </Typography>
            ) : (
              <Typography variant="body2" color="error">
                ❌ Sistema offline: {systemStatus.error || 'Conexão falhou'}
              </Typography>
            )}
          </Box>
        )}

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Empresa</TableCell>
                <TableCell>CNPJ</TableCell>
                <TableCell>Responsável</TableCell>
                <TableCell>Contato</TableCell>
                {user?.role === "super_admin" && <TableCell>Contabilidade</TableCell>}
                <TableCell>Funcionários</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="center">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredClientes.map((cliente) => (
                <TableRow key={cliente.id}>
                  <TableCell>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <Business color="primary" />
                      {cliente.nomeEmpresa}
                    </Box>
                  </TableCell>
                  <TableCell>{cliente.cnpj}</TableCell>
                  <TableCell>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <Person fontSize="small" />
                      {cliente.responsavel}
                    </Box>
                  </TableCell>
                  <TableCell>
                    <Box>
                      <Typography variant="body2">{cliente.email}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {cliente.telefone}
                      </Typography>
                    </Box>
                  </TableCell>
                  {user?.role === "super_admin" && (
                    <TableCell>{cliente.contabilidade}</TableCell>
                  )}
                  <TableCell>{cliente.funcionarios}</TableCell>
                  <TableCell>
                    <Chip 
                      label={cliente.status}
                      color={cliente.status === "ativo" ? "success" : "error"}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton 
                      size="small" 
                      color="primary"
                      onClick={() => handleEdit(cliente.id)}
                      title="Editar Cliente"
                    >
                      <Edit />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      color="info"
                      title="Visualizar Detalhes"
                    >
                      <Visibility />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      color="success"
                      onClick={() => activateBusinessFlow(cliente.id)}
                      title="Ativar Fluxo de Negócio"
                    >
                      <Business />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      color="error"
                      onClick={() => handleDelete(cliente.id)}
                      title="Excluir Cliente"
                    >
                      <Delete />
                    </IconButton>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      </Paper>

      {/* Dialog for add/edit */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="md" fullWidth>
        <DialogTitle>
          {editingId ? "Editar Cliente" : "Novo Cliente"}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Nome da Empresa"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="CNPJ"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Responsável"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Email"
                type="email"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Telefone"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Número de Funcionários"
                type="number"
                variant="outlined"
              />
            </Grid>
            {user?.role === "super_admin" && (
              <Grid item xs={12} md={6}>
                <FormControl fullWidth>
                  <InputLabel>Contabilidade</InputLabel>
                  <Select
                    label="Contabilidade"
                    defaultValue=""
                  >
                    <MenuItem value="alpha">Contabilidade Alpha</MenuItem>
                    <MenuItem value="beta">Beta Assessoria</MenuItem>
                  </Select>
                </FormControl>
              </Grid>
            )}
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  label="Status"
                  defaultValue="ativo"
                >
                  <MenuItem value="ativo">Ativo</MenuItem>
                  <MenuItem value="inativo">Inativo</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>
            Cancelar
          </Button>
          <Button 
            variant="contained" 
            onClick={() => {
              // Simulate saving client
              setOpenDialog(false);
              
              // Add gamification rewards
              addXP(50, "Cliente cadastrado");
              
              // Check if this is the first client (trigger achievement)
              if (clientes.length === 0 || !editingId) {
                unlockAchievement("first_client_config");
              }
              
              // Update client count for achievements
              const newClientCount = clientes.length + 1;
              if (newClientCount >= 10) {
                unlockAchievement("client_master");
              }
            }}
          >
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default GestaoClientes;