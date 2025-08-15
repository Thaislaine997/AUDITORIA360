
import React, { useState } from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, TextField, Box, Typography, CircularProgress, List, ListItem, ListItemText, Divider } from '@mui/material';
import { SmartToy, History as HistoryIcon } from '@mui/icons-material';
import { useIAHistory } from '../lib/hooks/useIAHistory';

const IAChatAssistant: React.FC = () => {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const { history, addInteraction, clearHistory } = useIAHistory();
  const [messages, setMessages] = useState<{ sender: 'user' | 'ia'; text: string }[]>([]);
  const [showHistory, setShowHistory] = useState(false);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages(msgs => [...msgs, { sender: 'user', text: input }]);
    setLoading(true);
    try {
      // Substitua a URL abaixo pelo endpoint real da IA/MCP
      const response = await fetch('/api/ia/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: input }),
      });
      if (!response.ok) throw new Error('Erro ao consultar IA');
      const data = await response.json();
      const resposta = data.result || 'Resposta IA não disponível.';
      setMessages(msgs => [...msgs, { sender: 'ia', text: resposta }]);
      addInteraction(input, resposta);
    } catch (err) {
      setMessages(msgs => [...msgs, { sender: 'ia', text: 'Erro ao consultar IA.' }]);
    } finally {
      setLoading(false);
      setInput('');
    }
  };

  return (
    <>
      <Button
        variant="contained"
        color="secondary"
        startIcon={<SmartToy />}
        sx={{ position: 'fixed', bottom: 32, right: 32, zIndex: 2000, boxShadow: 4 }}
        onClick={() => setOpen(true)}
      >
        Assistente IA
      </Button>
      <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Assistente IA (MCP/GitHub Copilot Models)</DialogTitle>
        <DialogContent dividers>
          <Box minHeight={200} maxHeight={350} overflow="auto" mb={2}>
            {messages.length === 0 && (
              <Typography color="text.secondary">Envie uma dúvida, peça análise de um item ou solicite sugestões inteligentes para o sistema.</Typography>
            )}
            {messages.map((msg, idx) => (
              <Box key={idx} mb={1} textAlign={msg.sender === 'user' ? 'right' : 'left'}>
                <Box
                  display="inline-block"
                  px={2}
                  py={1}
                  borderRadius={2}
                  bgcolor={msg.sender === 'user' ? 'primary.light' : 'grey.200'}
                  color={msg.sender === 'user' ? 'primary.contrastText' : 'text.primary'}
                  fontWeight={msg.sender === 'user' ? 600 : 400}
                >
                  {msg.text}
                </Box>
              </Box>
            ))}
            {loading && <CircularProgress size={24} sx={{ display: 'block', mx: 'auto', my: 2 }} />}
          </Box>
          <TextField
            fullWidth
            placeholder="Digite sua dúvida ou comando..."
            value={input}
            onChange={e => setInput(e.target.value)}
            onKeyDown={e => { if (e.key === 'Enter') handleSend(); }}
            disabled={loading}
            autoFocus
          />
          <Divider sx={{ my: 2 }} />
          <Box display="flex" alignItems="center" gap={1} mb={1}>
            <HistoryIcon fontSize="small" color="action" />
            <Typography variant="subtitle2" color="text.secondary">Histórico Global IA</Typography>
            <Button size="small" onClick={() => setShowHistory(h => !h)}>{showHistory ? 'Ocultar' : 'Exibir'}</Button>
            <Button size="small" color="error" onClick={clearHistory}>Limpar</Button>
          </Box>
          {showHistory && (
            <List dense>
              {history.length === 0 && <ListItem><ListItemText primary="Nenhuma interação registrada." /></ListItem>}
              {history.map(h => (
                <ListItem key={h.id} alignItems="flex-start">
                  <ListItemText
                    primary={h.result}
                    secondary={<>
                      <Typography variant="caption" color="text.secondary">{new Date(h.date).toLocaleString()}</Typography>
                      <br />
                      <span style={{ color: '#888' }}>{h.context}</span>
                    </>}
                  />
                </ListItem>
              ))}
            </List>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpen(false)}>Fechar</Button>
          <Button onClick={handleSend} disabled={loading || !input.trim()} variant="contained">Enviar</Button>
        </DialogActions>
      </Dialog>
    </>
  );
};
export default IAChatAssistant;
