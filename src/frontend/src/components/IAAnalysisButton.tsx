import React, { useState } from 'react';
import { Button, Dialog, DialogTitle, DialogContent, DialogActions, Box, Typography, CircularProgress, List, ListItem, ListItemText, Divider, Snackbar, Alert } from '@mui/material';
// Criação real de tarefa via API
async function criarTarefa(descricao: string) {
  const resp = await fetch('/api/tarefas', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ descricao }),
  });
  if (!resp.ok) throw new Error('Erro ao criar tarefa');
  return await resp.json();
}
// Criação real de notificação via API
async function criarNotificacao(descricao: string) {
  const resp = await fetch('/api/notificacoes', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ descricao }),
  });
  if (!resp.ok) throw new Error('Erro ao criar notificação');
  return await resp.json();
}
// Criação real de auditoria via API
async function criarAuditoria(descricao: string) {
  const resp = await fetch('/api/auditorias', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ descricao }),
  });
  if (!resp.ok) throw new Error('Erro ao criar auditoria');
  return await resp.json();
}
// Criação real de relatório via API
async function criarRelatorio(descricao: string) {
  const resp = await fetch('/api/relatorios', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ descricao }),
  });
  if (!resp.ok) throw new Error('Erro ao criar relatório');
  return await resp.json();
}
  const [snackbar, setSnackbar] = useState<{ open: boolean; message: string; severity: 'success'|'error' }>({ open: false, message: '', severity: 'success' });
import { SmartToy, History as HistoryIcon } from '@mui/icons-material';
import { useIAHistory } from '../lib/hooks/useIAHistory';

export interface IAAnalysisButtonProps {
  context: string;
  label?: string;
}


export const IAAnalysisButton: React.FC<IAAnalysisButtonProps> = ({ context, label = 'Analisar com IA' }) => {
  const [open, setOpen] = useState(false);
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<string | null>(null);
  const [showHistory, setShowHistory] = useState(false);
  const { history, addInteraction } = useIAHistory();

  // Chamada real para endpoint de IA/MCP
  const handleAnalyze = async () => {
    setLoading(true);
    setResult(null);
    try {
      // Substitua a URL abaixo pelo endpoint real da IA/MCP
      const response = await fetch('/api/ia/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ context }),
      });
      if (!response.ok) throw new Error('Erro ao consultar IA');
      const data = await response.json();
      const resposta = data.result || 'Sugestão IA: análise automática realizada para o contexto.';
      setResult(resposta);
      addInteraction(context, resposta);
    } catch (err) {
      setResult('Erro ao consultar IA.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Button
        variant="outlined"
        color="secondary"
        size="small"
        startIcon={<SmartToy />}
        onClick={() => { setOpen(true); handleAnalyze(); }}
        sx={{ ml: 1 }}
      >
        {label}
      </Button>
  <Dialog open={open} onClose={() => setOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Análise IA</DialogTitle>
  <DialogContent dividers>
          <Typography variant="body2" color="text.secondary" mb={2}>
            Contexto analisado:
          </Typography>
          <Box bgcolor="#f5f5f5" p={2} borderRadius={2} mb={2} fontSize={14}>
            {context}
          </Box>
          {loading && <CircularProgress size={24} sx={{ display: 'block', mx: 'auto', my: 2 }} />}
          {result && (
            <>
              <Typography color="primary.main" mb={2}>{result}</Typography>
              <Box display="flex" gap={2} flexWrap="wrap" mb={2}>
                <Button
                  variant="contained"
                  color="primary"
                  size="small"
                  onClick={async () => {
                    setSnackbar({ open: true, message: 'Criando tarefa...', severity: 'success' });
                    try {
                      await criarTarefa(result);
                      setSnackbar({ open: true, message: 'Tarefa criada com sucesso!', severity: 'success' });
                    } catch {
                      setSnackbar({ open: true, message: 'Erro ao criar tarefa.', severity: 'error' });
                    }
                  }}
                >
                  Criar tarefa sugerida
                </Button>
                <Button
                  variant="contained"
                  color="secondary"
                  size="small"
                  onClick={async () => {
                    setSnackbar({ open: true, message: 'Criando notificação...', severity: 'success' });
                    try {
                      await criarNotificacao(result);
                      setSnackbar({ open: true, message: 'Notificação criada com sucesso!', severity: 'success' });
                    } catch {
                      setSnackbar({ open: true, message: 'Erro ao criar notificação.', severity: 'error' });
                    }
                  }}
                >
                  Criar notificação sugerida
                </Button>
                <Button
                  variant="contained"
                  color="success"
                  size="small"
                  onClick={async () => {
                    setSnackbar({ open: true, message: 'Criando auditoria...', severity: 'success' });
                    try {
                      await criarAuditoria(result);
                      setSnackbar({ open: true, message: 'Auditoria criada com sucesso!', severity: 'success' });
                    } catch {
                      setSnackbar({ open: true, message: 'Erro ao criar auditoria.', severity: 'error' });
                    }
                  }}
                >
                  Criar auditoria sugerida
                </Button>
                <Button
                  variant="contained"
                  color="info"
                  size="small"
                  onClick={async () => {
                    setSnackbar({ open: true, message: 'Criando relatório...', severity: 'success' });
                    try {
                      await criarRelatorio(result);
                      setSnackbar({ open: true, message: 'Relatório criado com sucesso!', severity: 'success' });
                    } catch {
                      setSnackbar({ open: true, message: 'Erro ao criar relatório.', severity: 'error' });
                    }
                  }}
                >
                  Criar relatório sugerido
                </Button>
              </Box>
            </>
          )}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={2500}
        onClose={() => setSnackbar(s => ({ ...s, open: false }))}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={() => setSnackbar(s => ({ ...s, open: false }))} severity={snackbar.severity} sx={{ width: '100%' }}>
          {snackbar.message}
        </Alert>
      </Snackbar>
          <Divider sx={{ my: 2 }} />
          <Box display="flex" alignItems="center" gap={1} mb={1}>
            <HistoryIcon fontSize="small" color="action" />
            <Typography variant="subtitle2" color="text.secondary">Histórico de Interações IA</Typography>
            <Button size="small" onClick={() => setShowHistory(h => !h)}>{showHistory ? 'Ocultar' : 'Exibir'}</Button>
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
        </DialogActions>
      </Dialog>
    </>
  );
};
