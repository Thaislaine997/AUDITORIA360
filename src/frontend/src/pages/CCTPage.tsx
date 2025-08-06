/**
 * 🔮 CCTPage - Assistente Contextual Telepático
 * Página com assistência precognitiva para códigos CCT
 */

import React, { useState, useEffect, useRef } from "react";
import { 
  Container, 
  Typography, 
  Paper, 
  Box,
  Card,
  CardContent,
  TextField,
  Grid,
  Chip,
  Button,
  IconButton,
  Collapse,
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Tooltip,
  Fade
} from "@mui/material";
import {
  Psychology,
  Lightbulb,
  Code,
  Search,
  Info,
  CheckCircle,
  AutoAwesome,
  KeyboardArrowDown,
  KeyboardArrowUp
} from "@mui/icons-material";

interface CCTData {
  code: string;
  title: string;
  sector: string;
  description: string;
  applicableRegions: string[];
  lastUpdated: string;
  commonFields: string[];
}

interface TelepathicAssistance {
  isActive: boolean;
  suggestedCCT: CCTData | null;
  confidence: number;
  reasoning: string;
  pauseDetected: boolean;
}

const CCTPage: React.FC = () => {
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedCCT, setSelectedCCT] = useState<CCTData | null>(null);
  const [telepathicAssistance, setTelepathicAssistance] = useState<TelepathicAssistance>({
    isActive: false,
    suggestedCCT: null,
    confidence: 0,
    reasoning: "",
    pauseDetected: false
  });
  const [showAdvancedInfo, setShowAdvancedInfo] = useState(false);
  
  const searchTimeoutRef = useRef<NodeJS.Timeout | null>(null);
  const pauseStartTime = useRef<number | null>(null);

  // 🧠 CCT Database (simplified for demo)
  const cctDatabase: CCTData[] = [
    {
      code: "CCT-001",
      title: "Contrato Coletivo de Trabalho - Setor Público",
      sector: "Administração Pública",
      description: "CCT aplicável aos funcionários da administração pública central e local",
      applicableRegions: ["Lisboa", "Porto", "Nacional"],
      lastUpdated: "2024-01-15",
      commonFields: ["Escalão", "Subsídio de refeição", "Horário flexível", "Licenças especiais"]
    },
    {
      code: "CCT-002", 
      title: "Contrato Coletivo de Trabalho - Setor Privado",
      sector: "Setor Privado Geral",
      description: "CCT para empresas do setor privado com regime geral de trabalho",
      applicableRegions: ["Nacional"],
      lastUpdated: "2024-02-10",
      commonFields: ["Salário base", "Subsídio de Natal", "Férias", "Horas extraordinárias"]
    },
    {
      code: "CCT-003",
      title: "Contrato Coletivo de Trabalho - Setor da Saúde", 
      sector: "Saúde",
      description: "CCT específico para profissionais de saúde e instituições hospitalares",
      applicableRegions: ["Nacional"],
      lastUpdated: "2024-01-30",
      commonFields: ["Turnos", "Risco profissional", "Formação contínua", "Especialização"]
    },
    {
      code: "CCT-004",
      title: "Contrato Coletivo de Trabalho - Setor da Educação",
      sector: "Educação",
      description: "CCT para docentes e não docentes do sistema educativo",
      applicableRegions: ["Nacional"],
      lastUpdated: "2024-02-05",
      commonFields: ["Escalão docente", "Componente letiva", "Férias escolares", "Formação"]
    },
    {
      code: "CCT-005",
      title: "Contrato Coletivo de Trabalho - Setor Bancário",
      sector: "Banca e Seguros",
      description: "CCT aplicável a trabalhadores do setor bancário e segurador",
      applicableRegions: ["Nacional"],
      lastUpdated: "2024-01-20",
      commonFields: ["Comissões", "Objetivos", "Responsabilidade civil", "Sigilo bancário"]
    }
  ];

  // 🔮 Telepathic search behavior analysis
  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    const value = event.target.value;
    setSearchTerm(value);
    
    // Clear existing timeout
    if (searchTimeoutRef.current) {
      clearTimeout(searchTimeoutRef.current);
    }
    
    // Start pause detection
    pauseStartTime.current = Date.now();
    
    // Set timeout to detect search pause (1.5 seconds)
    searchTimeoutRef.current = setTimeout(() => {
      if (value.length > 0) {
        activateTelepathicAssistance(value);
      }
    }, 1500);
  };

  // 🧠 Activate telepathic assistance based on search behavior
  const activateTelepathicAssistance = (searchValue: string) => {
    const pauseDuration = pauseStartTime.current ? Date.now() - pauseStartTime.current : 0;
    
    if (pauseDuration >= 1500) { // User paused for 1.5+ seconds
      // Analyze search intent
      const suggestedCCT = findBestMatch(searchValue);
      const confidence = calculateConfidence(searchValue, suggestedCCT);
      const reasoning = generateReasoning(searchValue, suggestedCCT);
      
      setTelepathicAssistance({
        isActive: true,
        suggestedCCT,
        confidence,
        reasoning,
        pauseDetected: true
      });
    }
  };

  // 🎯 Find best CCT match based on search intent
  const findBestMatch = (searchValue: string): CCTData | null => {
    const search = searchValue.toLowerCase();
    
    // Exact code match
    const exactMatch = cctDatabase.find(cct => 
      cct.code.toLowerCase().includes(search)
    );
    if (exactMatch) return exactMatch;
    
    // Sector-based matching
    const sectorKeywords = {
      'público': 'CCT-001',
      'privado': 'CCT-002', 
      'saúde': 'CCT-003',
      'hospital': 'CCT-003',
      'educação': 'CCT-004',
      'escola': 'CCT-004',
      'docente': 'CCT-004',
      'banco': 'CCT-005',
      'banca': 'CCT-005',
      'seguro': 'CCT-005'
    };
    
    for (const [keyword, code] of Object.entries(sectorKeywords)) {
      if (search.includes(keyword)) {
        return cctDatabase.find(cct => cct.code === code) || null;
      }
    }
    
    // Default to most common (private sector)
    return cctDatabase.find(cct => cct.code === 'CCT-002') || null;
  };

  // 📊 Calculate confidence in suggestion
  const calculateConfidence = (searchValue: string, suggestedCCT: CCTData | null): number => {
    if (!suggestedCCT) return 0;
    
    const search = searchValue.toLowerCase();
    
    // Exact code match = 100% confidence
    if (suggestedCCT.code.toLowerCase().includes(search)) return 1.0;
    
    // Sector keyword match = 80% confidence
    if (suggestedCCT.sector.toLowerCase().includes(search) || 
        suggestedCCT.title.toLowerCase().includes(search)) return 0.8;
    
    // Partial match = 60% confidence
    return 0.6;
  };

  // 💡 Generate reasoning for the suggestion
  const generateReasoning = (searchValue: string, suggestedCCT: CCTData | null): string => {
    if (!suggestedCCT) return "Nenhuma correspondência encontrada";
    
    const search = searchValue.toLowerCase();
    
    if (suggestedCCT.code.toLowerCase().includes(search)) {
      return `Correspondência exata com código ${suggestedCCT.code}`;
    }
    
    if (search.includes('público')) {
      return "Detectado interesse no setor público - CCT mais relevante sugerido";
    }
    
    if (search.includes('saúde') || search.includes('hospital')) {
      return "Área da saúde identificada - CCT específico para profissionais de saúde";
    }
    
    if (search.includes('educação') || search.includes('escola') || search.includes('docente')) {
      return "Setor educativo detectado - CCT para pessoal docente e não docente";
    }
    
    if (search.includes('banco') || search.includes('banca')) {
      return "Setor bancário identificado - CCT específico para banca e seguros";
    }
    
    return `Sugestão baseada em análise semântica de "${searchValue}"`;
  };

  // 🎊 Apply suggested CCT
  const applySuggestion = (cct: CCTData) => {
    setSelectedCCT(cct);
    setSearchTerm(cct.code);
    setTelepathicAssistance({
      isActive: false,
      suggestedCCT: null,
      confidence: 0,
      reasoning: "",
      pauseDetected: false
    });
  };

  // Filter CCTs based on search
  const filteredCCTs = cctDatabase.filter(cct =>
    cct.code.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cct.title.toLowerCase().includes(searchTerm.toLowerCase()) ||
    cct.sector.toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      {/* Header with Telepathic Status */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          📋 CCT - Convenção Coletiva de Trabalho
          {telepathicAssistance.isActive && (
            <Chip 
              icon={<Psychology />} 
              label="Assistência Telepática Ativa" 
              color="primary" 
              size="small"
            />
          )}
        </Typography>
        <Typography variant="body1" color="text.secondary">
          Sistema inteligente de pesquisa e gestão de CCT com assistência precognitiva
        </Typography>
      </Box>

      {/* Telepathic Assistance Alert */}
      <Collapse in={telepathicAssistance.isActive}>
        <Alert 
          severity="info" 
          icon={<AutoAwesome />}
          sx={{ mb: 3 }}
          action={
            telepathicAssistance.suggestedCCT && (
              <Button 
                color="inherit" 
                size="small"
                onClick={() => applySuggestion(telepathicAssistance.suggestedCCT!)}
              >
                Aplicar Sugestão
              </Button>
            )
          }
        >
          <Typography variant="subtitle2" gutterBottom>
            🔮 Assistência Telepática Detectada
          </Typography>
          <Typography variant="body2">
            <strong>Pausa detectada:</strong> {telepathicAssistance.reasoning}
          </Typography>
          {telepathicAssistance.suggestedCCT && (
            <Typography variant="body2" sx={{ mt: 1 }}>
              <strong>Sugestão:</strong> {telepathicAssistance.suggestedCCT.code} - {telepathicAssistance.suggestedCCT.title}
              <br />
              <strong>Confiança:</strong> {(telepathicAssistance.confidence * 100).toFixed(0)}%
            </Typography>
          )}
        </Alert>
      </Collapse>

      <Grid container spacing={3}>
        {/* Search and Filter Section */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Search /> Pesquisa Inteligente
            </Typography>
            
            <TextField
              fullWidth
              label="Código CCT ou Setor"
              value={searchTerm}
              onChange={handleSearchChange}
              placeholder="Ex: CCT-001, público, saúde..."
              sx={{ mb: 2 }}
            />
            
            <Box sx={{ mb: 2 }}>
              <Button
                variant="outlined"
                size="small"
                onClick={() => setShowAdvancedInfo(!showAdvancedInfo)}
                endIcon={showAdvancedInfo ? <KeyboardArrowUp /> : <KeyboardArrowDown />}
              >
                Informações Avançadas
              </Button>
            </Box>
            
            <Collapse in={showAdvancedInfo}>
              <Alert severity="info" sx={{ mb: 2 }}>
                <Typography variant="subtitle2" gutterBottom>
                  💡 Dicas da Interface Telepática:
                </Typography>
                <List dense>
                  <ListItem sx={{ px: 0 }}>
                    <ListItemIcon sx={{ minWidth: 30 }}>
                      <Lightbulb fontSize="small" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Digite e pause para ativar sugestões"
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                  <ListItem sx={{ px: 0 }}>
                    <ListItemIcon sx={{ minWidth: 30 }}>
                      <Code fontSize="small" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Códigos diretos: CCT-001, CCT-002..."
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                  <ListItem sx={{ px: 0 }}>
                    <ListItemIcon sx={{ minWidth: 30 }}>
                      <Info fontSize="small" />
                    </ListItemIcon>
                    <ListItemText 
                      primary="Setores: público, privado, saúde, educação"
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                </List>
              </Alert>
            </Collapse>
            
            {/* Quick Sector Filters */}
            <Typography variant="subtitle2" gutterBottom>
              Filtros Rápidos:
            </Typography>
            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 1 }}>
              {['Público', 'Privado', 'Saúde', 'Educação', 'Bancário'].map((sector) => (
                <Chip
                  key={sector}
                  label={sector}
                  size="small"
                  onClick={() => setSearchTerm(sector.toLowerCase())}
                  sx={{ cursor: 'pointer' }}
                />
              ))}
            </Box>
          </Paper>
        </Grid>

        {/* CCT Results */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              📋 Resultados ({filteredCCTs.length} encontrados)
            </Typography>
            
            <Grid container spacing={2}>
              {filteredCCTs.map((cct) => (
                <Grid item xs={12} key={cct.code}>
                  <Card 
                    sx={{ 
                      cursor: 'pointer',
                      transition: 'all 0.2s',
                      '&:hover': { 
                        boxShadow: 3,
                        transform: 'translateY(-2px)'
                      },
                      border: selectedCCT?.code === cct.code ? 2 : 1,
                      borderColor: selectedCCT?.code === cct.code ? 'primary.main' : 'divider'
                    }}
                    onClick={() => setSelectedCCT(cct)}
                  >
                    <CardContent>
                      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 1 }}>
                        <Typography variant="h6" color="primary">
                          {cct.code}
                        </Typography>
                        <Chip 
                          label={cct.sector} 
                          size="small" 
                          color="secondary"
                        />
                      </Box>
                      
                      <Typography variant="subtitle1" gutterBottom>
                        {cct.title}
                      </Typography>
                      
                      <Typography variant="body2" color="text.secondary" paragraph>
                        {cct.description}
                      </Typography>
                      
                      <Box sx={{ display: 'flex', gap: 1, flexWrap: 'wrap' }}>
                        {cct.commonFields.slice(0, 3).map((field) => (
                          <Chip 
                            key={field}
                            label={field}
                            size="small"
                            variant="outlined"
                          />
                        ))}
                        {cct.commonFields.length > 3 && (
                          <Chip 
                            label={`+${cct.commonFields.length - 3} mais`}
                            size="small"
                            variant="outlined"
                            color="primary"
                          />
                        )}
                      </Box>
                    </CardContent>
                  </Card>
                </Grid>
              ))}
            </Grid>
          </Paper>
        </Grid>

        {/* Selected CCT Details */}
        {selectedCCT && (
          <Grid item xs={12}>
            <Fade in>
              <Paper sx={{ p: 3 }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
                  <CheckCircle color="success" />
                  <Typography variant="h5">
                    Detalhes do CCT Selecionado
                  </Typography>
                </Box>
                
                <Grid container spacing={3}>
                  <Grid item xs={12} md={6}>
                    <Typography variant="h6" gutterBottom>
                      {selectedCCT.code} - {selectedCCT.title}
                    </Typography>
                    <Typography variant="body1" paragraph>
                      {selectedCCT.description}
                    </Typography>
                    
                    <Typography variant="subtitle2" gutterBottom>
                      Regiões Aplicáveis:
                    </Typography>
                    <Box sx={{ display: 'flex', gap: 1, mb: 2 }}>
                      {selectedCCT.applicableRegions.map((region) => (
                        <Chip key={region} label={region} size="small" />
                      ))}
                    </Box>
                    
                    <Typography variant="caption" color="text.secondary">
                      Última atualização: {new Date(selectedCCT.lastUpdated).toLocaleDateString('pt-PT')}
                    </Typography>
                  </Grid>
                  
                  <Grid item xs={12} md={6}>
                    <Typography variant="subtitle2" gutterBottom>
                      Campos Comuns no Processamento:
                    </Typography>
                    <List dense>
                      {selectedCCT.commonFields.map((field) => (
                        <ListItem key={field}>
                          <ListItemIcon>
                            <CheckCircle color="success" fontSize="small" />
                          </ListItemIcon>
                          <ListItemText primary={field} />
                        </ListItem>
                      ))}
                    </List>
                  </Grid>
                </Grid>
                
                <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                  <Button variant="contained" startIcon={<PlayArrow />}>
                    Aplicar este CCT
                  </Button>
                  <Button variant="outlined">
                    Ver Detalhes Completos
                  </Button>
                </Box>
              </Paper>
            </Fade>
          </Grid>
        )}
      </Grid>
    </Container>
  );
};

export default CCTPage;
