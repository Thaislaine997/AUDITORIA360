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
  Card,
  CardContent,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  List,
  ListItem,
  ListItemText,
  Divider,
} from "@mui/material";
import {
  Add,
  Edit,
  Delete,
  FileCopy,
  Visibility,
  Description,
  Settings,
  Preview,
} from "@mui/icons-material";

interface Template {
  id: string;
  nome: string;
  descricao: string;
  categoria: "folha" | "auditoria" | "compliance" | "geral";
  campos: number;
  ultimaModificacao: string;
  status: "ativo" | "rascunho";
  utilizacoes: number;
}

const Templates: React.FC = () => {
  const [openDialog, setOpenDialog] = useState(false);
  const [editingId, setEditingId] = useState<string | null>(null);
  const [previewTemplate, setPreviewTemplate] = useState<Template | null>(null);

  const [templates, setTemplates] = useState<Template[]>([
    {
      id: "1",
      nome: "Configuração Padrão - Empresa Pequena",
      descricao: "Template básico para empresas de até 50 funcionários",
      categoria: "folha",
      campos: 12,
      ultimaModificacao: "2024-01-15",
      status: "ativo",
      utilizacoes: 25,
    },
    {
      id: "2",
      nome: "Auditoria Trabalhista Completa",
      descricao: "Checklist completo para auditoria trabalhista",
      categoria: "auditoria",
      campos: 35,
      ultimaModificacao: "2024-01-12",
      status: "ativo",
      utilizacoes: 18,
    },
    {
      id: "3",
      nome: "Compliance CCT 2024",
      descricao: "Template de conformidade com CCT atualizada",
      categoria: "compliance",
      campos: 28,
      ultimaModificacao: "2024-01-10",
      status: "rascunho",
      utilizacoes: 5,
    },
  ]);

  const handleEdit = (id: string) => {
    setEditingId(id);
    setOpenDialog(true);
  };

  const handleAdd = () => {
    setEditingId(null);
    setOpenDialog(true);
  };

  const handleDelete = (id: string) => {
    if (confirm("Tem certeza que deseja excluir este template?")) {
      setTemplates(prev => prev.filter(t => t.id !== id));
    }
  };

  const handleDuplicate = (template: Template) => {
    const newTemplate = {
      ...template,
      id: Date.now().toString(),
      nome: `${template.nome} (Cópia)`,
      utilizacoes: 0,
      status: "rascunho" as const,
    };
    setTemplates(prev => [...prev, newTemplate]);
  };

  const getCategoryLabel = (categoria: string) => {
    switch (categoria) {
      case "folha": return "Folha de Pagamento";
      case "auditoria": return "Auditoria";
      case "compliance": return "Compliance";
      case "geral": return "Geral";
      default: return categoria;
    }
  };

  const getCategoryColor = (categoria: string) => {
    switch (categoria) {
      case "folha": return "primary";
      case "auditoria": return "secondary";
      case "compliance": return "warning";
      case "geral": return "info";
      default: return "default";
    }
  };

  const templateFields = [
    { nome: "Razão Social", tipo: "texto", obrigatorio: true },
    { nome: "CNPJ", tipo: "documento", obrigatorio: true },
    { nome: "Número de Funcionários", tipo: "numero", obrigatorio: true },
    { nome: "Setor Principal", tipo: "selecao", obrigatorio: false },
    { nome: "Tipo de Contrato", tipo: "multipla_escolha", obrigatorio: true },
  ];

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Templates de Configuração
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Crie e gerencie templates para configuração de clientes.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
              <Typography variant="h6">
                Templates Disponíveis ({templates.length})
              </Typography>
              <Button
                variant="contained"
                startIcon={<Add />}
                onClick={handleAdd}
              >
                Novo Template
              </Button>
            </Box>

            <TableContainer>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Nome</TableCell>
                    <TableCell>Categoria</TableCell>
                    <TableCell>Campos</TableCell>
                    <TableCell>Utilizações</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell align="center">Ações</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {templates.map((template) => (
                    <TableRow key={template.id}>
                      <TableCell>
                        <Box>
                          <Typography variant="subtitle2">
                            {template.nome}
                          </Typography>
                          <Typography variant="caption" color="text.secondary">
                            {template.descricao}
                          </Typography>
                        </Box>
                      </TableCell>
                      <TableCell>
                        <Chip 
                          label={getCategoryLabel(template.categoria)}
                          color={getCategoryColor(template.categoria) as any}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{template.campos}</TableCell>
                      <TableCell>{template.utilizacoes}</TableCell>
                      <TableCell>
                        <Chip 
                          label={template.status}
                          color={template.status === "ativo" ? "success" : "warning"}
                          size="small"
                        />
                      </TableCell>
                      <TableCell align="center">
                        <IconButton 
                          size="small" 
                          color="info"
                          onClick={() => setPreviewTemplate(template)}
                        >
                          <Preview />
                        </IconButton>
                        <IconButton 
                          size="small" 
                          color="primary"
                          onClick={() => handleEdit(template.id)}
                        >
                          <Edit />
                        </IconButton>
                        <IconButton 
                          size="small" 
                          color="secondary"
                          onClick={() => handleDuplicate(template)}
                        >
                          <FileCopy />
                        </IconButton>
                        <IconButton 
                          size="small" 
                          color="error"
                          onClick={() => handleDelete(template.id)}
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
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Estatísticas
            </Typography>
            
            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h4" color="primary">
                  {templates.length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Templates Criados
                </Typography>
              </CardContent>
            </Card>

            <Card sx={{ mb: 2 }}>
              <CardContent>
                <Typography variant="h4" color="secondary">
                  {templates.reduce((sum, t) => sum + t.utilizacoes, 0)}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Total de Utilizações
                </Typography>
              </CardContent>
            </Card>

            <Card>
              <CardContent>
                <Typography variant="h4" color="success.main">
                  {templates.filter(t => t.status === "ativo").length}
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  Templates Ativos
                </Typography>
              </CardContent>
            </Card>
          </Paper>

          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Templates Populares
            </Typography>
            <List dense>
              {templates
                .sort((a, b) => b.utilizacoes - a.utilizacoes)
                .slice(0, 3)
                .map((template, index) => (
                  <React.Fragment key={template.id}>
                    <ListItem>
                      <ListItemText
                        primary={template.nome}
                        secondary={`${template.utilizacoes} utilizações`}
                      />
                    </ListItem>
                    {index < 2 && <Divider />}
                  </React.Fragment>
                ))}
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Dialog for add/edit template */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="lg" fullWidth>
        <DialogTitle>
          {editingId ? "Editar Template" : "Novo Template"}
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={2} sx={{ mt: 1 }}>
            <Grid item xs={12} md={6}>
              <TextField
                fullWidth
                label="Nome do Template"
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12} md={6}>
              <FormControl fullWidth>
                <InputLabel>Categoria</InputLabel>
                <Select
                  label="Categoria"
                  defaultValue=""
                >
                  <MenuItem value="folha">Folha de Pagamento</MenuItem>
                  <MenuItem value="auditoria">Auditoria</MenuItem>
                  <MenuItem value="compliance">Compliance</MenuItem>
                  <MenuItem value="geral">Geral</MenuItem>
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Descrição"
                multiline
                rows={3}
                variant="outlined"
              />
            </Grid>
            <Grid item xs={12}>
              <Typography variant="h6" gutterBottom>
                Campos do Template
              </Typography>
              <List>
                {templateFields.map((field, index) => (
                  <ListItem key={index} divider>
                    <ListItemText
                      primary={field.nome}
                      secondary={`${field.tipo} - ${field.obrigatorio ? "Obrigatório" : "Opcional"}`}
                    />
                    <IconButton size="small" color="primary">
                      <Settings />
                    </IconButton>
                    <IconButton size="small" color="error">
                      <Delete />
                    </IconButton>
                  </ListItem>
                ))}
              </List>
              <Button variant="outlined" startIcon={<Add />} fullWidth sx={{ mt: 2 }}>
                Adicionar Campo
              </Button>
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>
            Cancelar
          </Button>
          <Button variant="contained" onClick={() => setOpenDialog(false)}>
            Salvar Template
          </Button>
        </DialogActions>
      </Dialog>

      {/* Preview Dialog */}
      <Dialog 
        open={!!previewTemplate} 
        onClose={() => setPreviewTemplate(null)} 
        maxWidth="md" 
        fullWidth
      >
        <DialogTitle>
          Preview: {previewTemplate?.nome}
        </DialogTitle>
        <DialogContent>
          {previewTemplate && (
            <Box>
              <Typography variant="body1" gutterBottom>
                {previewTemplate.descricao}
              </Typography>
              <Typography variant="h6" gutterBottom sx={{ mt: 3 }}>
                Campos do Template:
              </Typography>
              <List>
                {templateFields.map((field, index) => (
                  <ListItem key={index}>
                    <Description sx={{ mr: 2 }} />
                    <ListItemText
                      primary={field.nome}
                      secondary={`Tipo: ${field.tipo} | ${field.obrigatorio ? "Obrigatório" : "Opcional"}`}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPreviewTemplate(null)}>
            Fechar
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default Templates;