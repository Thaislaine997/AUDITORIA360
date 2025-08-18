// Migrated from src/frontend/pages/ia/ChatbotPage.tsx
import React, { useState } from "react";
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
} from "@mui/material";
import {
  SmartToy,
  Person,
  Send,
} from "@mui/icons-material";

interface ChatMessage {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

const ChatbotPage: React.FC = () => {
  const [messages, setMessages] = useState<ChatMessage[]>([
    {
      id: '1',
      type: 'assistant',
      content: 'Olá! Sou o assistente inteligente do AUDITORIA360. Como posso ajudá-lo hoje?',
      timestamp: new Date()
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [loading, setLoading] = useState(false);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: ChatMessage = {
      id: Date.now().toString(),
      type: 'user',
      content: inputMessage,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInputMessage('');
    setLoading(true);

    // Simulate AI response
    setTimeout(() => {
      const aiResponse: ChatMessage = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: `Entendi sua pergunta: "${inputMessage}". Este é um sistema de demonstração. A funcionalidade completa do chatbot será implementada em breve.`,
        timestamp: new Date()
      };
      setMessages(prev => [...prev, aiResponse]);
      setLoading(false);
    }, 1000);
  };

  const handleKeyPress = (event: React.KeyboardEvent) => {
    if (event.key === 'Enter' && !event.shiftKey) {
      event.preventDefault();
      handleSendMessage();
    }
  };

  return (
    <Container maxWidth="md">
      <Box sx={{ py: 4 }}>
        <Typography variant="h4" gutterBottom>
          Assistente Inteligente
        </Typography>
        
        <Paper sx={{ height: '600px', display: 'flex', flexDirection: 'column' }}>
          {/* Chat Messages */}
          <Box sx={{ flex: 1, overflow: 'auto', p: 2 }}>
            <List>
              {messages.map((message) => (
                <ListItem key={message.id} sx={{ alignItems: 'flex-start' }}>
                  <Avatar sx={{ mr: 2, mt: 1 }}>
                    {message.type === 'user' ? <Person /> : <SmartToy />}
                  </Avatar>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                        <Chip 
                          label={message.type === 'user' ? 'Você' : 'Assistente'}
                          size="small"
                          color={message.type === 'user' ? 'primary' : 'secondary'}
                        />
                        <Typography variant="caption" sx={{ ml: 1, color: 'text.secondary' }}>
                          {message.timestamp.toLocaleTimeString()}
                        </Typography>
                      </Box>
                    }
                    secondary={
                      <Typography variant="body1">
                        {message.content}
                      </Typography>
                    }
                  />
                </ListItem>
              ))}
              {loading && (
                <ListItem>
                  <Avatar sx={{ mr: 2 }}>
                    <SmartToy />
                  </Avatar>
                  <ListItemText
                    primary={
                      <Chip label="Assistente" size="small" color="secondary" />
                    }
                    secondary={
                      <Typography variant="body1" sx={{ fontStyle: 'italic' }}>
                        Digitando...
                      </Typography>
                    }
                  />
                </ListItem>
              )}
            </List>
          </Box>
          
          {/* Input Area */}
          <Box sx={{ p: 2, borderTop: 1, borderColor: 'divider' }}>
            <Box sx={{ display: 'flex', gap: 1 }}>
              <TextField
                fullWidth
                multiline
                maxRows={3}
                placeholder="Digite sua pergunta..."
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                disabled={loading}
              />
              <Button
                variant="contained"
                onClick={handleSendMessage}
                disabled={loading || !inputMessage.trim()}
                startIcon={<Send />}
              >
                Enviar
              </Button>
            </Box>
          </Box>
        </Paper>
      </Box>
    </Container>
  );
};

export default ChatbotPage;