// Migrated from src/frontend/pages/ia/ValidacaoIAPage.tsx
import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  TextField,
  Alert,
  LinearProgress,
  Card,
  CardContent,
  Chip,
} from "@mui/material";
import {
  Psychology,
  CheckCircle,
  Error,
  Warning,
} from "@mui/icons-material";

interface ValidationResult {
  id: string;
  input: string;
  output: string;
  confidence: number;
  status: 'APROVADO' | 'REJEITADO' | 'PENDENTE';
  feedback?: string;
}

const ValidacaoIAPage: React.FC = () => {
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [results, setResults] = useState<ValidationResult[]>([
    {
      id: '1',
      input: 'Calcular adicional noturno para funcionário',
      output: 'Adicional noturno deve ser 20% sobre o valor da hora normal, aplicado das 22h às 5h.',
      confidence: 0.95,
      status: 'APROVADO',
      feedback: 'Resposta correta e completa'
    },
    {
      id: '2',
      input: 'Como calcular férias proporcionais?',
      output: 'Férias proporcionais = (salário / 12) × meses trabalhados',
      confidence: 0.88,
      status: 'PENDENTE'
    }
  ]);

  const handleValidate = async () => {
    if (!input.trim()) return;

    setLoading(true);
    
    // Simulate AI processing
    setTimeout(() => {
      const newResult: ValidationResult = {
        id: Date.now().toString(),
        input: input,
        output: 'Esta é uma resposta simulada do sistema de IA. A validação real será implementada em breve.',
        confidence: Math.random() * 0.4 + 0.6, // Random confidence between 0.6-1.0
        status: 'PENDENTE'
      };
      
      setResults(prev => [newResult, ...prev]);
      setInput('');
      setLoading(false);
    }, 2000);
  };

  const getStatusIcon = (status: string) => {
    switch (status) {
      case 'APROVADO': return <CheckCircle color="success" />;
      case 'REJEITADO': return <Error color="error" />;
      case 'PENDENTE': return <Warning color="warning" />;
      default: return null;
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'APROVADO': return 'success';
      case 'REJEITADO': return 'error';
      case 'PENDENTE': return 'warning';
      default: return 'default';
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Validação de IA
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Sistema de validação e treinamento para respostas da Inteligência Artificial
        </Typography>

        {/* Input Section */}
        <Paper sx={{ p: 3, mb: 4 }}>
          <Typography variant="h6" gutterBottom>
            Testar Nova Consulta
          </Typography>
          <Box display="flex" gap={2} alignItems="start">
            <TextField
              fullWidth
              label="Digite uma pergunta para testar a IA"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              multiline
              rows={3}
              disabled={loading}
            />
            <Button
              variant="contained"
              onClick={handleValidate}
              disabled={loading || !input.trim()}
              startIcon={<Psychology />}
              sx={{ minWidth: 120 }}
            >
              Validar
            </Button>
          </Box>
          {loading && (
            <Box sx={{ mt: 2 }}>
              <LinearProgress />
              <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                Processando consulta com IA...
              </Typography>
            </Box>
          )}
        </Paper>

        {/* Results */}
        <Typography variant="h6" gutterBottom>
          Resultados de Validação
        </Typography>
        
        {results.length === 0 ? (
          <Alert severity="info">
            Nenhuma validação realizada ainda. Teste uma consulta acima.
          </Alert>
        ) : (
          <Box display="flex" flexDirection="column" gap={2}>
            {results.map((result) => (
              <Card key={result.id}>
                <CardContent>
                  <Box display="flex" justifyContent="between" alignItems="start" mb={2}>
                    <Box flex={1}>
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Pergunta:
                      </Typography>
                      <Typography variant="body2" paragraph>
                        {result.input}
                      </Typography>
                      
                      <Typography variant="subtitle1" fontWeight="bold" gutterBottom>
                        Resposta da IA:
                      </Typography>
                      <Typography variant="body2" paragraph>
                        {result.output}
                      </Typography>
                      
                      <Box display="flex" gap={2} alignItems="center">
                        <Chip
                          icon={getStatusIcon(result.status)}
                          label={result.status}
                          color={getStatusColor(result.status) as any}
                          size="small"
                        />
                        <Typography variant="caption" color="text.secondary">
                          Confiança: {(result.confidence * 100).toFixed(1)}%
                        </Typography>
                      </Box>
                      
                      {result.feedback && (
                        <Alert severity="info" sx={{ mt: 2 }}>
                          <strong>Feedback:</strong> {result.feedback}
                        </Alert>
                      )}
                    </Box>
                  </Box>
                </CardContent>
              </Card>
            ))}
          </Box>
        )}
      </Box>
    </Container>
  );
};

export default ValidacaoIAPage;