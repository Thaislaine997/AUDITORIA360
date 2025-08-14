/**
 * GestaoLegislacaoPage - Sistema Central de Gestão de Legislação
 * 
 * Implementa o "Repositório Central" inteligente para todas as regras de negócio:
 * - Upload e processamento de PDFs com IA
 * - Listagem e busca avançada de documentos
 * - Integração com o módulo de CCTs
 * - Base de conhecimento ativa que alimenta toda a plataforma
 */

import React, { useState, useEffect } from 'react';
import { 
  Container, 
  Typography, 
  Box, 
  Card, 
  CardContent, 
  Alert,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  CircularProgress,
  LinearProgress,
  Stack,
  IconButton,
  Tooltip,
  Divider
} from '@mui/material';
import {
  CloudUpload,
  Search,
  FilterList,
  Add,
  Visibility,
  AutoAwesome,
  CheckCircle,
  Error,
  Info,
  Refresh,
} from '@mui/icons-material';
import SaveIcon from '@mui/icons-material/Save';

interface LegislacaoDocumento {
  id: number;
  titulo: string;
  tipo_documento: string;
  numero_documento?: string;
  data_publicacao?: string;
  orgao_emissor?: string;
  arquivo_pdf?: string;
  dados_extraidos?: any;
  status_processamento: string;
  criado_em: string;
  processado_em?: string;
}

interface ExtrairPDFResponse {
  documento_id: number;
  dados_extraidos: any;
  confidence_score: number;
  processamento_tempo_segundos: number;
  sugestoes_validacao: string[];
}

const tiposDocumento = [
  { value: 'lei', label: 'Lei' },
  { value: 'decreto', label: 'Decreto' },
  { value: 'cct', label: 'Convenção Coletiva (CCT)' },
  { value: 'medida_provisoria', label: 'Medida Provisória' },
  { value: 'portaria', label: 'Portaria' },
];

const statusProcessamento = [
  { value: 'pendente', label: 'Pendente', color: 'default' as const },
  { value: 'processando', label: 'Processando', color: 'warning' as const },
  { value: 'concluido', label: 'Concluído', color: 'success' as const },
];

const GestaoLegislacaoPage: React.FC = () => {
  const [documentos, setDocumentos] = useState<LegislacaoDocumento[]>([]);
  const [loading, setLoading] = useState(false);
  const [uploadDialogOpen, setUploadDialogOpen] = useState(false);
  const [manualDialogOpen, setManualDialogOpen] = useState(false);
  const [selectedDocument, setSelectedDocument] = useState<LegislacaoDocumento | null>(null);
  
  // Filters
  const [searchTerm, setSearchTerm] = useState('');
  const [filterTipo, setFilterTipo] = useState<string>('');
  const [filterStatus, setFilterStatus] = useState<string>('');
  
  // Upload state
  const [uploadFile, setUploadFile] = useState<File | null>(null);
  const [processing, setProcessing] = useState(false);
  const [aiResults, setAIResults] = useState<ExtrairPDFResponse | null>(null);
  
  // Manual form state
  const [manualForm, setManualForm] = useState({
    titulo: '',
    tipo_documento: 'lei',
    numero_documento: '',
    data_publicacao: '',
    orgao_emissor: ''
  });

  useEffect(() => {
    carregarDocumentos();
  }, []);

  useEffect(() => {
    carregarDocumentos();
  }, [searchTerm, filterTipo, filterStatus]);

  const carregarDocumentos = async () => {
    setLoading(true);
    try {
      let url = '/api/v1/legislacao?';
      const params = new URLSearchParams();
      
      if (filterTipo) params.append('tipo_documento', filterTipo);
      if (filterStatus) params.append('status', filterStatus);
      if (searchTerm) params.append('search_text', searchTerm);
      
      const response = await fetch(`${url}${params}`);
      const data = await response.json();
      setDocumentos(data);
    } catch (error) {
      console.error('Erro ao carregar documentos:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleUploadPDF = async () => {
    if (!uploadFile) return;
    
    setProcessing(true);
    try {
      const formData = new FormData();
      formData.append('arquivo_pdf', uploadFile);
      
      const response = await fetch('/api/v1/legislacao/extrair-pdf', {
        method: 'POST',
        body: formData,
      });
      
      const result: ExtrairPDFResponse = await response.json();
      setAIResults(result);
      
      // Refresh documents list
      await carregarDocumentos();
    } catch (error) {
      console.error('Erro no processamento do PDF:', error);
    } finally {
      setProcessing(false);
    }
  };

  const handleManualSubmit = async () => {
    try {
      const response = await fetch('/api/v1/legislacao', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(manualForm),
      });
      
      await response.json();
      
      // Reset form and close dialog
      setManualForm({
        titulo: '',
        tipo_documento: 'lei',
        numero_documento: '',
        data_publicacao: '',
        orgao_emissor: ''
      });
      setManualDialogOpen(false);
      
      // Refresh documents list
      await carregarDocumentos();
    } catch (error) {
      console.error('Erro ao criar documento:', error);
    }
  };

  const getStatusChip = (status: string) => {
    const statusInfo = statusProcessamento.find(s => s.value === status);
    if (!statusInfo) return <Chip label={status} size="small" />;
    
    const icons = {
      pendente: <Info />,
      processando: <CircularProgress size={16} />,
      concluido: <CheckCircle />,
      erro: <Error />
    };
    
    return (
      <Chip 
        label={statusInfo.label} 
        color={statusInfo.color} 
        size="small"
        icon={icons[status as keyof typeof icons]}
      />
    );
  };

  const getTipoDocumentoLabel = (tipo: string) => {
    const tipoInfo = tiposDocumento.find(t => t.value === tipo);
    return tipoInfo?.label || tipo;
  };

  // Função handleUploadSuccess removida pois não é utilizada

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          📚 Gestão de Legislação
          <Chip 
            label="Base de Conhecimento Ativa" 
            color="primary" 
            size="small"
            icon={<AutoAwesome />}
          />
        </Typography>
        
        <Typography variant="body1" color="text.secondary" sx={{ mb: 3 }}>
          Sistema inteligente para transformar arquivos de legislação em conhecimento estruturado que alimenta toda a plataforma AUDITORIA360
        </Typography>
        
        {/* Statistics Cards */}
        <Grid container spacing={2} sx={{ mb: 3 }}>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 2 }}>
                <Typography variant="h3" color="primary.main">{documentos.length}</Typography>
                <Typography variant="body2" color="text.secondary">Total Documentos</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 2 }}>
                <Typography variant="h3" color="success.main">
                  {documentos.filter((d: LegislacaoDocumento) => d.status_processamento === 'concluido').length}
                </Typography>
                <Typography variant="body2" color="text.secondary">Processados</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 2 }}>
                <Typography variant="h3" color="warning.main">
                  {documentos.filter((d: LegislacaoDocumento) => d.status_processamento === 'processando').length}
                </Typography>
                <Typography variant="body2" color="text.secondary">Em Processamento</Typography>
              </CardContent>
            </Card>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Card>
              <CardContent sx={{ textAlign: 'center', py: 2 }}>
                <Typography variant="h3" color="secondary.main">
                  {documentos.filter((d: LegislacaoDocumento) => d.tipo_documento === 'cct').length}
                </Typography>
                <Typography variant="body2" color="text.secondary">CCTs</Typography>
              </CardContent>
            </Card>
          </Grid>
        </Grid>
      </Box>

      <Grid container spacing={3}>
        {/* Filters and Actions Panel */}
        <Grid item xs={12} md={4}>
          <Paper sx={{ p: 3, position: 'sticky', top: 20, zIndex: 1 }}>
            <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <FilterList /> Filtros e Ações
            </Typography>
            
            <Stack spacing={3}>
              {/* Search */}
              <TextField
                fullWidth
                label="Buscar Documentos"
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                placeholder="Título, número, órgão emissor..."
                InputProps={{
                  startAdornment: <Search sx={{ mr: 1, color: 'action.active' }} />,
                }}
              />

              {/* Type Filter */}
              <FormControl fullWidth>
                <InputLabel>Tipo de Documento</InputLabel>
                <Select
                  value={filterTipo}
                  label="Tipo de Documento"
                  onChange={(e) => setFilterTipo(e.target.value)}
                >
                  <MenuItem value="">Todos os Tipos</MenuItem>
                  {tiposDocumento.map((tipo) => (
                    <MenuItem key={tipo.value} value={tipo.value}>
                      {tipo.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              {/* Status Filter */}
              <FormControl fullWidth>
                <InputLabel>Status</InputLabel>
                <Select
                  value={filterStatus}
                  label="Status"
                  onChange={(e) => setFilterStatus(e.target.value)}
                >
                  <MenuItem value="">Todos os Status</MenuItem>
                  {statusProcessamento.map((status) => (
                    <MenuItem key={status.value} value={status.value}>
                      {status.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>

              <Divider />

              {/* Action Buttons */}
              <Stack spacing={2}>
                <Button
                  variant="contained"
                  startIcon={<CloudUpload />}
                  onClick={() => setUploadDialogOpen(true)}
                  fullWidth
                >
                  📤 Upload com IA
                </Button>
                
                <Button
                  variant="outlined"
                  startIcon={<Add />}
                  onClick={() => setManualDialogOpen(true)}
                  fullWidth
                >
                  ✏️ Cadastro Manual
                </Button>
                
                <Button
                  variant="text"
                  startIcon={<Refresh />}
                  onClick={carregarDocumentos}
                  fullWidth
                  disabled={loading}
                >
                  🔄 Atualizar Lista
                </Button>
              </Stack>
            </Stack>
          </Paper>
        </Grid>

        {/* Documents Table */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              📋 Documentos Cadastrados ({documentos.length})
            </Typography>
            
            {loading && <LinearProgress sx={{ mb: 2 }} />}
            
            {documentos.length === 0 && !loading ? (
              <Alert severity="info" sx={{ my: 3 }}>
                <Typography variant="subtitle1">Nenhum documento encontrado</Typography>
                <Typography variant="body2">
                  Comece fazendo upload de um PDF ou cadastrando um documento manualmente.
                </Typography>
              </Alert>
            ) : (
              <TableContainer>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Título</TableCell>
                      <TableCell>Tipo</TableCell>
                      <TableCell>Status</TableCell>
                      <TableCell>Processado</TableCell>
                      <TableCell>Ações</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {documentos.map((documento: LegislacaoDocumento) => (
                      <TableRow key={documento.id}>
                        <TableCell>
                          <Box>
                            <Typography variant="subtitle2">
                              {documento.titulo}
                            </Typography>
                            {documento.numero_documento && (
                              <Typography variant="caption" color="text.secondary">
                                {documento.numero_documento}
                              </Typography>
                            )}
                          </Box>
                        </TableCell>
                        <TableCell>
                          <Chip 
                            label={getTipoDocumentoLabel(documento.tipo_documento)}
                            size="small"
                            variant="outlined"
                          />
                        </TableCell>
                        <TableCell>
                          {getStatusChip(documento.status_processamento)}
                        </TableCell>
                        <TableCell>
                          <Typography variant="body2" color="text.secondary">
                            {documento.processado_em 
                              ? new Date(documento.processado_em).toLocaleDateString()
                              : '-'
                            }
                          </Typography>
                        </TableCell>
                        <TableCell>
                          <Stack direction="row" spacing={1}>
                            <Tooltip title="Ver Detalhes">
                              <IconButton
                                size="small"
                                onClick={() => setSelectedDocument(documento)}
                              >
                                <Visibility />
                              </IconButton>
                            </Tooltip>
                            {documento.dados_extraidos && (
                              <Tooltip title="Dados IA Disponíveis">
                                <IconButton size="small" color="primary">
                                  <AutoAwesome />
                                </IconButton>
                              </Tooltip>
                            )}
                          </Stack>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            )}
          </Paper>
        </Grid>
      </Grid>

      {/* Upload Dialog */}
      <Dialog 
        open={uploadDialogOpen} 
        onClose={() => setUploadDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          🤖 Upload Inteligente com IA
        </DialogTitle>
        <DialogContent>
          <Typography variant="body1" sx={{ mb: 3 }}>
            Faça upload do PDF de legislação para que nossa IA extraia automaticamente os dados estruturados.
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
            onClick={() => document.getElementById('legislation-file-upload')?.click()}
          >
            <input
              id="legislation-file-upload"
              type="file"
              accept=".pdf"
              hidden
              onChange={(e) => setUploadFile(e.target.files?.[0] || null)}
            />
            <CloudUpload sx={{ fontSize: 48, color: 'primary.main', mb: 2 }} />
            <Typography variant="h6" gutterBottom>
              {uploadFile ? `✓ ${uploadFile.name}` : 'Selecione um arquivo PDF'}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              A IA irá classificar, extrair e estruturar os dados automaticamente
            </Typography>
          </Box>

          {processing && (
            <Box sx={{ mt: 3, textAlign: 'center' }}>
              <CircularProgress />
              <Typography variant="body2" sx={{ mt: 2 }}>
                🧠 Processando com IA... 
                <br />
                Classificando documento e extraindo dados estruturados
              </Typography>
            </Box>
          )}

          {aiResults && (
            <Alert severity="success" sx={{ mt: 3 }}>
              <Typography variant="subtitle1">✅ Processamento Concluído!</Typography>
              <Typography variant="body2">
                Documento processado com {(aiResults.confidence_score * 100).toFixed(1)}% de confiança 
                em {aiResults.processamento_tempo_segundos.toFixed(1)}s.
              </Typography>
              {aiResults.sugestoes_validacao.length > 0 && (
                <Box sx={{ mt: 2 }}>
                  <Typography variant="caption" display="block">
                    💡 Sugestões de validação:
                  </Typography>
                  {aiResults.sugestoes_validacao.map((sugestao, index) => (
                    <Typography key={index} variant="caption" display="block" sx={{ ml: 2 }}>
                      • {sugestao}
                    </Typography>
                  ))}
                </Box>
              )}
            </Alert>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setUploadDialogOpen(false)}>
            Cancelar
          </Button>
          <Button 
            variant="contained" 
            onClick={handleUploadPDF}
            disabled={!uploadFile || processing}
            startIcon={processing ? <CircularProgress size={20} /> : <AutoAwesome />}
          >
            {processing ? 'Processando...' : '🧠 Processar com IA'}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Manual Entry Dialog */}
      <Dialog 
        open={manualDialogOpen} 
        onClose={() => setManualDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          ✏️ Cadastro Manual de Documento
        </DialogTitle>
        <DialogContent>
          <Grid container spacing={3} sx={{ mt: 1 }}>
            <Grid item xs={12}>
              <TextField
                fullWidth
                label="Título do Documento"
                value={manualForm.titulo}
                onChange={(e) => setManualForm({...manualForm, titulo: e.target.value})}
                required
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <FormControl fullWidth required>
                <InputLabel>Tipo de Documento</InputLabel>
                <Select
                  value={manualForm.tipo_documento}
                  label="Tipo de Documento"
                  onChange={(e) => setManualForm({...manualForm, tipo_documento: e.target.value})}
                >
                  {tiposDocumento.map((tipo) => (
                    <MenuItem key={tipo.value} value={tipo.value}>
                      {tipo.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Número/Código"
                value={manualForm.numero_documento}
                onChange={(e) => setManualForm({...manualForm, numero_documento: e.target.value})}
                placeholder="Ex: Lei 14.442/2022"
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Data de Publicação"
                type="date"
                value={manualForm.data_publicacao}
                onChange={(e) => setManualForm({...manualForm, data_publicacao: e.target.value})}
                InputLabelProps={{ shrink: true }}
              />
            </Grid>
            <Grid item xs={12} sm={6}>
              <TextField
                fullWidth
                label="Órgão Emissor"
                value={manualForm.orgao_emissor}
                onChange={(e) => setManualForm({...manualForm, orgao_emissor: e.target.value})}
                placeholder="Ex: Ministério do Trabalho"
              />
            </Grid>
          </Grid>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setManualDialogOpen(false)}>
            Cancelar
          </Button>
          <Button 
            variant="contained" 
            onClick={handleManualSubmit}
            disabled={!manualForm.titulo}
            startIcon={<SaveIcon />}
          >
            Salvar Documento
          </Button>
        </DialogActions>
      </Dialog>

      {/* Document Details Dialog */}
      {selectedDocument && (
        <Dialog 
          open={Boolean(selectedDocument)} 
          onClose={() => setSelectedDocument(null)}
          maxWidth="lg"
          fullWidth
        >
          <DialogTitle>
            📄 Detalhes do Documento
          </DialogTitle>
          <DialogContent>
            <Grid container spacing={3}>
              <Grid item xs={12} md={6}>
                <Typography variant="subtitle2" gutterBottom>Informações Básicas:</Typography>
                <Box sx={{ mb: 2 }}>
                  <Typography variant="h6">{selectedDocument.titulo}</Typography>
                  <Typography variant="body2" color="text.secondary">
                    {getTipoDocumentoLabel(selectedDocument.tipo_documento)}
                    {selectedDocument.numero_documento && ` • ${selectedDocument.numero_documento}`}
                  </Typography>
                  {selectedDocument.orgao_emissor && (
                    <Typography variant="body2" color="text.secondary">
                      {selectedDocument.orgao_emissor}
                    </Typography>
                  )}
                  {selectedDocument.data_publicacao && (
                    <Typography variant="body2" color="text.secondary">
                      Publicado em: {new Date(selectedDocument.data_publicacao).toLocaleDateString()}
                    </Typography>
                  )}
                </Box>
                <Box sx={{ mb: 2 }}>
                  {getStatusChip(selectedDocument.status_processamento)}
                </Box>
              </Grid>
              
              <Grid item xs={12} md={6}>
                {selectedDocument.dados_extraidos && (
                  <>
                    <Typography variant="subtitle2" gutterBottom>📊 Dados Extraídos pela IA:</Typography>
                    <Box sx={{ backgroundColor: 'grey.50', p: 2, borderRadius: 1, maxHeight: 400, overflow: 'auto' }}>
                      <Typography variant="caption" component="pre" sx={{ fontSize: '0.75rem', whiteSpace: 'pre-wrap' }}>
                        {JSON.stringify(selectedDocument.dados_extraidos, null, 2)}
                      </Typography>
                    </Box>
                  </>
                )}
              </Grid>
            </Grid>
          </DialogContent>
          <DialogActions>
            <Button onClick={() => setSelectedDocument(null)}>
              Fechar
            </Button>
          </DialogActions>
        </Dialog>
      )}
    </Container>
  );
};

export default GestaoLegislacaoPage;