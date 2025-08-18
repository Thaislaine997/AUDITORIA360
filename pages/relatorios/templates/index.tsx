// Migrated from src/frontend/pages/relatorios/ReportTemplatesPage.tsx
import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Button,
  Card,
  CardContent,
  Paper,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
} from "@mui/material";
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  Visibility as PreviewIcon,
} from "@mui/icons-material";

interface ReportTemplate {
  id: number;
  name: string;
  description?: string;
  type: string;
  is_default: boolean;
  is_active: boolean;
  usage_count: number;
  created_at: string;
}

const ReportTemplatesPage: React.FC = () => {
  const [templates, setTemplates] = useState<ReportTemplate[]>([
    {
      id: 1,
      name: "Relatório Mensal de Folha",
      description: "Template padrão para relatórios mensais",
      type: "FOLHA",
      is_default: true,
      is_active: true,
      usage_count: 25,
      created_at: "2024-01-15"
    },
    {
      id: 2,
      name: "Análise de Divergências",
      description: "Template para relatórios de auditoria",
      type: "AUDITORIA",
      is_default: false,
      is_active: true,
      usage_count: 12,
      created_at: "2024-02-01"
    }
  ]);
  
  const [editDialog, setEditDialog] = useState(false);
  const [selectedTemplate, setSelectedTemplate] = useState<ReportTemplate | null>(null);

  const handleEdit = (template: ReportTemplate) => {
    setSelectedTemplate(template);
    setEditDialog(true);
  };

  const handleCloseDialog = () => {
    setEditDialog(false);
    setSelectedTemplate(null);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" gutterBottom>
            Templates de Relatórios
          </Typography>
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setEditDialog(true)}
          >
            Novo Template
          </Button>
        </Box>

        <Box display="flex" flexDirection="column" gap={2}>
          {templates.map((template) => (
            <Card key={template.id}>
              <CardContent>
                <Box display="flex" justifyContent="space-between" alignItems="start">
                  <Box>
                    <Typography variant="h6" gutterBottom>
                      {template.name}
                      {template.is_default && (
                        <Chip label="Padrão" size="small" color="primary" sx={{ ml: 1 }} />
                      )}
                    </Typography>
                    <Typography variant="body2" color="text.secondary" paragraph>
                      {template.description}
                    </Typography>
                    <Box display="flex" gap={1} alignItems="center">
                      <Chip label={template.type} size="small" />
                      <Typography variant="caption" color="text.secondary">
                        Usado {template.usage_count} vezes
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        • Criado em {new Date(template.created_at).toLocaleDateString('pt-BR')}
                      </Typography>
                    </Box>
                  </Box>
                  <Box>
                    <IconButton onClick={() => handleEdit(template)}>
                      <EditIcon />
                    </IconButton>
                    <IconButton>
                      <PreviewIcon />
                    </IconButton>
                    <IconButton>
                      <DeleteIcon />
                    </IconButton>
                  </Box>
                </Box>
              </CardContent>
            </Card>
          ))}
        </Box>

        {/* Edit Dialog */}
        <Dialog open={editDialog} onClose={handleCloseDialog} maxWidth="sm" fullWidth>
          <DialogTitle>
            {selectedTemplate ? 'Editar Template' : 'Novo Template'}
          </DialogTitle>
          <DialogContent>
            <TextField
              fullWidth
              label="Nome do Template"
              defaultValue={selectedTemplate?.name || ''}
              margin="normal"
            />
            <TextField
              fullWidth
              label="Descrição"
              defaultValue={selectedTemplate?.description || ''}
              margin="normal"
              multiline
              rows={3}
            />
          </DialogContent>
          <DialogActions>
            <Button onClick={handleCloseDialog}>Cancelar</Button>
            <Button onClick={handleCloseDialog} variant="contained">
              Salvar
            </Button>
          </DialogActions>
        </Dialog>
      </Box>
    </Container>
  );
};

export default ReportTemplatesPage;