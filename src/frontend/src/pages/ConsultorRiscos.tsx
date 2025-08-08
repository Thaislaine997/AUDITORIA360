import React, { useState, useEffect } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  TextField,
  Button,
  Grid,
  Card,
  CardContent,
  Chip,
  List,
  ListItem,
  ListItemText,
  Divider,
  IconButton,
  Modal,
  LinearProgress,
  Alert,
  Tooltip,
  CircularProgress,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import {
  Psychology,
  Send,
  History,
  TrendingUp,
  TrendingDown,
  TrendingFlat,
  Warning,
  CheckCircle,
  ThumbUp,
  ThumbDown,
  ExpandMore,
  Info,
  Close,
  Assessment,
  Business,
} from "@mui/icons-material";

// Import our new Risk Analysis Service
import RiskAnalysisService, { 
  type AnaliseRiscoResponse, 
  type RiscoDetalhado,
  type HistoricoAnaliseRisco 
} from "../services/riskAnalysisService";

const ConsultorRiscos: React.FC = () => {
  // State management for the real API integration
  const [selectedEmpresaId, setSelectedEmpresaId] = useState<number>(1); // Default test company
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<AnaliseRiscoResponse | null>(null);
  const [analysisError, setAnalysisError] = useState<string | null>(null);
  const [selectedRisk, setSelectedRisk] = useState<any>(null);
  const [drillDownModal, setDrillDownModal] = useState(false);
  const [feedback, setFeedback] = useState<{ [key: string]: 'positive' | 'negative' | null }>({});
  const [riskHistory, setRiskHistory] = useState<HistoricoAnaliseRisco[]>([]);
  
  // Load risk history when component mounts
  useEffect(() => {
    loadRiskHistory();
  }, [selectedEmpresaId]);

  const loadRiskHistory = async () => {
    try {
      const history = await RiskAnalysisService.obterHistoricoRiscos(selectedEmpresaId, 5);
      setRiskHistory(history);
    } catch (error) {
      console.warn('Could not load risk history:', error);
    }
  };

  const handleAnalyze = async () => {
    setIsAnalyzing(true);
    setAnalysisError(null);

    try {
      console.log(`🔮 Starting risk analysis for company ${selectedEmpresaId}`);
      
      const result = await RiskAnalysisService.analisarRiscos({ 
        empresa_id: selectedEmpresaId 
      });
      
      setAnalysisResult(result);
      
      // Reload history to show the new analysis
      await loadRiskHistory();
      
      console.log('✅ Risk analysis completed successfully');
    } catch (error: any) {
      console.error('❌ Risk analysis failed:', error);
      setAnalysisError(error.message || 'Erro desconhecido na análise de riscos');
    } finally {
      setIsAnalyzing(false);
    }
  };

  const handleFeedback = (riskId: number, type: 'positive' | 'negative') => {
    setFeedback(prev => ({ ...prev, [riskId]: type }));
    
    // RLHF v2.0 - Enhanced feedback submission
    fetch('/api/v1/ai/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recommendation_id: riskId,
        feedback_type: type,
        timestamp: new Date().toISOString(),
        user_context: {
          workspace: 'risk-analysis',
          session_id: sessionStorage.getItem('session_id'),
          empresa_id: selectedEmpresaId
        }
      })
    }).then(response => {
      if (response.ok) {
        console.log(`✅ RLHF feedback successfully submitted for risk ${riskId}: ${type}`);
      }
    }).catch(err => {
      console.warn('⚠️ RLHF feedback submission failed:', err);
    });
  };

  const handleDrillDown = (riskFactor: string) => {
    // Use real risk history data if available
    if (riskHistory.length > 0) {
      const mockHistorical = riskHistory.slice(0, 5).map((analysis, index) => ({
        month: new Date(analysis.data_analise).toLocaleDateString('pt-BR', { month: 'short' }),
        value: analysis.score_risco + Math.random() * 10 - 5 // Add some variation for demo
      }));
      
      setSelectedRisk({
        factor: riskFactor,
        historicalData: mockHistorical
      });
    } else {
      // Fallback to mock data
      setSelectedRisk({
        factor: riskFactor,
        historicalData: [
          { month: "Jan", value: 15 },
          { month: "Fev", value: 23 },
          { month: "Mar", value: 31 },
          { month: "Abr", value: 18 },
          { month: "Mai", value: 25 },
        ]
      });
    }
    setDrillDownModal(true);
  };

  const getConfidenceColor = (severidade: number) => {
    // Map severity to colors (5=critical, 1=low)
    if (severidade >= 4) return '#EF4444'; // High/Critical - red
    if (severidade >= 3) return '#F59E0B'; // Medium - orange
    if (severidade >= 2) return '#10B981'; // Low - green
    return '#6B7280'; // Very low - gray
  };

  const getTrendIcon = () => {
    if (!analysisResult?.score_anterior) return <TrendingFlat />;
    
    const trend = RiskAnalysisService.calculateTrend(
      analysisResult.score_risco,
      analysisResult.score_anterior
    );
    
    switch (trend.trend) {
      case 'up': return <TrendingUp color="success" />;
      case 'down': return <TrendingDown color="error" />;
      default: return <TrendingFlat color="disabled" />;
    }
  };

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          🔮 Consultor de Riscos
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          Análise preditiva inteligente para identificação proativa de riscos trabalhistas, fiscais e operacionais.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              🤖 Análise Inteligente de Riscos
            </Typography>
            
            {/* Company Selection */}
            <Box sx={{ mb: 3 }}>
              <FormControl fullWidth>
                <InputLabel>Empresa para Análise</InputLabel>
                <Select
                  value={selectedEmpresaId}
                  onChange={(e) => setSelectedEmpresaId(Number(e.target.value))}
                  label="Empresa para Análise"
                >
                  <MenuItem value={1}>Empresa Teste de Riscos S/A</MenuItem>
                  <MenuItem value={2}>Outra Empresa Ltda (Demo)</MenuItem>
                  <MenuItem value={3}>Empresa Exemplo ME (Demo)</MenuItem>
                </Select>
              </FormControl>
            </Box>

            {/* Analysis Trigger */}
            <Button
              variant="contained"
              size="large"
              startIcon={isAnalyzing ? <CircularProgress size={20} /> : <Assessment />}
              onClick={handleAnalyze}
              disabled={isAnalyzing}
              sx={{ mb: 3 }}
            >
              {isAnalyzing ? "Analisando..." : "Executar Nova Análise Completa"}
            </Button>

            {/* Analysis Progress */}
            {isAnalyzing && (
              <Box sx={{ mt: 2, mb: 3, p: 2, bgcolor: "grey.50", borderRadius: 1 }}>
                <Typography variant="body2" gutterBottom>
                  🤖 Consultor de Riscos processando análise...
                </Typography>
                {analysisResult?.progresso_analise && Object.entries(analysisResult.progresso_analise).map(([step, status]) => (
                  <Box key={step} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Typography variant="caption" sx={{ minWidth: 200 }}>
                      {step.replace(/_/g, ' ')}: 
                    </Typography>
                    <Typography variant="caption" color="success.main">
                      {status}
                    </Typography>
                  </Box>
                ))}
                <LinearProgress sx={{ mt: 2 }} />
              </Box>
            )}

            {/* Analysis Error */}
            {analysisError && (
              <Alert severity="error" sx={{ mb: 3 }}>
                <Typography variant="body2">
                  ❌ Erro na análise: {analysisError}
                </Typography>
              </Alert>
            )}

            {/* Analysis Results */}
            {analysisResult && (
              <Paper sx={{ mt: 3, p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Business sx={{ mr: 1 }} />
                  <Typography variant="h6">
                    📊 Relatório: {analysisResult.empresa_nome}
                  </Typography>
                </Box>
                
                {/* Risk Score Display */}
                <Box sx={{ mb: 3, p: 2, bgcolor: 'primary.light', borderRadius: 2 }}>
                  <Grid container spacing={2} alignItems="center">
                    <Grid item xs={12} md={4}>
                      <Typography variant="h3" color="primary" sx={{ fontWeight: 'bold' }}>
                        {analysisResult.score_risco}/100
                      </Typography>
                      <Typography variant="h6" color="primary">
                        Score de Risco
                      </Typography>
                      <Chip 
                        label={analysisResult.nivel_risco}
                        color={analysisResult.nivel_risco === 'BAIXO' ? 'success' : 
                               analysisResult.nivel_risco === 'MÉDIO' ? 'warning' : 'error'}
                        size="large"
                        sx={{ mt: 1 }}
                      />
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Typography variant="body2" color="text.secondary">
                        {RiskAnalysisService.formatScoreMessage(analysisResult.score_risco, analysisResult.nivel_risco)}
                      </Typography>
                      {analysisResult.score_anterior && (
                        <Box sx={{ display: 'flex', alignItems: 'center', mt: 1 }}>
                          {getTrendIcon()}
                          <Typography variant="caption" sx={{ ml: 1 }}>
                            {RiskAnalysisService.calculateTrend(
                              analysisResult.score_risco,
                              analysisResult.score_anterior
                            ).message}
                          </Typography>
                        </Box>
                      )}
                    </Grid>
                    <Grid item xs={12} md={4}>
                      <Typography variant="body2" color="text.secondary">
                        Última análise: {new Date(analysisResult.data_analise).toLocaleDateString('pt-BR')}
                      </Typography>
                      <Typography variant="body2" color="text.secondary">
                        Total de riscos: {analysisResult.total_riscos}
                      </Typography>
                    </Grid>
                  </Grid>
                </Box>

                {/* Risk Summary */}
                <Grid container spacing={2} sx={{ mb: 3 }}>
                  <Grid item xs={3}>
                    <Card sx={{ textAlign: 'center', bgcolor: 'error.light' }}>
                      <CardContent>
                        <Typography variant="h4" color="error">{analysisResult.riscos_criticos}</Typography>
                        <Typography variant="body2">Críticos</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={3}>
                    <Card sx={{ textAlign: 'center', bgcolor: 'warning.light' }}>
                      <CardContent>
                        <Typography variant="h4" color="warning.dark">{analysisResult.riscos_altos}</Typography>
                        <Typography variant="body2">Altos</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={3}>
                    <Card sx={{ textAlign: 'center', bgcolor: 'info.light' }}>
                      <CardContent>
                        <Typography variant="h4" color="info.dark">{analysisResult.riscos_medios}</Typography>
                        <Typography variant="body2">Médios</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                  <Grid item xs={3}>
                    <Card sx={{ textAlign: 'center', bgcolor: 'success.light' }}>
                      <CardContent>
                        <Typography variant="h4" color="success.dark">{analysisResult.riscos_baixos}</Typography>
                        <Typography variant="body2">Baixos</Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                </Grid>

                {/* Detailed Risk List */}
                <Typography variant="h6" gutterBottom>
                  🔍 Riscos Detalhados
                </Typography>
                {analysisResult.riscos_encontrados.map((risco: RiscoDetalhado, index: number) => (
                  <Card 
                    key={index} 
                    sx={{ 
                      mb: 2,
                      border: `2px solid ${getConfidenceColor(risco.severidade)}`,
                    }}
                  >
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                        <Box sx={{ flex: 1 }}>
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                            <Typography variant="body2" sx={{ mr: 1 }}>
                              {RiskAnalysisService.getCategoryIcon(risco.categoria)}
                            </Typography>
                            <Chip 
                              label={risco.categoria}
                              size="small"
                              color={risco.categoria === 'CONFORMIDADE' ? 'success' : 'default'}
                            />
                            <Chip 
                              label={`Severidade: ${risco.severidade}/5`}
                              size="small"
                              sx={{ ml: 1, bgcolor: getConfidenceColor(risco.severidade), color: 'white' }}
                            />
                          </Box>
                          
                          <Typography variant="h6" gutterBottom>
                            {risco.tipo_risco}
                          </Typography>
                          
                          <Typography variant="body2" color="text.secondary" paragraph>
                            <strong>Descrição:</strong> {risco.descricao}
                          </Typography>
                          
                          <Typography variant="body2" color="text.secondary" paragraph>
                            <strong>Evidência:</strong> {risco.evidencia}
                          </Typography>
                          
                          <Typography variant="body2" color="error" paragraph>
                            <strong>Impacto Potencial:</strong> {risco.impacto_potencial}
                          </Typography>
                          
                          <Typography variant="body2" color="primary" paragraph>
                            <strong>Plano de Ação:</strong> {risco.plano_acao}
                          </Typography>
                        </Box>

                        {/* Feedback Mechanism */}
                        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', ml: 2 }}>
                          <Typography variant="caption" sx={{ mb: 1 }}>
                            Esta análise foi útil?
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Tooltip title="Análise útil">
                              <IconButton
                                size="small"
                                color={feedback[index] === 'positive' ? 'success' : 'default'}
                                onClick={() => handleFeedback(index, 'positive')}
                              >
                                <ThumbUp />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Análise não útil">
                              <IconButton
                                size="small"
                                color={feedback[index] === 'negative' ? 'error' : 'default'}
                                onClick={() => handleFeedback(index, 'negative')}
                              >
                                <ThumbDown />
                              </IconButton>
                            </Tooltip>
                          </Box>
                          {feedback[index] && (
                            <Typography variant="caption" sx={{ mt: 1, color: 'text.secondary' }}>
                              Obrigado pelo feedback!
                            </Typography>
                          )}
                        </Box>
                      </Box>
                    </CardContent>
                  </Card>
                ))}
              </Paper>
            )}
          </Paper>

          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              📈 Histórico de Análises
            </Typography>
            
            {riskHistory.length > 0 ? (
              riskHistory.map((analise, index) => (
                <Card key={analise.id} sx={{ mb: 2 }}>
                  <CardContent sx={{ p: 2, "&:last-child": { pb: 2 } }}>
                    <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 1 }}>
                      <Typography variant="body2" color="text.secondary">
                        {new Date(analise.data_analise).toLocaleDateString('pt-BR')}
                      </Typography>
                      <Typography variant="h6" color="primary">
                        {analise.score_risco}/100
                      </Typography>
                    </Box>
                    
                    <Chip 
                      label={analise.relatorio_resumo.nivel_risco}
                      size="small"
                      color={
                        analise.relatorio_resumo.nivel_risco === 'BAIXO' ? 'success' : 
                        analise.relatorio_resumo.nivel_risco === 'MÉDIO' ? 'warning' : 'error'
                      }
                      sx={{ mb: 1 }}
                    />
                    
                    <Typography variant="body2" color="text.secondary">
                      {analise.relatorio_resumo.total_riscos} riscos identificados
                    </Typography>
                    
                    {/* Category breakdown */}
                    <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap', mt: 1 }}>
                      {Object.entries(analise.relatorio_resumo.categorias).map(([categoria, count]) => (
                        count > 0 && (
                          <Chip
                            key={categoria}
                            label={`${categoria}: ${count}`}
                            size="small"
                            variant="outlined"
                            sx={{ fontSize: '0.6rem', height: '16px' }}
                          />
                        )
                      ))}
                    </Box>
                  </CardContent>
                </Card>
              ))
            ) : (
              <Alert severity="info">
                <Typography variant="body2">
                  Nenhuma análise anterior encontrada. Execute uma análise para começar o histórico.
                </Typography>
              </Alert>
            )}
          </Paper>

          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              ℹ️ Como Funciona
            </Typography>
            <List dense>
              <ListItem>
                <ListItemText 
                  primary="1. Agregação de Dados"
                  secondary="Coleta dados dos últimos 12-24 meses da empresa"
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText 
                  primary="2. Análise de Conformidade"
                  secondary="Verifica conformidade trabalhista e fiscal"
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText 
                  primary="3. Detecção de Padrões"
                  secondary="IA identifica anomalias e riscos ocultos"
                />
              </ListItem>
              <Divider />
              <ListItem>
                <ListItemText 
                  primary="4. Recomendações"
                  secondary="Gera planos de ação específicos"
                />
              </ListItem>
            </List>
          </Paper>
        </Grid>
      </Grid>

      {/* Drill-Down Modal for Risk Factor Details */}
      <Modal
        open={drillDownModal}
        onClose={() => setDrillDownModal(false)}
        aria-labelledby="drill-down-modal"
      >
        <Box sx={{
          position: 'absolute',
          top: '50%',
          left: '50%',
          transform: 'translate(-50%, -50%)',
          width: 600,
          bgcolor: 'background.paper',
          borderRadius: 2,
          boxShadow: 24,
          p: 4,
          maxHeight: '80vh',
          overflow: 'auto'
        }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
            <Typography variant="h6" component="h2">
              📊 Análise Detalhada: {selectedRisk?.factor}
            </Typography>
            <IconButton onClick={() => setDrillDownModal(false)}>
              <Close />
            </IconButton>
          </Box>
          
          {selectedRisk && (
            <Box>
              <Alert severity="info" sx={{ mb: 2 }}>
                <Typography variant="body2">
                  Dados históricos dos últimos 5 meses para o fator de risco "{selectedRisk.factor}"
                </Typography>
              </Alert>
              
              {/* Mock chart data - in real implementation would use recharts */}
              <Paper sx={{ p: 2, bgcolor: 'grey.50' }}>
                <Typography variant="subtitle2" gutterBottom>
                  Tendência Temporal
                </Typography>
                {selectedRisk.historicalData.map((data: any, index: number) => (
                  <Box key={index} sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Typography variant="body2" sx={{ minWidth: 40 }}>
                      {data.month}:
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={(data.value / 35) * 100} 
                      sx={{ flex: 1, ml: 1, mr: 1 }}
                    />
                    <Typography variant="body2" sx={{ minWidth: 30 }}>
                      {data.value}
                    </Typography>
                  </Box>
                ))}
              </Paper>
              
              <Box sx={{ mt: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  Recomendações Específicas
                </Typography>
                <Typography variant="body2" color="text.secondary">
                  • Monitorar variações acima de 20% em relação ao mês anterior
                  • Revisar políticas internas relacionadas a este fator
                  • Considerar automação para reduzir erros manuais
                </Typography>
              </Box>
            </Box>
          )}
        </Box>
      </Modal>
    </Container>
  );
};

export default ConsultorRiscos;