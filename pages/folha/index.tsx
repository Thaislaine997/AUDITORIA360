// Migrated from src/frontend/pages/folha/PayrollPage.tsx
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
  LinearProgress,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from "@mui/material";
import {
  CloudUpload,
  CheckCircle,
  Warning,
  Info,
  Error,
  Refresh,
} from "@mui/icons-material";

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

const PayrollPage: React.FC = () => {
  const [selectedCompany, setSelectedCompany] = useState<number>(1);
  const [selectedMonth, setSelectedMonth] = useState<number>(new Date().getMonth() + 1);
  const [selectedYear, setSelectedYear] = useState<number>(new Date().getFullYear());
  const [uploadedFile, setUploadedFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState<boolean>(false);
  const [auditResult, setAuditResult] = useState<ProcessamentoFolhaResponse | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [auditProgress, setAuditProgress] = useState<number>(0);

  const handleFileChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const file = event.target.files?.[0];
    if (file && file.type === "application/pdf") {
      setUploadedFile(file);
      setError(null);
      setAuditResult(null);
    } else {
      setError("Por favor, selecione apenas arquivos PDF.");
    }
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
      // Simulate processing steps
      setAuditProgress(25);
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAuditProgress(50);
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAuditProgress(75);
      await new Promise(resolve => setTimeout(resolve, 1000));
      
      setAuditProgress(100);

      // Mock result for migration purposes
      const mockResult: ProcessamentoFolhaResponse = {
        id: 1,
        empresa_id: selectedCompany,
        mes: selectedMonth,
        ano: selectedYear,
        arquivo_pdf: uploadedFile.name,
        total_funcionarios: 10,
        total_divergencias: 2,
        status_processamento: "CONCLUÍDO",
        criado_em: new Date().toISOString(),
        divergencias: [
          {
            nome_funcionario: "João Silva",
            tipo_divergencia: "AVISO",
            descricao_divergencia: "Adicional noturno não aplicado",
            valor_encontrado: "R$ 0,00",
            valor_esperado: "R$ 150,00",
            campo_afetado: "adicional_noturno"
          }
        ]
      };
      
      setAuditResult(mockResult);
    } catch {
      setError("Erro ao processar auditoria");
    } finally {
      setProcessing(false);
    }
  };

  const resetForm = () => {
    setUploadedFile(null);
    setAuditResult(null);
    setError(null);
    setProcessing(false);
    setAuditProgress(0);
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
          <Typography variant="h4" gutterBottom>
            Motor de Auditoria Inteligente - Folha de Pagamento
          </Typography>
          <Button startIcon={<Refresh />} onClick={resetForm} variant="outlined">
            Nova Auditoria
          </Button>
        </Box>

        {/* Context Panel */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Typography variant="h6" gutterBottom>
            Contexto da Auditoria
          </Typography>
          <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={2} sx={{ mb: 2 }}>
            <FormControl sx={{ minWidth: 200 }}>
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
            <FormControl sx={{ minWidth: 120 }}>
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
            <FormControl sx={{ minWidth: 120 }}>
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
          </Box>
        </Paper>

        {!processing && !auditResult && (
          <>
            {/* Upload Area */}
            <Paper sx={{ p: 4, mb: 3, textAlign: "center" }}>
              <CloudUpload sx={{ fontSize: 48, color: "primary.main", mb: 2 }} />
              <Typography variant="h6" gutterBottom>
                {uploadedFile
                  ? `Arquivo selecionado: ${uploadedFile.name}`
                  : "Selecione a folha de pagamento em PDF"}
              </Typography>
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileChange}
                style={{ margin: "16px 0" }}
              />
              {uploadedFile && (
                <Box sx={{ mt: 2 }}>
                  <Button
                    variant="contained"
                    size="large"
                    onClick={handleAuditSubmit}
                    startIcon={<CheckCircle />}
                  >
                    Iniciar Auditoria
                  </Button>
                </Box>
              )}
            </Paper>
          </>
        )}

        {/* Processing Status */}
        {processing && (
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Processamento em Andamento
            </Typography>
            <LinearProgress variant="determinate" value={auditProgress} sx={{ mb: 2 }} />
            <Typography variant="body2" color="text.secondary">
              {auditProgress}% concluído
            </Typography>
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
          <Paper sx={{ p: 3, mb: 3 }}>
            <Typography variant="h6" gutterBottom>
              Sumário da Auditoria
            </Typography>
            <Box display="flex" flexDirection={{ xs: 'column', md: 'row' }} gap={3}>
              <Card sx={{ flex: 1 }}>
                <CardContent>
                  <Typography variant="h4" color="primary">
                    {auditResult.total_funcionarios}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Funcionários Auditados
                  </Typography>
                </CardContent>
              </Card>
              <Card sx={{ flex: 1 }}>
                <CardContent>
                  <Typography variant="h4" color={auditResult.total_divergencias > 0 ? "error" : "success"}>
                    {auditResult.total_divergencias}
                  </Typography>
                  <Typography variant="body2" color="text.secondary">
                    Divergências Encontradas
                  </Typography>
                </CardContent>
              </Card>
            </Box>
            <Chip
              label={`Status: ${auditResult.status_processamento}`}
              color="success"
              size="small"
              sx={{ mt: 2 }}
            />
          </Paper>
        )}
      </Box>
    </Container>
  );
};

export default PayrollPage;