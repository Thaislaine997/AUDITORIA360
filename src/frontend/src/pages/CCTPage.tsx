/**
 * 📋 CCTPage - Módulo de Gestão de Legislação e CCTs
 * 
 * A "Biblioteca Digital" inteligente para CCTs que implementa:
 * - Listagem pesquisável com filtros poderosos
 * - Status dinâmico: Ativo, Expirado, Expirando em breve
 * - Cadastro manual e assistido por IA (upload de PDF)
 * - Gestão centralizada do conhecimento de CCTs
 */

import React, { useState, useEffect } from "react";
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
  Alert,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  Fab,
  Badge,
  Divider,
  Stack,
  LinearProgress
} from "@mui/material";
import {
  Search,
  Add,
  FilterList,
  CheckCircle,
  Warning,
  Error,
  Info,
  UploadFile,
  Save,
  Refresh,
  Business,
  DateRange,
  Description,
  CloudUpload,
  AutoFixHigh,
  Visibility
} from "@mui/icons-material";

interface Sindicato {
  id: number;
  nome_sindicato: string;
  cnpj?: string;
  base_territorial?: string;
  categoria_representada?: string;
  criado_em: string;
}

interface CCT {
  id: number;
  sindicato_id: number;
  numero_registro_mte?: string;
  vigencia_inicio: string;
  vigencia_fim: string;
  link_documento_oficial?: string;
  dados_cct?: any;
  criado_em: string;
  atualizado_em: string;
}

interface CCTListResponse {
  ccts: CCT[];
  total: number;
  ativas: number;
  expiradas: number;
  expirando_30_dias: number;
}

const CCTPage: React.FC = () => {
  const [ccts, setCcts] = useState<CCT[]>([]);
  const [sindicatos, setSindicatos] = useState<Sindicato[]>([]);
  const [stats, setStats] = useState<CCTListResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [searchTerm, setSearchTerm] = useState("");
  const [selectedSindicato, setSelectedSindicato] = useState<number | "">("");
  const [filterVigencia, setFilterVigencia] = useState<string>("todas");
  
  // Dialog states
  const [showNewCCTDialog, setShowNewCCTDialog] = useState(false);
  const [showUploadDialog, setShowUploadDialog] = useState(false);
  const [selectedCCT, setSelectedCCT] = useState<CCT | null>(null);
  
  // Form states
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [processingAI, setProcessingAI] = useState(false);
  const [aiResults, setAIResults] = useState<any>(null);

  // Load initial data
  useEffect(() => {
    carregarDados();
  }, []);

  // Apply filters when they change
  useEffect(() => {
    carregarCCTs();
  }, [searchTerm, selectedSindicato, filterVigencia]);

  const carregarDados = async () => {
    setLoading(true);
    try {
      // Load syndicates
      const sindicatosResponse = await fetch('/api/v1/sindicatos');
      const sindicatosData = await sindicatosResponse.json();
      setSindicatos(sindicatosData);

      // Load CCTs
      await carregarCCTs();
    } catch (error) {
      console.error('Erro ao carregar dados:', error);
    } finally {
      setLoading(false);
    }
  };

  const carregarCCTs = async () => {
    try {
      let url = '/api/v1/cct?';
      const params = new URLSearchParams();
      
      if (selectedSindicato) params.append('sindicato_id', selectedSindicato.toString());
      if (searchTerm) params.append('search_text', searchTerm);
      if (filterVigencia !== 'todas') {
        params.append('vigente', filterVigencia === 'ativas' ? 'true' : 'false');
      }
      
      const response = await fetch(`${url}${params}`);
      const data: CCTListResponse = await response.json();
      
      setCcts(data.ccts);
      setStats(data);
    } catch (error) {
      console.error('Erro ao carregar CCTs:', error);
    }
  };

  const handleUploadPDF = async () => {
    if (!uploadFile) return;
    
    setProcessingAI(true);
    try {
      const formData = new FormData();
      formData.append('arquivo_pdf', uploadFile);
      
      const response = await fetch('/api/v1/legislacao/extrair-pdf', {
        method: 'POST',
        body: formData,
      });
      
      const result = await response.json();
      setAIResults(result);
      
      // Refresh data after processing
      await carregarDados();
    } catch (error) {
      console.error('Erro no processamento do PDF:', error);
    } finally {
      setProcessingAI(false);
    }
  };

  const getStatusChip = (cct: CCT) => {
    const hoje = new Date();
    const inicio = new Date(cct.vigencia_inicio);
    const fim = new Date(cct.vigencia_fim);
    const treintaDias = new Date();
    treintaDias.setDate(hoje.getDate() + 30);
    
    if (fim < hoje) {
      return <Chip label="Expirado" color="error" size="small" icon={<Error />} />;
    } else if (fim <= treintaDias) {
      return <Chip label="Expirando em Breve" color="warning" size="small" icon={<Warning />} />;
    } else if (inicio <= hoje && fim >= hoje) {
      return <Chip label="Ativo" color="success" size="small" icon={<CheckCircle />} />;
    } else {
      return <Chip label="Futuro" color="info" size="small" icon={<Info />} />;
    }
  };

  const getSindicatoNome = (sindicato_id: number) => {
    const sindicato = sindicatos.find(s => s.id === sindicato_id);
    return sindicato?.nome_sindicato || 'Sindicato não encontrado';
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header with Statistics */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          📋 CCT - Convenções Coletivas de Trabalho
          <Chip 
            label="Biblioteca Digital Inteligente" 
            color="primary" 
            size="small"
            icon={<AutoFixHigh />}
          />
        </Typography>
        
        {stats && (
          <Grid container spacing={2} sx={{ mb: 3 }}>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center', py: 2 }}>
                  <Typography variant="h3" color="primary.main">{stats.total}</Typography>
                  <Typography variant="body2" color="text.secondary">Total de CCTs</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center', py: 2 }}>
                  <Typography variant="h3" color="success.main">{stats.ativas}</Typography>
                  <Typography variant="body2" color="text.secondary">Ativas</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center', py: 2 }}>
                  <Typography variant="h3" color="warning.main">{stats.expirando_30_dias}</Typography>
                  <Typography variant="body2" color="text.secondary">Expirando em 30 dias</Typography>
                </CardContent>
              </Card>
            </Grid>
            <Grid item xs={12} sm={6} md={3}>
              <Card>
                <CardContent sx={{ textAlign: 'center', py: 2 }}>
                  <Typography variant="h3" color="error.main">{stats.expiradas}</Typography>
                  <Typography variant="body2" color="text.secondary">Expiradas</Typography>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        )}
      </Box>

      <Grid container spacing={3}>
        {/* Filter and Search Panel */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, sticky: true, top: 20 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <FilterList /> Filtros Poderosos
            </Typography>
            
            <Stack spacing={3}>
              {/* Search */}
              <TextField
                fullWidth
                label="Busca Inteligente"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Nome do sindicato, registro MTE..."
                InputProps={{
                  startAdornment: <Search sx={{ mr: 1, color: 'action.active' }} />,
                }}
              />

              {/* Syndicate Filter */}
              <FormControl fullWidth>
                <InputLabel>Filtrar por Sindicato</InputLabel>
                <Select
                  value={selectedSindicato}
                  label="Filtrar por Sindicato"
                  onChange={(e) => setSelectedSindicato(e.target.value as number)}
                >
                  <MenuItem value="">Todos os Sindicatos</MenuItem>
                  {sindicatos.map((sindicato) => (
                    <MenuItem key={sindicato.id} value={sindicato.id}>
                      {sindicato.nome_sindicato}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Validity Filter */}
              <FormControl fullWidth>
                <InputLabel>Filtrar por Vigência</InputLabel>
                <Select
                  value={filterVigencia}
                  label="Filtrar por Vigência"
                  onChange={(e) => setFilterVigencia(e.target.value)}
                >
                  <MenuItem value="todas">Todas as CCTs</MenuItem>
                  <MenuItem value="ativas">Apenas Ativas</MenuItem>
                  <MenuItem value="expiradas">Apenas Expiradas</MenuItem>
                </Select>
              </FormControl>

              <Divider />

              {/* Action Buttons */}
              <Stack spacing={2}>
                <Button
                  variant="contained"
                  startIcon={<Add />}
                  onClick={() => setShowNewCCTDialog(true)}
                  fullWidth
                >
                  Cadastrar Nova CCT
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<CloudUpload />}
                  onClick={() => setShowUploadDialog(true)}
                  fullWidth
                  color="secondary"
                >
                  Upload com IA
                </Button>
                
                <Button
                  variant="text"
                  startIcon={<Refresh />}
                  onClick={carregarDados}
                  fullWidth
                  disabled={loading}
                >
                  Atualizar Dados
                </Button>
              </Stack>
            </Stack>
          </Paper>
        </Grid>

        {/* CCT List */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              📋 Resultados ({stats?.total || 0} CCTs encontradas)
            </Typography>
            
            {loading && <LinearProgress sx={{ mb: 2 }} />}
            
            {ccts.length === 0 && !loading ? (
              <Alert severity="info" sx={{ my: 3 }}>
                <Typography variant="subtitle1">Nenhuma CCT encontrada</Typography>
                <Typography variant="body2">
                  Comece cadastrando um novo sindicato e sua CCT, ou faça upload de um PDF para análise automática.
                </Typography>
              </Alert>
            ) : (
              <Grid container spacing={2}>
                {ccts.map((cct) => (
                  <Grid item xs={12} key={cct.id}>
                    <Card 
                      sx={{ 
                        cursor: 'pointer',
                        transition: 'all 0.2s',
                        '&:hover': { 
                          boxShadow: 3,
                          transform: 'translateY(-2px)'
                        },
                      }}
                      onClick={() => setSelectedCCT(cct)}
                    >
                      <CardContent>
                        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                          <Box sx={{ flexGrow: 1 }}>
                            <Typography variant="h6" color="primary" gutterBottom>
                              {getSindicatoNome(cct.sindicato_id)}
                            </Typography>
                            <Typography variant="body2" color="text.secondary">
                              <Business fontSize="small" sx={{ mr: 1, verticalAlign: 'middle' }} />
                              Registro MTE: {cct.numero_registro_mte || 'Não informado'}
                            </Typography>
                          </Box>
                          {getStatusChip(cct)}
                        </Box>
                        
                        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 1 }}>
                          <DateRange fontSize="small" color="action" />
                          <Typography variant="body2">
                            Vigência: {new Date(cct.vigencia_inicio).toLocaleDateString()} até {new Date(cct.vigencia_fim).toLocaleDateString()}
                          </Typography>
                        </Box>
                        
                        {cct.dados_cct && (
                          <Box sx={{ mt: 2 }}>
                            <Typography variant="caption" color="text.secondary">
                              📊 Dados estruturados disponíveis • Processado pela IA
                            </Typography>
                          </Box>
                        )}
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Upload Dialog */}
      <Dialog 
        open={showUploadDialog} 
        onClose={() => setShowUploadDialog(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          🤖 Cadastro Assistido por IA
        </DialogTitle>
        <DialogContent>
          <Typography variant="body1" sx={{ mb: 3 }}>
            Arraste o PDF da CCT ou da Lei para que nossa IA extraia os dados automaticamente.
          </Typography>
          
          <Box
            sx={{
              border: '2px dashed',
              borderColor: uploadFile ? 'primary.main' : 'grey.300',
              borderRadius: 2,
              p: 4,
              textAlign: 'center',
              cursor: 'pointer',
              transition: 'all 0.2s',
              '&:hover': {
                borderColor: 'primary.main',
                backgroundColor: 'action.hover'
              }
            }}
            onClick={() => document.getElementById('file-upload')?.click()}
          >
            <input
              id="file-upload"
              type="file"
              accept=".pdf"
              hidden
              onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
            />
            <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {uploadFile ? `✓ ${uploadFile.name}` : 'Clique ou arraste um PDF aqui'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              Formatos aceitos: PDF (máximo 50MB)
            </Typography>
          </Box>

          {processingAI && (
            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <CircularProgress />
              <Typography variant="body2" sx={{ mt: 2 }}>
                🧠 Processando com IA... Analisando documento e extraindo dados estruturados
              </Typography>
            </Box>
          )}

          {aiResults && (
            <Alert severity="success" sx={{ mt: 3 }}>
              <Typography variant="subtitle1">✓ Processamento Concluído!</Typography>
              <Typography variant="body2">
                Documento processado com {(aiResults.confidence_score * 100).toFixed(1)}% de confiança.
                Os dados extraídos estão prontos para validação.
              </Typography>
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowUploadDialog(false)}>
            Cancelar
          </Button>
          <Button 
            variant="contained" 
            onClick={handleUploadPDF}
            disabled={!uploadFile || processingAI}
            startIcon={processingAI ? <CircularProgress size={20} /> : <AutoFixHigh />}
          >
            {processingAI ? 'Processando...' : 'Processar com IA'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* CCT Details Dialog */}
      {selectedCCT && (
        <Dialog 
          open={Boolean(selectedCCT)} 
          onClose={() => setSelectedCCT(null)}
          maxWidth="lg"
          fullWidth
        >
          <DialogTitle>
            📋 Detalhes da CCT - {getSindicatoNome(selectedCCT.sindicato_id)}
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" gutterBottom>Informações Básicas:</Typography>
                <List dense>
                  <ListItem>
                    <ListItemIcon><Business /></ListItemIcon>
                    <ListItemText 
                      primary="Sindicato" 
                      secondary={getSindicatoNome(selectedCCT.sindicato_id)}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon><Description /></ListItemIcon>
                    <ListItemText 
                      primary="Registro MTE" 
                      secondary={selectedCCT.numero_registro_mte || 'Não informado'}
                    />
                  </ListItem>
                  <ListItem>
                    <ListItemIcon><DateRange /></ListItemIcon>
                    <ListItemText 
                      primary="Vigência" 
                      secondary={`${new Date(selectedCCT.vigencia_inicio).toLocaleDateString()} - ${new Date(selectedCCT.vigencia_fim).toLocaleDateString()}`}
                    />
                  </ListItem>
                </List>
              </Grid>
              
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" gutterBottom>Status:</Typography>
                <Box sx={{ mb: 2 }}>{getStatusChip(selectedCCT)}</Box>
                
                {selectedCCT.dados_cct && (
                  <>
                    <Typography variant="subtitle2" gutterBottom>Dados Estruturados (IA):</Typography>
                    <Box sx={{ backgroundColor: 'grey.50', p: 2, borderRadius: 1 }}>
                      <Typography variant="caption" component="pre" sx={{ fontSize: '0.75rem' }}>
                        {JSON.stringify(selectedCCT.dados_cct, null, 2)}
                      </Typography>
                    </Box>
                  </>
                )}
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSelectedCCT(null)}>Fechar</Button>
            {selectedCCT.link_documento_oficial && (
              <Button 
                variant="contained" 
                startIcon={<Visibility />}
                href={selectedCCT.link_documento_oficial}
                target="_blank"
              >
                Ver Documento Oficial
              </Button>
            )}
          </DialogActions>
        </Dialog>
      )}
    </Container>
  );
};

export default CCTPage;
