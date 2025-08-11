import React, { useState, useEffect } from "react";
import { 
  Container, 
  Typography, 
  Paper, 
  Box,
  TextField,
  Button,
  List,
  ListItem,
  Avatar,
  Chip,
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Divider,
  Grid,
  IconButton,
  Tooltip,
} from "@mui/material";
import {
  SmartToy,
  Person,
  Psychology,
  Code,
  Refresh,
  CheckCircle,
  Warning,
  Error,
  Info,
  Send,
} from "@mui/icons-material";

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  sources?: Array<{
    file: string;
    type: string;
  }>;
}

interface AssistantStatus {
  database_exists: boolean;
  retrieval_ready: boolean;
  files_processed: number;
  last_training: number | null;
  message: string;
}

const DevAssistantPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'system',
      content: 'Olá! Sou o seu assistente de desenvolvimento interno do AUDITORIA360. 🧠\n\nPosso ajudar com:\n• Explicações sobre o código existente\n• Sugestões de implementação\n• Dúvidas sobre a arquitetura\n• Exemplos de uso das APIs\n• Boas práticas do projeto\n\nPergunta sobre qualquer parte do código!',
      timestamp: new Date(),
    }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isLoading, setIsLoading] = useState(false);
  const [status, setStatus] = useState<AssistantStatus | null>(null);
  const [statusLoading, setStatusLoading] = useState(false);

  // Load status on component mount
  useEffect(() => {
    loadStatus();
  }, []);

  const loadStatus = async () => {
    setStatusLoading(true);
    try {
      const response = await fetch('/api/v1/dev-assistant/status');
      if (response.ok) {
        const statusData = await response.json();
        setStatus(statusData);
      } else {
        console.error('Failed to load status');
      }
    } catch (error) {
      console.error('Error loading status:', error);
    } finally {
      setStatusLoading(false);
    }
  };

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    // Add user message
    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date(),
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = inputMessage;
    setInputMessage("");
    setIsLoading(true);

    try {
      const response = await fetch('/api/v1/dev-assistant/query', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ pergunta: currentInput }),
      });

      if (response.ok) {
        const data = await response.json();
        
        const assistantMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          content: data.resposta,
          timestamp: new Date(),
          sources: data.sources || [],
        };

        setMessages(prev => [...prev, assistantMessage]);
      } else {
        const errorData = await response.json();
        const errorMessage: ChatMessage = {
          id: (Date.now() + 1).toString(),
          type: 'system',
          content: `Erro: ${errorData.detail || 'Falha na comunicação com o assistente'}`,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, errorMessage]);
      }
    } catch (error) {
      const errorMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'system',
        content: `Erro de conexão: ${error instanceof Error ? error.message : 'Erro desconhecido'}`,
        timestamp: new Date(),
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  const handleRetrain = async () => {
    setStatusLoading(true);
    try {
      const response = await fetch('/api/v1/dev-assistant/retrain', {
        method: 'POST',
      });
      
      if (response.ok) {
        const data = await response.json();
        // Show success message
        const successMessage: ChatMessage = {
          id: Date.now().toString(),
          type: 'system',
          content: `✅ ${data.message}\nArquivos processados: ${data.files_processed}`,
          timestamp: new Date(),
        };
        setMessages(prev => [...prev, successMessage]);
        // Reload status
        await loadStatus();
      } else {
        const errorData = await response.json();
        console.error('Retrain failed:', errorData);
      }
    } catch (error) {
      console.error('Error retraining:', error);
    } finally {
      setStatusLoading(false);
    }
  };

  const getStatusIcon = (status: AssistantStatus | null) => {
    if (!status) return <Warning color="warning" />;
    if (status.retrieval_ready) return <CheckCircle color="success" />;
    if (status.database_exists) return <Warning color="warning" />;
    return <Error color="error" />;
  };

  const getStatusColor = (status: AssistantStatus | null) => {
    if (!status) return "warning";
    if (status.retrieval_ready) return "success";
    if (status.database_exists) return "warning";
    return "error";
  };

  return (
    <Container maxWidth="xl" sx={{ mt: 4, mb: 4 }}>
      <Grid container spacing={3}>
        {/* Header */}
        <Grid item xs={12}>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mb: 3 }}>
            <Psychology color="primary" sx={{ fontSize: 40 }} />
            <Box sx={{ flex: 1 }}>
              <Typography variant="h4" gutterBottom>
                Assistente de Desenvolvimento
              </Typography>
              <Typography variant="subtitle1" color="text.secondary">
                IA interna treinada no código do AUDITORIA360
              </Typography>
            </Box>
            <Chip 
              label="Cérebro Ativo" 
              color="success" 
              icon={<SmartToy />}
              size="medium"
            />
          </Box>
        </Grid>

        {/* Status Card */}
        <Grid item xs={12} md={4}>
          <Card>
            <CardContent>
              <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 2 }}>
                <Monitor color="primary" />
                <Typography variant="h6">Status do Sistema</Typography>
                <IconButton 
                  size="small" 
                  onClick={loadStatus}
                  disabled={statusLoading}
                >
                  {statusLoading ? <CircularProgress size={16} /> : <Refresh />}
                </IconButton>
              </Box>
              
              {status && (
                <Box sx={{ space: 1 }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 1 }}>
                    {getStatusIcon(status)}
                    <Typography variant="body2" color={getStatusColor(status)}>
                      {status.message}
                    </Typography>
                  </Box>
                  
                  <Typography variant="body2" color="text.secondary">
                    📁 Arquivos processados: {status.files_processed}
                  </Typography>
                  
                  <Typography variant="body2" color="text.secondary">
                    🗄️ Base de dados: {status.database_exists ? 'Existe' : 'Não existe'}
                  </Typography>
                  
                  <Typography variant="body2" color="text.secondary">
                    🔍 Sistema de busca: {status.retrieval_ready ? 'Pronto' : 'Não pronto'}
                  </Typography>
                  
                  {status.last_training && (
                    <Typography variant="body2" color="text.secondary">
                      🕐 Último treino: {new Date(status.last_training * 1000).toLocaleString()}
                    </Typography>
                  )}
                </Box>
              )}
              
              <Box sx={{ mt: 2 }}>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={handleRetrain}
                  disabled={statusLoading}
                  startIcon={statusLoading ? <CircularProgress size={16} /> : <Refresh />}
                  fullWidth
                >
                  Retreinar IA
                </Button>
              </Box>
            </CardContent>
          </Card>

          {/* Tips Card */}
          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                <Info color="primary" sx={{ mr: 1 }} />
                Dicas de Uso
              </Typography>
              <Typography variant="body2" paragraph>
                💡 <strong>Específico:</strong> "Como funciona a autenticação em auth.py?"
              </Typography>
              <Typography variant="body2" paragraph>
                🔍 <strong>Exploratório:</strong> "Que APIs existem para relatórios?"
              </Typography>
              <Typography variant="body2" paragraph>
                🏗️ <strong>Arquitetura:</strong> "Como está organizada a estrutura de routers?"
              </Typography>
              <Typography variant="body2">
                🐛 <strong>Debug:</strong> "Como resolver erros de CORS no frontend?"
              </Typography>
            </CardContent>
          </Card>
        </Grid>

        {/* Chat Interface */}
        <Grid item xs={12} md={8}>
          <Paper sx={{ height: 600, display: 'flex', flexDirection: 'column' }}>
            {/* Messages area */}
            <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
              <List>
                {messages.map((message) => (
                  <ListItem 
                    key={message.id} 
                    sx={{ 
                      justifyContent: message.type === 'user' ? 'flex-end' : 'flex-start',
                      mb: 1,
                    }}
                  >
                    <Box 
                      sx={{ 
                        display: 'flex', 
                        alignItems: 'flex-start',
                        gap: 1,
                        maxWidth: '85%',
                        flexDirection: message.type === 'user' ? 'row-reverse' : 'row',
                      }}
                    >
                      <Avatar 
                        sx={{ 
                          bgcolor: message.type === 'user' ? 'primary.main' : 
                                   message.type === 'system' ? 'warning.main' : 'secondary.main',
                          width: 32,
                          height: 32,
                        }}
                      >
                        {message.type === 'user' ? <Person /> : 
                         message.type === 'system' ? <Info /> : <Psychology />}
                      </Avatar>
                      
                      <Paper 
                        elevation={1}
                        sx={{ 
                          p: 2, 
                          bgcolor: message.type === 'user' ? 'primary.light' : 
                                   message.type === 'system' ? 'warning.light' : 'background.paper',
                          color: message.type === 'user' ? 'white' : 'text.primary',
                        }}
                      >
                        <Typography 
                          variant="body1" 
                          sx={{ whiteSpace: 'pre-wrap' }}
                        >
                          {message.content}
                        </Typography>
                        
                        {/* Show sources if available */}
                        {message.sources && message.sources.length > 0 && (
                          <Box sx={{ mt: 1 }}>
                            <Divider sx={{ mb: 1 }} />
                            <Typography variant="caption" color="text.secondary">
                              📚 Fontes consultadas:
                            </Typography>
                            <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5, mt: 0.5 }}>
                              {message.sources.map((source, idx) => (
                                <Tooltip key={idx} title={source.file}>
                                  <Chip 
                                    label={source.file.split('/').pop() || source.file}
                                    size="small"
                                    variant="outlined"
                                    sx={{ fontSize: '0.7rem' }}
                                  />
                                </Tooltip>
                              ))}
                            </Box>
                          </Box>
                        )}
                        
                        <Typography 
                          variant="caption" 
                          sx={{ 
                            opacity: 0.7,
                            display: 'block',
                            mt: 0.5,
                          }}
                        >
                          {message.timestamp.toLocaleTimeString()}
                        </Typography>
                      </Paper>
                    </Box>
                  </ListItem>
                ))}
                
                {isLoading && (
                  <ListItem sx={{ justifyContent: 'flex-start' }}>
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32 }}>
                        <Psychology />
                      </Avatar>
                      <Paper elevation={1} sx={{ p: 2, display: 'flex', alignItems: 'center', gap: 1 }}>
                        <CircularProgress size={16} />
                        <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
                          🧠 Analisando o código...
                        </Typography>
                      </Paper>
                    </Box>
                  </ListItem>
                )}
              </List>
            </Box>
            
            {/* Input area */}
            <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
              <Box sx={{ display: 'flex', gap: 1 }}>
                <TextField
                  fullWidth
                  placeholder="Faça sua pergunta sobre o código do AUDITORIA360..."
                  value={inputMessage}
                  onChange={(e) => setInputMessage(e.target.value)}
                  onKeyPress={handleKeyPress}
                  multiline
                  maxRows={3}
                  variant="outlined"
                  size="small"
                />
                <Button 
                  variant="contained" 
                  onClick={handleSendMessage}
                  disabled={!inputMessage.trim() || isLoading}
                  sx={{ minWidth: 100 }}
                  endIcon={<Send />}
                >
                  Enviar
                </Button>
              </Box>
              
              <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
                🧠 Este assistente conhece todo o código do projeto e pode ajudar com implementação, debugging e arquitetura.
              </Typography>
            </Box>
          </Paper>
        </Grid>
      </Grid>

      <Alert severity="info" sx={{ mt: 3 }} icon={<Psychology />}>
        <strong>Assistente de Desenvolvimento Interno:</strong> Esta IA foi treinada especificamente 
        no código-fonte do AUDITORIA360. Ela entende a arquitetura, padrões de código, APIs disponíveis 
        e pode ajudar a acelerar seu desenvolvimento mantendo a consistência do projeto.
      </Alert>
    </Container>
  );
};

export default DevAssistantPage;