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
  Tab,
  Tabs,
} from "@mui/material";
import {
  Add,
  Edit,
  Delete,
  Person,
  PersonAdd,
  Security,
} from "@mui/icons-material";
import { useAuthStore } from "../stores/authStore";

interface Usuario {
  id: string;
  nome: string;
  email: string;
  role: "super_admin" | "contabilidade" | "cliente_final";
  contabilidade?: string;
  status: "ativo" | "inativo";
  ultimoAcesso: string;
}

const GerenciamentoUsuarios: React.FC = () => {
  const { user } = useAuthStore();
  const [openDialog, setOpenDialog] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [tabValue, setTabValue] = useState(0);

  // Mock data
  const [usuarios, setUsuarios] = useState<Usuario[]>([
    {
      id: "1",
      nome: "João Admin",
      email: "admin@auditoria360.com",
      role: "super_admin",
      status: "ativo",
      ultimoAcesso: "2024-01-15",
    },
    {
      id: "2",
      nome: "Maria Gestora",
      email: "maria@alpha.com.br",
      role: "contabilidade",
      contabilidade: "Contabilidade Alpha",
      status: "ativo",
      ultimoAcesso: "2024-01-14",
    },
    {
      id: "3",
      nome: "Carlos Cliente",
      email: "carlos@empresa.com.br",
      role: "cliente_final",
      contabilidade: "Contabilidade Alpha",
      status: "ativo",
      ultimoAcesso: "2024-01-13",
    },
  ]);

  // Check permissions
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
    if (confirm("Tem certeza que deseja excluir este usuário?")) {
      setUsuarios(prev => prev.filter(u => u.id !== id));
    }
  };

  const getRoleLabel = (role: string) => {
    switch (role) {
      case "super_admin": return "Super Admin";
      case "contabilidade": return "Gestor";
      case "cliente_final": return "Cliente";
      default: return role;
    }
  };

  const getRoleColor = (role: string) => {
    switch (role) {
      case "super_admin": return "error";
      case "contabilidade": return "warning";
      case "cliente_final": return "info";
      default: return "default";
    }
  };

  // Filter users based on current user role
  const filteredUsuarios = user?.role === "super_admin" 
    ? usuarios 
    : usuarios.filter(usuario => 
        // Gestor only sees users from their contabilidade
        usuario.contabilidade === user?.name // In real app, this would be proper filtering
      );

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Gerenciamento de Usuários
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          {user?.role === "super_admin" 
            ? "Gerencie todos os usuários do sistema." 
            : "Gerencie os usuários da sua contabilidade."
          }
        </Typography>
      </Box>

      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
          <Typography variant="h6">
            Usuários Cadastrados ({filteredUsuarios.length})
          </Typography>
          <Button
            variant="contained"
            startIcon={<PersonAdd />}
            onClick={handleAdd}
          >
            Novo Usuário
          </Button>
        </Box>

        <Tabs 
          value={tabValue} 
          onChange={(_, newValue) => setTabValue(newValue)}
          sx={{ mb: 3 }}
        >
          <Tab label="Todos" />
          <Tab label="Administradores" />
          <Tab label="Gestores" />
          <Tab label="Clientes" />
        </Tabs>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Nome</TableCell>
                <TableCell>Email</TableCell>
                <TableCell>Tipo</TableCell>
                {user?.role === "super_admin" && <TableCell>Contabilidade</TableCell>}
                <TableCell>Status</TableCell>
                <TableCell>Último Acesso</TableCell>
                <TableCell align="center">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {filteredUsuarios.map((usuario) => (
                <TableRow key={usuario.id}>
                  <TableCell>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <Person color="primary" />
                      {usuario.nome}
                    </Box>
                  </TableCell>
                  <TableCell>{usuario.email}</TableCell>
                  <TableCell>
                    <Chip 
                      label={getRoleLabel(usuario.role)}
                      color={getRoleColor(usuario.role) as any}
                      size="small"
                      icon={usuario.role === "super_admin" ? <Security /> : undefined}
                    />
                  </TableCell>
                  {user?.role === "super_admin" && (
                    <TableCell>{usuario.contabilidade || "-"}</TableCell>
                  )}
                  <TableCell>
                    <Chip 
                      label={usuario.status}
                      color={usuario.status === "ativo" ? "success" : "error"}
                      size="small"
                    />
                  </TableCell>
                  <TableCell>{new Date(usuario.ultimoAcesso).toLocaleDateString()}</TableCell>
                  <TableCell align="center">
                    <IconButton 
                      size="small" 
                      color="primary"
                      onClick={() => handleEdit(usuario.id)}
                    >
                      <Edit />
                    </IconButton>
                    {usuario.role !== "super_admin" && (
                      <IconButton 
                        size="small" 
                        color="error"
                        onClick={() => handleDelete(usuario.id)}
                      >
                        <Delete />
                      </IconButton>
                    )}
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
          {editingId ? "Editar Usuário" : "Novo Usuário"}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Nome Completo"
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
              <FormControl fullWidth>
                <InputLabel>Tipo de Usuário</InputLabel>
                <Select
                  label="Tipo de Usuário"
                  defaultValue=""
                >
                  {user?.role === "super_admin" && (
                    <MenuItem value="super_admin">Super Admin</MenuItem>
                  )}
                  <MenuItem value="contabilidade">Gestor</MenuItem>
                  <MenuItem value="cliente_final">Cliente</MenuItem>
                </Select>
              </FormControl>
            </Grid>
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
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Senha Temporária"
                type="password"
                variant="outlined"
              />
            </Grid>
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
          <Button variant="contained" onClick={() => setOpenDialog(false)}>
            Salvar
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default GerenciamentoUsuarios;