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
} from "@mui/material";
import {
  Add,
  Edit,
  Delete,
  Business,
  Visibility,
} from "@mui/icons-material";
import { useAuthStore } from "../stores/authStore";

interface Contabilidade {
  id: string;
  nome: string;
  cnpj: string;
  responsavel: string;
  email: string;
  telefone: string;
  clientesCount: number;
  status: "ativa" | "inativa";
}

const GestaoContabilidades: React.FC = () => {
  const { user } = useAuthStore();
  const [openDialog, setOpenDialog] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);

  // Mock data - in real app this would come from API
  const [contabilidades, setContabilidades] = useState<Contabilidade[]>([
    {
      id: "1",
      nome: "Contabilidade Alpha Ltda",
      cnpj: "12.345.678/0001-90",
      responsavel: "João Silva",
      email: "joao@alpha.com.br",
      telefone: "(11) 98765-4321",
      clientesCount: 25,
      status: "ativa",
    },
    {
      id: "2",
      nome: "Beta Assessoria Contábil",
      cnpj: "98.765.432/0001-10",
      responsavel: "Maria Santos",
      email: "maria@beta.com.br",
      telefone: "(11) 91234-5678",
      clientesCount: 18,
      status: "ativa",
    },
  ]);

  // Only Super Admin can access this page
  if (user?.role !== "super_admin") {
    return (
      <Container maxWidth="xl">
        <Box sx={{ textAlign: "center", mt: 8 }}>
          <Typography variant="h5" color="error">
            Acesso Negado
          </Typography>
          <Typography variant="body1" color="text.secondary">
            Esta funcionalidade é restrita a Super Administradores.
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
    if (confirm("Tem certeza que deseja excluir esta contabilidade?")) {
      setContabilidades(prev => prev.filter(c => c.id !== id));
    }
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Gestão de Contabilidades
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Gerencie todas as contabilidades e seus dados no sistema.
        </Typography>
      </Box>

      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
          <Typography variant="h6">
            Contabilidades Cadastradas
          </Typography>
          <Button
            variant="contained"
            startIcon={<Add />}
            onClick={handleAdd}
          >
            Nova Contabilidade
          </Button>
        </Box>

        <TableContainer>
          <Table>
            <TableHead>
              <TableRow>
                <TableCell>Nome</TableCell>
                <TableCell>CNPJ</TableCell>
                <TableCell>Responsável</TableCell>
                <TableCell>Contato</TableCell>
                <TableCell>Clientes</TableCell>
                <TableCell>Status</TableCell>
                <TableCell align="center">Ações</TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {contabilidades.map((contabilidade) => (
                <TableRow key={contabilidade.id}>
                  <TableCell>
                    <Box sx={{ display: "flex", alignItems: "center", gap: 1 }}>
                      <Business color="primary" />
                      {contabilidade.nome}
                    </Box>
                  </TableCell>
                  <TableCell>{contabilidade.cnpj}</TableCell>
                  <TableCell>{contabilidade.responsavel}</TableCell>
                  <TableCell>
                    <Box>
                      <Typography variant="body2">{contabilidade.email}</Typography>
                      <Typography variant="caption" color="text.secondary">
                        {contabilidade.telefone}
                      </Typography>
                    </Box>
                  </TableCell>
                  <TableCell>{contabilidade.clientesCount}</TableCell>
                  <TableCell>
                    <Chip 
                      label={contabilidade.status}
                      color={contabilidade.status === "ativa" ? "success" : "error"}
                      size="small"
                    />
                  </TableCell>
                  <TableCell align="center">
                    <IconButton 
                      size="small" 
                      color="primary"
                      onClick={() => handleEdit(contabilidade.id)}
                    >
                      <Edit />
                    </IconButton>
                    <IconButton size="small" color="info">
                      <Visibility />
                    </IconButton>
                    <IconButton 
                      size="small" 
                      color="error"
                      onClick={() => handleDelete(contabilidade.id)}
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
          {editingId ? "Editar Contabilidade" : "Nova Contabilidade"}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Nome da Contabilidade"
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

export default GestaoContabilidades;