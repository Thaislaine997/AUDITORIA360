/**
 * 🚀 PayrollPage - AI-Powered Payroll Auditing System
 * Motor de Auditoria Inteligente da Folha de Pagamento
 */

import React, { useState, useCallback } from "react";
import {
  Container,
  Typography,
  Paper,
  Box,
  Grid,
  Card,
  CardContent,
  Button,
  Chip,
  CircularProgress,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  LinearProgress,
  Collapse,
  IconButton,
  Tooltip,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import {
  CloudUpload,
  CheckCircle,
  Warning,
  Info,
  Error,
  Visibility,
  Download,
  Refresh,
} from "@mui/icons-material";
import { useDropzone } from "react-dropzone";

interface FuncionarioDivergencia {
  nome_funcionario: string;
  tipo_divergencia: "ALERTA" | "AVISO" | "INFO";
  descricao_divergencia: string;
  valor_encontrado?: string;
  valor_esperado?: string;
  campo_afetado: string;
}

interface ProcessamentoFolhaResponse {
  id: number;
  empresa_id: number;
  mes: number;
  ano: number;
  arquivo_pdf: string;
  total_funcionarios: number;
  total_divergencias: number;
  status_processamento: string;
  criado_em: string;
  concluido_em?: string;
  divergencias: FuncionarioDivergencia[];
}

interface AuditStep {
  id: string;
  label: string;
  completed: boolean;
  inProgress: boolean;
}

const PayrollPage: React.FC = () => {
  const [selectedCompany, setSelectedCompany] = useState<number>(1);
  const [selectedMonth, setSelectedMonth] = useState<number>(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState<number>(new Date().getFullYear());
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState<boolean>(false);
  const [auditResult, setAuditResult] = useState<ProcessamentoFolhaResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [auditProgress, setAuditProgress] = useState<number>(0);
  const [auditSteps, setAuditSteps] = useState<AuditStep[]>([
    { id: "upload", label: "PDF(s) recebidos com sucesso", completed: false, inProgress: false },
    { id: "extract", label: "Lendo e extraindo dados do ficheiro", completed: false, inProgress: false },
    { id: "identify", label: "Identificando verbas e funcionários", completed: false, inProgress: false },
    { id: "audit", label: "Cruzando dados com as regras da CCT", completed: false, inProgress: false },
    { id: "report", label: "Compilando o relatório de divergências", completed: false, inProgress: false },
  ]);

  const onDrop = useCallback((acceptedFiles: File[]) => {
    const file = acceptedFiles[0];
    if (file && file.type === "application/pdf") {
      setUploadedFile(file);
      setError(null);
      setAuditResult(null);
    } else {
      setError("Por favor, arraste apenas arquivos PDF.");
    }
  }, []);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      "application/pdf": [".pdf"],
    },
    multiple: false,
  });

  const simulateAuditSteps = async () => {
    const steps = [...auditSteps];
    
    // Step 1: Upload completed
    steps[0].completed = true;
    setAuditSteps([...steps]);
    setAuditProgress(20);

    // Step 2: Extracting
    await new Promise(resolve => setTimeout(resolve, 1000));
    steps[1].inProgress = true;
    setAuditSteps([...steps]);
    
    await new Promise(resolve => setTimeout(resolve, 1500));
    steps[1].completed = true;
    steps[1].inProgress = false;
    setAuditSteps([...steps]);
    setAuditProgress(40);

    // Step 3: Identifying
    await new Promise(resolve => setTimeout(resolve, 800));
    steps[2].inProgress = true;
    setAuditSteps([...steps]);
    
    await new Promise(resolve => setTimeout(resolve, 1200));
    steps[2].completed = true;
    steps[2].inProgress = false;
    setAuditSteps([...steps]);
    setAuditProgress(65);

    // Step 4: Auditing
    await new Promise(resolve => setTimeout(resolve, 1000));
    steps[3].inProgress = true;
    setAuditSteps([...steps]);
    
    await new Promise(resolve => setTimeout(resolve, 1800));
    steps[3].completed = true;
    steps[3].inProgress = false;
    setAuditSteps([...steps]);
    setAuditProgress(85);

    // Step 5: Report generation
    await new Promise(resolve => setTimeout(resolve, 500));
    steps[4].inProgress = true;
    setAuditSteps([...steps]);
    
    await new Promise(resolve => setTimeout(resolve, 1000));
    steps[4].completed = true;
    steps[4].inProgress = false;
    setAuditSteps([...steps]);
    setAuditProgress(100);
  };

  const handleAuditSubmit = async () => {
    if (!uploadedFile) {
      setError("Por favor, selecione um arquivo PDF.");
      return;
    }

    setProcessing(true);
    setError(null);
    setAuditProgress(0);

    try {
      // Reset audit steps
      const resetSteps = auditSteps.map(step => ({ ...step, completed: false, inProgress: false }));
      setAuditSteps(resetSteps);

      // Start progress simulation
      await simulateAuditSteps();

      // Create form data
      const formData = new FormData();
      formData.append("arquivo_pdf", uploadedFile);

      // Make API request
      const response = await fetch(
        `http://localhost:8001/v1/folha/auditar?empresa_id=${selectedCompany}&mes=${selectedMonth}&ano=${selectedYear}`,
        {
          method: "POST",
          body: formData,
        }
      );

      if (!response.ok) {
        const errorData = await response.json();
        throw new Error(errorData.detail || "Erro no processamento da auditoria");
      }

      const result: ProcessamentoFolhaResponse = await response.json();
      setAuditResult(result);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Erro desconhecido");
    } finally {
      setProcessing(false);
    }
  };

  const getDivergenceIcon = (tipo: string) => {
    switch (tipo) {
      case "ALERTA":
        return <Error color="error" />;
      case "AVISO":
        return <Warning color="warning" />;
      case "INFO":
        return <Info color="info" />;
      default:
        return <Info />;
    }
  };

  const getDivergenceColor = (tipo: string) => {
    switch (tipo) {
      case "ALERTA":
        return "error";
      case "AVISO":
        return "warning";
      case "INFO":
        return "info";
      default:
        return "default";
    }
  };

  const resetForm = () => {
    setUploadedFile(null);
    setAuditResult(null);
    setError(null);
    setProcessing(false);
    setAuditProgress(0);
    const resetSteps = auditSteps.map(step => ({ ...step, completed: false, inProgress: false }));
    setAuditSteps(resetSteps);
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
        <Typography variant="h4" gutterBottom>
          Motor de Auditoria Inteligente - Folha de Pagamento
        </Typography>
        <Button startIcon={<Refresh />} onClick={resetForm} variant="outlined">
          Nova Auditoria
        </Button>
      </Box>

      {/* Context Panel */}
      <Paper sx={{ p: 3, mb: 3, backgroundColor: "#f8f9fa" }}>
        <Typography variant="h6" gutterBottom>
          Contexto da Auditoria
        </Typography>
        <Grid container spacing={2} sx={{ mb: 2 }}>
          <Grid item xs={12} md={4}>
            <FormControl fullWidth>
              <InputLabel>Empresa</InputLabel>
              <Select
                value={selectedCompany}
                onChange={(e) => setSelectedCompany(e.target.value as number)}
                disabled={processing}
              >
                <MenuItem value={1}>Empresa Modelo Ltda</MenuItem>
                <MenuItem value={2}>Comércio ABC S/A</MenuItem>
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={6} md={4}>
            <FormControl fullWidth>
              <InputLabel>Mês</InputLabel>
              <Select
                value={selectedMonth}
                onChange={(e) => setSelectedMonth(e.target.value as number)}
                disabled={processing}
              >
                {Array.from({ length: 12 }, (_, i) => (
                  <MenuItem key={i + 1} value={i + 1}>
                    {String(i + 1).padStart(2, "0")}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
          <Grid item xs={6} md={4}>
            <FormControl fullWidth>
              <InputLabel>Ano</InputLabel>
              <Select
                value={selectedYear}
                onChange={(e) => setSelectedYear(e.target.value as number)}
                disabled={processing}
              >
                {Array.from({ length: 5 }, (_, i) => (
                  <MenuItem key={2020 + i} value={2020 + i}>
                    {2020 + i}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
          </Grid>
        </Grid>
        <Typography variant="body2" color="text.secondary">
          A auditoria será feita com base na CCT do Sindicato dos Comerciários, vigente de 01/01/2025 a 31/12/2025.
        </Typography>
      </Paper>

      {!processing && !auditResult && (
        <>
          {/* Upload Area */}
          <Paper
            {...getRootProps()}
            sx={{
              p: 4,
              mb: 3,
              border: "2px dashed",
              borderColor: isDragActive ? "primary.main" : "grey.300",
              backgroundColor: isDragActive ? "action.hover" : "background.paper",
              cursor: "pointer",
              textAlign: "center",
              transition: "all 0.2s ease-in-out",
              "&:hover": {
                borderColor: "primary.main",
                backgroundColor: "action.hover",
              },
            }}
          >
            <input {...getInputProps()} />
            <CloudUpload sx={{ fontSize: 48, color: "primary.main", mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {uploadedFile
                ? `Arquivo selecionado: ${uploadedFile.name}`
                : "Arraste para aqui os extratos da folha de pagamento em PDF"}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {uploadedFile
                ? "Clique em 'Iniciar Auditoria' para processar"
                : "ou clique para selecionar arquivo"}
            </Typography>
          </Paper>

          {uploadedFile && (
            <Box sx={{ textAlign: "center", mb: 3 }}>
              <Button
                variant="contained"
                size="large"
                onClick={handleAuditSubmit}
                startIcon={<CheckCircle />}
                sx={{ minWidth: 200 }}
              >
                Iniciar Auditoria
              </Button>
            </Box>
          )}
        </>
      )}

      {/* Processing Status */}
      {processing && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Processamento em Andamento
          </Typography>
          <LinearProgress variant="determinate" value={auditProgress} sx={{ mb: 2 }} />
          <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
            {auditProgress}% concluído
          </Typography>

          {auditSteps.map((step, index) => (
            <Box key={step.id} sx={{ display: "flex", alignItems: "center", mb: 1 }}>
              {step.completed ? (
                <CheckCircle color="success" sx={{ mr: 1 }} />
              ) : step.inProgress ? (
                <CircularProgress size={20} sx={{ mr: 1 }} />
              ) : (
                <Box sx={{ width: 20, height: 20, mr: 1 }} />
              )}
              <Typography
                variant="body2"
                color={step.completed ? "success.main" : step.inProgress ? "primary.main" : "text.secondary"}
              >
                {step.label}
              </Typography>
            </Box>
          ))}
        </Paper>
      )}

      {/* Error Display */}
      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {/* Audit Results */}
      {auditResult && (
        <>
          {/* Summary */}
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Sumário da Auditoria
            </Typography>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h4" color="primary">
                      {auditResult.total_funcionarios}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Funcionários Auditados
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
              <Grid item xs={12} md={6}>
                <Card>
                  <CardContent>
                    <Typography variant="h4" color={auditResult.total_divergencias > 0 ? "error" : "success"}>
                      {auditResult.total_divergencias}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      Divergências Encontradas
                    </Typography>
                  </CardContent>
                </Card>
              </Grid>
            </Grid>
            <Typography variant="body1" sx={{ mt: 2 }}>
              Auditoria Concluída: {auditResult.total_divergencias} divergências encontradas em{" "}
              {auditResult.total_funcionarios} funcionários.
            </Typography>
            <Chip
              label={`Status: ${auditResult.status_processamento}`}
              color="success"
              size="small"
              sx={{ mt: 1 }}
            />
          </Paper>

          {/* Divergences List */}
          {auditResult.divergencias.length > 0 && (
            <Paper sx={{ p: 3, mb: 3 }}>
              <Typography variant="h6" gutterBottom>
                Lista de Divergências (Ação Necessária)
              </Typography>
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Tipo</TableCell>
                      <TableCell>Funcionário</TableCell>
                      <TableCell>Descrição</TableCell>
                      <TableCell>Valor Encontrado</TableCell>
                      <TableCell>Valor Esperado</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {auditResult.divergencias.map((divergencia, index) => (
                      <TableRow key={index}>
                        <TableCell>
                          <Box sx={{ display: "flex", alignItems: "center" }}>
                            {getDivergenceIcon(divergencia.tipo_divergencia)}
                            <Chip
                              label={divergencia.tipo_divergencia}
                              color={getDivergenceColor(divergencia.tipo_divergencia) as any}
                              size="small"
                              sx={{ ml: 1 }}
                            />
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" fontWeight="medium">
                            {divergencia.nome_funcionario}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">{divergencia.descricao_divergencia}</Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {divergencia.valor_encontrado || "N/A"}
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2">
                            {divergencia.valor_esperado || "N/A"}
                          </Typography>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </Paper>
          )}

          {/* PDF Preview Placeholder */}
          <Paper sx={{ p: 3, textAlign: "center" }}>
            <Typography variant="h6" gutterBottom>
              Visualizador de Extratos
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Pré-visualização do PDF original com as áreas de divergências destacadas
            </Typography>
            <Box
              sx={{
                border: "1px dashed grey.300",
                p: 4,
                backgroundColor: "grey.50",
                minHeight: 200,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Typography variant="body1" color="text.secondary">
                📄 PDF: {auditResult.arquivo_pdf}
                <br />
                (Visualizador será implementado em versão futura)
              </Typography>
            </Box>
            <Box sx={{ mt: 2 }}>
              <Button startIcon={<Visibility />} variant="outlined" sx={{ mr: 1 }}>
                Visualizar PDF
              </Button>
              <Button startIcon={<Download />} variant="outlined">
                Baixar Relatório
              </Button>
            </Box>
          </Paper>
        </>
      )}
    </Container>
  );
};

export default PayrollPage;
