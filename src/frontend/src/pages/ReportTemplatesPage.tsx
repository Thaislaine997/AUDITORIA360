import React, { useState, useEffect } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Typography,
  Grid,
  Chip,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Fab,
  Tooltip,
  Paper,
} from "@mui/material";
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  DragIndicator as DragIcon,
  Visibility as PreviewIcon,
  FileCopy as CopyIcon,
} from "@mui/icons-material";
import ExportButton from "../components/ExportButton";

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

interface ReportBlock {
  id: number;
  block_type: string;
  title?: string;
  position_order: number;
  width_percentage: number;
}

interface BlockType {
  type: string;
  name: string;
  description: string;
  icon: string;
}

const ReportTemplatesPage: React.FC = () => {
  const [templates, setTemplates] = useState<ReportTemplate[]>([]);
  const [blockTypes, setBlockTypes] = useState<BlockType[]>([]);
  const [selectedTemplate, setSelectedTemplate] = useState<ReportTemplate | null>(null);
  const [templateBlocks, setTemplateBlocks] = useState<ReportBlock[]>([]);
  const [createDialogOpen, setCreateDialogOpen] = useState(false);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [previewDialogOpen, setPreviewDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  // Form states
  const [templateName, setTemplateName] = useState("");
  const [templateDescription, setTemplateDescription] = useState("");
  const [templateType, setTemplateType] = useState("financial");

  useEffect(() => {
    fetchTemplates();
    fetchBlockTypes();
  }, []);

  const fetchTemplates = async () => {
    // TODO: Replace with actual API call
    const mockTemplates: ReportTemplate[] = [
      {
        id: 1,
        name: "Relatório Financeiro Básico",
        description: "Template padrão para relatórios financeiros",
        type: "financial",
        is_default: true,
        is_active: true,
        usage_count: 15,
        created_at: "2024-01-01T00:00:00Z",
      },
      {
        id: 2,
        name: "Análise de Despesas Detalhada",
        description: "Template customizado para análise detalhada de despesas",
        type: "financial",
        is_default: false,
        is_active: true,
        usage_count: 8,
        created_at: "2024-01-05T10:30:00Z",
      },
    ];
    setTemplates(mockTemplates);
  };

  const fetchBlockTypes = async () => {
    // TODO: Replace with actual API call
    const mockBlockTypes: BlockType[] = [
      {
        type: "header",
        name: "Cabeçalho",
        description: "Cabeçalho do relatório com logo e informações básicas",
        icon: "header",
      },
      {
        type: "expense_analysis",
        name: "Análise de Despesas",
        description: "Gráficos e tabelas de análise de despesas",
        icon: "chart-bar",
      },
      {
        type: "balance_sheet",
        name: "Balanço Patrimonial Simplificado",
        description: "Resumo do balanço patrimonial",
        icon: "balance-scale",
      },
      {
        type: "monthly_revenue_chart",
        name: "Gráfico de Faturamento Mensal",
        description: "Gráfico de evolução do faturamento",
        icon: "chart-line",
      },
    ];
    setBlockTypes(mockBlockTypes);
  };

  const handleCreateTemplate = async () => {
    setLoading(true);
    // TODO: Implement actual API call
    setTimeout(() => {
      const newTemplate: ReportTemplate = {
        id: Date.now(),
        name: templateName,
        description: templateDescription,
        type: templateType,
        is_default: false,
        is_active: true,
        usage_count: 0,
        created_at: new Date().toISOString(),
      };
      setTemplates([...templates, newTemplate]);
      setCreateDialogOpen(false);
      setTemplateName("");
      setTemplateDescription("");
      setTemplateType("financial");
      setLoading(false);
    }, 1000);
  };

  const handleEditTemplate = (template: ReportTemplate) => {
    setSelectedTemplate(template);
    setTemplateName(template.name);
    setTemplateDescription(template.description || "");
    setTemplateType(template.type);
    setEditDialogOpen(true);
  };

  const handlePreviewTemplate = async (template: ReportTemplate) => {
    setSelectedTemplate(template);
    // TODO: Fetch template blocks
    const mockBlocks: ReportBlock[] = [
      {
        id: 1,
        block_type: "header",
        title: "Cabeçalho do Relatório",
        position_order: 1,
        width_percentage: 100,
      },
      {
        id: 2,
        block_type: "expense_analysis",
        title: "Análise de Despesas",
        position_order: 2,
        width_percentage: 100,
      },
    ];
    setTemplateBlocks(mockBlocks);
    setPreviewDialogOpen(true);
  };

  const handleDeleteTemplate = async (templateId: number) => {
    if (window.confirm("Tem certeza que deseja excluir este template?")) {
      // TODO: Implement actual API call
      setTemplates(templates.filter(t => t.id !== templateId));
    }
  };

  const handleGenerateReport = async (template: ReportTemplate) => {
    // TODO: Implement report generation
    console.log("Generating report with template:", template.name);
  };

  const handleExportTemplatesPdf = async () => {
    // TODO: Implement PDF export of templates list
    console.log("Exporting templates to PDF");
  };

  const handleExportTemplatesCsv = async () => {
    // TODO: Implement CSV export of templates list
    console.log("Exporting templates to CSV");
  };

  const getTypeLabel = (type: string) => {
    switch (type) {
      case "financial":
        return "Financeiro";
      case "payroll":
        return "Folha";
      case "compliance":
        return "Compliance";
      case "audit":
        return "Auditoria";
      default:
        return "Personalizado";
    }
  };

  const getBlockTypeLabel = (type: string) => {
    const blockType = blockTypes.find(bt => bt.type === type);
    return blockType ? blockType.name : type;
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Modelos de Relatório
        </Typography>
        <Box sx={{ display: "flex", gap: 2 }}>
          <ExportButton
            onExportPdf={handleExportTemplatesPdf}
            onExportCsv={handleExportTemplatesCsv}
          />
          <Button
            variant="contained"
            startIcon={<AddIcon />}
            onClick={() => setCreateDialogOpen(true)}
          >
            Novo Template
          </Button>
        </Box>
      </Box>

      <Grid container spacing={3}>
        {templates.map((template) => (
          <Grid item xs={12} md={6} lg={4} key={template.id}>
            <Card>
              <CardContent>
                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start", mb: 2 }}>
                  <Typography variant="h6" gutterBottom>
                    {template.name}
                  </Typography>
                  <Box sx={{ display: "flex", gap: 1 }}>
                    {template.is_default && (
                      <Chip label="Padrão" size="small" color="primary" />
                    )}
                    <Chip
                      label={getTypeLabel(template.type)}
                      size="small"
                      variant="outlined"
                    />
                  </Box>
                </Box>

                <Typography variant="body2" color="text.secondary" gutterBottom>
                  {template.description}
                </Typography>

                <Typography variant="caption" display="block" sx={{ mt: 1, mb: 2 }}>
                  Usado {template.usage_count} vezes
                </Typography>

                <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
                  <Box>
                    <Tooltip title="Visualizar">
                      <IconButton size="small" onClick={() => handlePreviewTemplate(template)}>
                        <PreviewIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Editar">
                      <IconButton size="small" onClick={() => handleEditTemplate(template)}>
                        <EditIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Duplicar">
                      <IconButton size="small">
                        <CopyIcon />
                      </IconButton>
                    </Tooltip>
                    {!template.is_default && (
                      <Tooltip title="Excluir">
                        <IconButton
                          size="small"
                          color="error"
                          onClick={() => handleDeleteTemplate(template.id)}
                        >
                          <DeleteIcon />
                        </IconButton>
                      </Tooltip>
                    )}
                  </Box>
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => handleGenerateReport(template)}
                  >
                    Gerar Relatório
                  </Button>
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Create Template Dialog */}
      <Dialog open={createDialogOpen} onClose={() => setCreateDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle>Criar Novo Template</DialogTitle>
        <DialogContent>
          <Box sx={{ display: "flex", flexDirection: "column", gap: 2, mt: 1 }}>
            <TextField
              label="Nome do Template"
              value={templateName}
              onChange={(e) => setTemplateName(e.target.value)}
              fullWidth
            />
            <TextField
              label="Descrição"
              value={templateDescription}
              onChange={(e) => setTemplateDescription(e.target.value)}
              multiline
              rows={3}
              fullWidth
            />
            <FormControl fullWidth>
              <InputLabel>Tipo do Relatório</InputLabel>
              <Select
                value={templateType}
                onChange={(e) => setTemplateType(e.target.value)}
              >
                <MenuItem value="financial">Financeiro</MenuItem>
                <MenuItem value="payroll">Folha de Pagamento</MenuItem>
                <MenuItem value="compliance">Compliance</MenuItem>
                <MenuItem value="audit">Auditoria</MenuItem>
                <MenuItem value="custom">Personalizado</MenuItem>
              </Select>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCreateDialogOpen(false)}>Cancelar</Button>
          <Button onClick={handleCreateTemplate} variant="contained" disabled={!templateName || loading}>
            {loading ? "Criando..." : "Criar Template"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Preview Template Dialog */}
      <Dialog open={previewDialogOpen} onClose={() => setPreviewDialogOpen(false)} maxWidth="lg" fullWidth>
        <DialogTitle>
          Visualizar Template: {selectedTemplate?.name}
        </DialogTitle>
        <DialogContent>
          <Paper sx={{ p: 2, bgcolor: "grey.50" }}>
            <Typography variant="h6" gutterBottom>
              Blocos do Relatório
            </Typography>
            <List>
              {templateBlocks.map((block, index) => (
                <ListItem key={block.id} sx={{ bgcolor: "white", mb: 1, borderRadius: 1 }}>
                  <DragIcon sx={{ mr: 2, color: "text.secondary" }} />
                  <ListItemText
                    primary={block.title || getBlockTypeLabel(block.block_type)}
                    secondary={`Tipo: ${getBlockTypeLabel(block.block_type)} | Largura: ${block.width_percentage}%`}
                  />
                  <ListItemSecondaryAction>
                    <Typography variant="caption" color="text.secondary">
                      #{block.position_order}
                    </Typography>
                  </ListItemSecondaryAction>
                </ListItem>
              ))}
            </List>
          </Paper>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setPreviewDialogOpen(false)}>Fechar</Button>
          <Button variant="contained" onClick={() => handleGenerateReport(selectedTemplate!)}>
            Gerar Relatório
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default ReportTemplatesPage;