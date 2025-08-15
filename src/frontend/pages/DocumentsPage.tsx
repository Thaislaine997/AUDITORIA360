import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Paper,
  Box,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  Chip,
  IconButton,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
  InputAdornment,
  Tooltip,
} from "@mui/material";
import {
  Search as SearchIcon,
  Visibility as ViewIcon,
  Download as DownloadIcon,
  CloudUpload as UploadIcon,
} from "@mui/icons-material";
import ExportButton from "../components/ExportButton";

interface Document {
  id: number;
  title: string;
  category: string;
  upload_date: string;
  size: string;
  uploaded_by: string;
  status?: string;
}

const DocumentsPage: React.FC = () => {
  const [documents, setDocuments] = useState<Document[]>([]);
  const [filteredDocuments, setFilteredDocuments] = useState<Document[]>([]);
  const [categoryFilter, setCategoryFilter] = useState("");
  const [searchTerm, setSearchTerm] = useState("");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetchDocuments();
  }, []);

  useEffect(() => {
    // Apply filters
    let filtered = documents;
    
    if (categoryFilter) {
      filtered = filtered.filter(doc => doc.category === categoryFilter);
    }
    
    if (searchTerm) {
      filtered = filtered.filter(doc => 
        doc.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
        doc.uploaded_by.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    setFilteredDocuments(filtered);
  }, [documents, categoryFilter, searchTerm]);

  const fetchDocuments = async () => {
    setLoading(true);
    // TODO: Replace with actual API call
    const mockDocuments: Document[] = [
      {
        id: 1,
        title: "Nota Fiscal 001.pdf",
        category: "fiscal",
        upload_date: "2024-01-10T09:30:00Z",
        size: "2.5 MB",
        uploaded_by: "Cliente ABC",
        status: "processed"
      },
      {
        id: 2,
        title: "Contrato Social.pdf",
        category: "legal",
        upload_date: "2024-01-08T14:15:00Z", 
        size: "1.8 MB",
        uploaded_by: "Empresa XYZ",
        status: "processing"
      },
      {
        id: 3,
        title: "Comprovante Pagamento.pdf",
        category: "payment",
        upload_date: "2024-01-12T11:20:00Z",
        size: "750 KB",
        uploaded_by: "Fornecedor ABC",
        status: "processed"
      },
      {
        id: 4,
        title: "Relatório Contábil Dezembro.xlsx",
        category: "report",
        upload_date: "2024-01-05T16:45:00Z",
        size: "3.2 MB",
        uploaded_by: "Contabilidade Santos",
        status: "processed"
      }
    ];
    
    setDocuments(mockDocuments);
    setLoading(false);
  };

  const handleExportPdf = async () => {
    // TODO: Implement actual PDF export
    console.log("Exporting documents to PDF");
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
  };

  const handleExportCsv = async () => {
    // TODO: Implement actual CSV export
    console.log("Exporting documents to CSV");
    // Simulate API call
    await new Promise(resolve => setTimeout(resolve, 1000));
  };

  const getCategoryLabel = (category: string) => {
    switch (category) {
      case "fiscal":
        return "Fiscal";
      case "legal":
        return "Jurídico";
      case "payment":
        return "Pagamento";
      case "report":
        return "Relatório";
      default:
        return "Outros";
    }
  };

  const getCategoryColor = (category: string) => {
    switch (category) {
      case "fiscal":
        return "primary";
      case "legal":
        return "secondary";
      case "payment":
        return "success";
      case "report":
        return "info";
      default:
        return "default";
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case "processed":
        return "success";
      case "processing":
        return "warning";
      case "error":
        return "error";
      default:
        return "default";
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString("pt-BR", {
      day: "2-digit",
      month: "2-digit",
      year: "numeric",
      hour: "2-digit",
      minute: "2-digit"
    });
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Documentos
        </Typography>
        <Box sx={{ display: "flex", gap: 2 }}>
          <ExportButton
            onExportPdf={handleExportPdf}
            onExportCsv={handleExportCsv}
          />
          <Button
            variant="contained"
            startIcon={<UploadIcon />}
          >
            Upload Documento
          </Button>
        </Box>
      </Box>

      {/* Filters */}
      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: "flex", gap: 2, flexWrap: "wrap" }}>
          <TextField
            placeholder="Buscar documentos..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
            }}
            sx={{ minWidth: 300 }}
          />
          <FormControl sx={{ minWidth: 200 }}>
            <InputLabel>Categoria</InputLabel>
            <Select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
            >
              <MenuItem value="">Todas</MenuItem>
              <MenuItem value="fiscal">Fiscal</MenuItem>
              <MenuItem value="legal">Jurídico</MenuItem>
              <MenuItem value="payment">Pagamento</MenuItem>
              <MenuItem value="report">Relatório</MenuItem>
            </Select>
          </FormControl>
          <Button 
            variant="outlined"
            onClick={() => {
              setCategoryFilter("");
              setSearchTerm("");
            }}
          >
            Limpar Filtros
          </Button>
        </Box>
      </Paper>

      {/* Documents Table */}
      <TableContainer component={Paper}>
        <Table>
          <TableHead>
            <TableRow>
              <TableCell>Documento</TableCell>
              <TableCell>Categoria</TableCell>
              <TableCell>Data Upload</TableCell>
              <TableCell>Tamanho</TableCell>
              <TableCell>Enviado por</TableCell>
              <TableCell>Status</TableCell>
              <TableCell align="center">Ações</TableCell>
            </TableRow>
          </TableHead>
          <TableBody>
            {filteredDocuments.map((document) => (
              <TableRow key={document.id} hover>
                <TableCell>
                  <Typography variant="body2" fontWeight="medium">
                    {document.title}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Chip
                    label={getCategoryLabel(document.category)}
                    color={getCategoryColor(document.category) as any}
                    size="small"
                    variant="outlined"
                  />
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {formatDate(document.upload_date)}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {document.size}
                  </Typography>
                </TableCell>
                <TableCell>
                  <Typography variant="body2">
                    {document.uploaded_by}
                  </Typography>
                </TableCell>
                <TableCell>
                  {document.status && (
                    <Chip
                      label={document.status === "processed" ? "Processado" : 
                            document.status === "processing" ? "Processando" : "Erro"}
                      color={getStatusColor(document.status) as any}
                      size="small"
                    />
                  )}
                </TableCell>
                <TableCell align="center">
                  <Box sx={{ display: "flex", gap: 1, justifyContent: "center" }}>
                    <Tooltip title="Visualizar">
                      <IconButton size="small">
                        <ViewIcon />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Download">
                      <IconButton size="small">
                        <DownloadIcon />
                      </IconButton>
                    </Tooltip>
                  </Box>
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>

      {filteredDocuments.length === 0 && !loading && (
        <Paper sx={{ p: 4, textAlign: "center", mt: 3 }}>
          <Typography variant="body1" color="text.secondary">
            {searchTerm || categoryFilter ? "Nenhum documento encontrado com os filtros aplicados." : "Nenhum documento encontrado."}
          </Typography>
        </Paper>
      )}
    </Container>
  );
};

export default DocumentsPage;
