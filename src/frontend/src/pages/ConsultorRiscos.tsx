import React, { useState } from "react";
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
} from "@mui/material";
import {
  Psychology,
  Send,
  History,
  TrendingUp,
  Warning,
  CheckCircle,
  ThumbUp,
  ThumbDown,
  ExpandMore,
  Info,
  Close,
} from "@mui/icons-material";

const ConsultorRiscos: React.FC = () => {
  const [query, setQuery] = useState("");
  const [isAnalyzing, setIsAnalyzing] = useState(false);
  const [analysisResult, setAnalysisResult] = useState<any>(null);
  const [selectedRisk, setSelectedRisk] = useState<any>(null);
  const [drillDownModal, setDrillDownModal] = useState(false);
  const [feedback, setFeedback] = useState<{ [key: string]: 'positive' | 'negative' | null }>({});

  const handleAnalyze = () => {
    setIsAnalyzing(true);
    // Simulate AI analysis with confidence intervals
    setTimeout(() => {
      setAnalysisResult({
        recommendations: [
          {
            id: 1,
            title: "Risco de Horas Extra Irregulares",
            description: "Identificadas variações atípicas no padrão de horas extras",
            confidence: 0.87,
            priority: "high",
            factors: ["Variação de Horas Extra", "Padrão Temporal", "Histórico de Funcionário"]
          },
          {
            id: 2,
            title: "Conformidade com Adicional Noturno",
            description: "Possível não conformidade com cálculo de adicional noturno",
            confidence: 0.73,
            priority: "medium",
            factors: ["Horário de Trabalho", "Legislação CCT", "Cálculo Automático"]
          }
        ]
      });
      setIsAnalyzing(false);
    }, 3000);
  };

  const handleFeedback = (recommendationId: string, type: 'positive' | 'negative') => {
    setFeedback(prev => ({ ...prev, [recommendationId]: type }));
    
    // RLHF v2.0 - Enhanced feedback submission
    fetch('/api/v1/ai/feedback', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        recommendation_id: recommendationId,
        feedback_type: type,
        timestamp: new Date().toISOString(),
        user_context: {
          workspace: 'audit',
          session_id: sessionStorage.getItem('session_id'),
          analysis_confidence: analysisResult?.recommendations?.find((r: any) => r.id === recommendationId)?.confidence
        }
      })
    }).then(response => {
      if (response.ok) {
        console.log(`✅ RLHF feedback successfully submitted for recommendation ${recommendationId}: ${type}`);
      }
    }).catch(err => {
      console.warn('⚠️ RLHF feedback submission failed:', err);
    });
  };

  const handleDrillDown = (riskFactor: string) => {
    // Simulate fetching historical data for the risk factor
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
    setDrillDownModal(true);
  };

  const getConfidenceColor = (confidence: number) => {
    if (confidence >= 0.8) return '#10B981'; // High confidence - green
    if (confidence >= 0.6) return '#F59E0B'; // Medium confidence - yellow
    return '#EF4444'; // Low confidence - red
  };

  const getConfidenceOpacity = (confidence: number) => {
    return 0.3 + (confidence * 0.7); // Range from 0.3 to 1.0
  };

  const riskCategories = [
    { 
      name: "Riscos Trabalhistas", 
      level: "Alto", 
      count: 12, 
      color: "error",
      confidence: 0.92,
      factors: ["Horas Extra", "Adicional Noturno", "Férias"] 
    },
    { 
      name: "Conformidade Fiscal", 
      level: "Médio", 
      count: 8, 
      color: "warning",
      confidence: 0.78,
      factors: ["FGTS", "INSS", "IRRF"] 
    },
    { 
      name: "Cálculos de Folha", 
      level: "Baixo", 
      count: 3, 
      color: "success",
      confidence: 0.95,
      factors: ["Salário Base", "Benefícios", "Descontos"] 
    },
    { 
      name: "Documentação", 
      level: "Médio", 
      count: 5, 
      color: "warning",
      confidence: 0.65,
      factors: ["Contratos", "Cartão Ponto", "Atestados"] 
    },
  ];

  const recentAnalyses = [
    "Análise de horas extras irregulares",
    "Verificação de adicional noturno",
    "Conformidade com CCT 2024",
    "Auditoria de benefícios",
  ];

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Consultor de Riscos
        </Typography>
        <Typography variant="subtitle1" color="text.secondary">
          IA avançada para identificação e análise de riscos na folha de pagamento.
        </Typography>
      </Box>

      <Grid container spacing={3}>
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Análise Inteligente de Riscos
            </Typography>
            
            <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
              <TextField
                fullWidth
                multiline
                rows={4}
                placeholder="Descreva a situação ou faça uma pergunta sobre riscos trabalhistas..."
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                variant="outlined"
              />
            </Box>

            <Button
              variant="contained"
              startIcon={<Psychology />}
              onClick={handleAnalyze}
              disabled={!query.trim() || isAnalyzing}
              size="large"
            >
              {isAnalyzing ? "Analisando..." : "Analisar Riscos"}
            </Button>

            {isAnalyzing && (
              <Box sx={{ mt: 3, p: 2, bgcolor: "grey.50", borderRadius: 1 }}>
                <Typography variant="body2">
                  🤖 IA processando análise de riscos...
                </Typography>
                <LinearProgress sx={{ mt: 1 }} />
              </Box>
            )}

            {/* Enhanced AI Results with Feedback */}
            {analysisResult && (
              <Paper sx={{ mt: 3, p: 3 }}>
                <Typography variant="h6" gutterBottom>
                  🤖 Recomendações da IA
                </Typography>
                {analysisResult.recommendations.map((rec: any, index: number) => (
                  <Card 
                    key={rec.id} 
                    sx={{ 
                      mb: 2, 
                      opacity: getConfidenceOpacity(rec.confidence),
                      border: `2px solid ${getConfidenceColor(rec.confidence)}`,
                      position: 'relative'
                    }}
                  >
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                        <Box sx={{ flex: 1 }}>
                          <Typography variant="h6" gutterBottom>
                            {rec.title}
                          </Typography>
                          <Typography variant="body2" color="text.secondary" paragraph>
                            {rec.description}
                          </Typography>
                          
                          {/* Confidence Indicator */}
                          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                            <Typography variant="caption" sx={{ mr: 1 }}>
                              Confiança:
                            </Typography>
                            <LinearProgress 
                              variant="determinate" 
                              value={rec.confidence * 100}
                              sx={{ 
                                width: 100, 
                                mr: 1,
                                '& .MuiLinearProgress-bar': {
                                  backgroundColor: getConfidenceColor(rec.confidence)
                                }
                              }}
                            />
                            <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
                              {(rec.confidence * 100).toFixed(0)}%
                            </Typography>
                          </Box>

                          {/* Interactive Risk Factors */}
                          <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                            {rec.factors.map((factor: string, factorIndex: number) => (
                              <Chip
                                key={factorIndex}
                                label={factor}
                                size="small"
                                clickable
                                onClick={() => handleDrillDown(factor)}
                                icon={<ExpandMore />}
                                sx={{ 
                                  cursor: 'pointer',
                                  '&:hover': { 
                                    backgroundColor: 'primary.light',
                                    color: 'white'
                                  }
                                }}
                              />
                            ))}
                          </Box>
                        </Box>

                        {/* Feedback Mechanism */}
                        <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', ml: 2 }}>
                          <Typography variant="caption" sx={{ mb: 1 }}>
                            Esta recomendação foi útil?
                          </Typography>
                          <Box sx={{ display: 'flex', gap: 1 }}>
                            <Tooltip title="Recomendação útil">
                              <IconButton
                                size="small"
                                color={feedback[rec.id] === 'positive' ? 'success' : 'default'}
                                onClick={() => handleFeedback(rec.id, 'positive')}
                              >
                                <ThumbUp />
                              </IconButton>
                            </Tooltip>
                            <Tooltip title="Recomendação não útil">
                              <IconButton
                                size="small"
                                color={feedback[rec.id] === 'negative' ? 'error' : 'default'}
                                onClick={() => handleFeedback(rec.id, 'negative')}
                              >
                                <ThumbDown />
                              </IconButton>
                            </Tooltip>
                          </Box>
                          {feedback[rec.id] && (
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

          <Paper sx={{ p: 3, mt: 3 }}>
            <Typography variant="h6" gutterBottom>
              Análises Recentes
            </Typography>
            <List>
              {recentAnalyses.map((analysis, index) => (
                <React.Fragment key={index}>
                  <ListItem>
                    <ListItemText 
                      primary={analysis}
                      secondary={`${new Date().toLocaleDateString()} - Análise completa`}
                    />
                    <Button size="small" startIcon={<History />}>
                      Ver Detalhes
                    </Button>
                  </ListItem>
                  {index < recentAnalyses.length - 1 && <Divider />}
                </React.Fragment>
              ))}
            </List>
          </Paper>
        </Grid>

        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Categorias de Risco
            </Typography>
            
            {riskCategories.map((category, index) => (
              <Card 
                key={index} 
                sx={{ 
                  mb: 2,
                  opacity: getConfidenceOpacity(category.confidence),
                  border: `1px solid ${getConfidenceColor(category.confidence)}`
                }}
              >
                <CardContent sx={{ p: 2, "&:last-child": { pb: 2 } }}>
                  <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 1 }}>
                    <Typography variant="subtitle2">
                      {category.name}
                    </Typography>
                    <Chip 
                      label={category.level}
                      color={category.color as any}
                      size="small"
                    />
                  </Box>
                  <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
                    {category.count} itens identificados
                  </Typography>
                  
                  {/* Confidence Indicator */}
                  <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                    <Typography variant="caption" sx={{ mr: 1 }}>
                      Confiança:
                    </Typography>
                    <LinearProgress 
                      variant="determinate" 
                      value={category.confidence * 100}
                      sx={{ 
                        width: 60, 
                        mr: 1,
                        '& .MuiLinearProgress-bar': {
                          backgroundColor: getConfidenceColor(category.confidence)
                        }
                      }}
                    />
                    <Typography variant="caption" sx={{ fontWeight: 'bold' }}>
                      {(category.confidence * 100).toFixed(0)}%
                    </Typography>
                  </Box>

                  <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                    {category.level === "Alto" && <Warning color="error" fontSize="small" />}
                    {category.level === "Médio" && <TrendingUp color="warning" fontSize="small" />}
                    {category.level === "Baixo" && <CheckCircle color="success" fontSize="small" />}
                    <Typography variant="caption" sx={{ ml: 1 }}>
                      Prioridade {category.level.toLowerCase()}
                    </Typography>
                  </Box>

                  {/* Interactive Risk Factors */}
                  <Box sx={{ display: 'flex', gap: 0.5, flexWrap: 'wrap' }}>
                    {category.factors.slice(0, 2).map((factor: string, factorIndex: number) => (
                      <Chip
                        key={factorIndex}
                        label={factor}
                        size="small"
                        variant="outlined"
                        clickable
                        onClick={() => handleDrillDown(factor)}
                        sx={{ 
                          fontSize: '0.7rem',
                          height: '20px',
                          cursor: 'pointer',
                          '&:hover': { 
                            backgroundColor: 'primary.light',
                            color: 'white'
                          }
                        }}
                      />
                    ))}
                    {category.factors.length > 2 && (
                      <Chip
                        label={`+${category.factors.length - 2}`}
                        size="small"
                        variant="outlined"
                        sx={{ fontSize: '0.7rem', height: '20px' }}
                      />
                    )}
                  </Box>
                </CardContent>
              </Card>
            ))}
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