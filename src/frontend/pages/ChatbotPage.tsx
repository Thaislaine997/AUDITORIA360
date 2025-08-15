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
  ListItemText,
  Avatar,
  Chip,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from "@mui/material";
import {
  SmartToy,
  Person,
  Psychology,
  Lightbulb,
  Help,
} from "@mui/icons-material";

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant' | 'system';
  content: string;
  timestamp: Date;
  context?: any;
}

interface EmpathicHelpProps {
  open: boolean;
  onClose: () => void;
  errorContext?: {
    formId: string;
    errorType: string;
    errorCount: number;
  };
}

const EmpathicHelpDialog: React.FC<EmpathicHelpProps> = ({ open, onClose, errorContext }) => {
  const [helpMessage, setHelpMessage] = useState("");
  const [example, setExample] = useState("");

  useEffect(() => {
    if (errorContext) {
      // Generate empathetic help based on error context
      const { formId, errorType, errorCount } = errorContext;
      
      let message = `Percebi que este campo está a ser complicado (${errorCount} tentativas). `;
      let exampleText = "";

      switch (errorType) {
        case 'email':
          message += "Posso ajudar com o formato do email?";
          exampleText = "Exemplo correto: usuario@empresa.com.br";
          break;
        case 'phone':
          message += "Vamos tentar com o formato de telefone?";
          exampleText = "Exemplo correto: (11) 99999-9999";
          break;
        case 'cnpj':
          message += "O CNPJ pode ser complicado. Deixe-me ajudar!";
          exampleText = "Exemplo correto: 11.222.333/0001-44";
          break;
        case 'date':
          message += "Datas podem ser confusas. Que tal este formato?";
          exampleText = "Exemplo correto: 15/01/2024";
          break;
        default:
          message += "Posso ajudar a preencher este campo corretamente?";
          exampleText = "Vou guiá-lo passo a passo.";
      }

      setHelpMessage(message);
      setExample(exampleText);
    }
  }, [errorContext]);

  return (
    <Dialog open={open} onClose={onClose} maxWidth="md" fullWidth>
      <DialogTitle sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
        <Psychology color="primary" />
        Assistente Empático
      </DialogTitle>
      <DialogContent>
        <Alert severity="info" sx={{ mb: 2 }} icon={<Lightbulb />}>
          {helpMessage}
        </Alert>
        
        {example && (
          <Box sx={{ mt: 2, p: 2, bgcolor: 'background.paper', borderRadius: 1, border: 1, borderColor: 'divider' }}>
            <Typography variant="subtitle2" gutterBottom>
              <Help sx={{ fontSize: 16, mr: 1 }} />
              Exemplo:
            </Typography>
            <Typography variant="body1" sx={{ fontFamily: 'monospace', color: 'primary.main' }}>
              {example}
            </Typography>
          </Box>
        )}

        <Box sx={{ mt: 3 }}>
          <Typography variant="body2" color="text.secondary">
            💡 <strong>Dica:</strong> A interface neural detectou que você pode precisar de ajuda. 
            Estou aqui para tornar este processo mais fácil e intuitivo.
          </Typography>
        </Box>
      </DialogContent>
      <DialogActions>
        <Button onClick={onClose}>
          Entendi, obrigado!
        </Button>
        <Button variant="contained" onClick={onClose}>
          Tentar novamente
        </Button>
      </DialogActions>
    </Dialog>
  );
};

const ChatbotPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'system',
      content: 'Olá! Sou o assistente empático da interface neuro-simbólica. Como posso ajudá-lo hoje?',
      timestamp: new Date(),
    }
  ]);
  const [inputMessage, setInputMessage] = useState("");
  const [isTyping, setIsTyping] = useState(false);

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
    setInputMessage("");
    setIsTyping(true);

    // Simulate AI response with empathetic understanding
    setTimeout(() => {
      const responses = [
        "Compreendo sua situação. A interface neural detectou alguns padrões que podem ajudar...",
        "Baseado nos seus padrões de interação, posso sugerir uma abordagem mais eficiente...", 
        "Percebi que você está navegando pela área de clientes. Posso pré-carregar os dados que você precisa?",
        "Sua carga cognitiva parece elevada. Que tal simplificarmos a interface temporariamente?",
        "Detectei hesitação no mouse. Posso explicar melhor essa funcionalidade?",
      ];

      const assistantMessage: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: responses[Math.floor(Math.random() * responses.length)],
        timestamp: new Date(),
      };

      setMessages(prev => [...prev, assistantMessage]);
      setIsTyping(false);
    }, 1000 + Math.random() * 2000);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4, mb: 4 }}>
      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, mb: 3 }}>
        <Psychology color="primary" />
        <Typography variant="h4" gutterBottom>
          Assistente Neuro-Simbólico
        </Typography>
        <Chip 
          label="Interface Empática Ativa" 
          color="success" 
          icon={<SmartToy />}
          size="small"
        />
      </Box>
      
      <Paper sx={{ height: 500, display: 'flex', flexDirection: 'column' }}>
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
                    maxWidth: '70%',
                    flexDirection: message.type === 'user' ? 'row-reverse' : 'row',
                  }}
                >
                  <Avatar 
                    sx={{ 
                      bgcolor: message.type === 'user' ? 'primary.main' : 'secondary.main',
                      width: 32,
                      height: 32,
                    }}
                  >
                    {message.type === 'user' ? <Person /> : <Psychology />}
                  </Avatar>
                  
                  <Paper 
                    elevation={1}
                    sx={{ 
                      p: 2, 
                      bgcolor: message.type === 'user' ? 'primary.light' : 'background.paper',
                      color: message.type === 'user' ? 'white' : 'text.primary',
                    }}
                  >
                    <Typography variant="body1">
                      {message.content}
                    </Typography>
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
            
            {isTyping && (
              <ListItem sx={{ justifyContent: 'flex-start' }}>
                <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                  <Avatar sx={{ bgcolor: 'secondary.main', width: 32, height: 32 }}>
                    <Psychology />
                  </Avatar>
                  <Paper elevation={1} sx={{ p: 2 }}>
                    <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
                      🧠 Processando sinais neurais...
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
              placeholder="Digite sua mensagem... (A interface neural está escutando)"
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
              disabled={!inputMessage.trim() || isTyping}
              sx={{ minWidth: 100 }}
            >
              Enviar
            </Button>
          </Box>
          
          <Typography variant="caption" color="text.secondary" sx={{ mt: 1, display: 'block' }}>
            💡 Este chatbot entende o contexto das suas interações e adapta-se ao seu estado cognitivo
          </Typography>
        </Box>
      </Paper>

      <Alert severity="info" sx={{ mt: 2 }} icon={<Psychology />}>
        <strong>Interface Neuro-Simbólica Ativa:</strong> Este assistente é acionado automaticamente 
        quando a interface detecta frustração ou dificuldades (ex: 3+ erros no mesmo formulário).
        Ele oferece ajuda contextual e empática baseada nos seus padrões de interação.
      </Alert>
    </Container>
  );
};

// Export both components for use in other parts of the application
export default ChatbotPage;
export { EmpathicHelpDialog };
