// src/frontend/src/components/ValidacaoIARow.tsx

import React, { useState } from 'react';
import { 
  Button, 
  Dialog, 
  DialogTitle, 
  DialogContent, 
  DialogActions, 
  TextField, 
  Box, 
  Typography, 
  Chip,
  Alert
} from '@mui/material';
import { Check, Edit, Info } from '@mui/icons-material';

interface ExtracaoIA {
  id: number;
  documento_id: number;
  nome_parametro: string;
  valor_parametro: string;
  tipo_valor: string;
  contexto_original: string;
  ia_confidence_score?: number;
  modelo_utilizado: string;
  criado_em: string;
  status_validacao: 'PENDENTE' | 'APROVADO' | 'REJEITADO' | 'CONCLUIDO';
}

interface Props {
  extracao: ExtracaoIA;
  onApprove: (id: number) => Promise<void>;
  onEdit: (id: number, editedData: Partial<ExtracaoIA>) => Promise<void>;
  isProcessing?: boolean;
}

export const ValidacaoIARow: React.FC<Props> = ({ 
  extracao, 
  onApprove, 
  onEdit, 
  isProcessing = false 
}) => {
  const [isEditDialogOpen, setIsEditDialogOpen] = useState(false);
  const [editedValues, setEditedValues] = useState({
    nome_parametro: extracao.nome_parametro,
    valor_parametro: extracao.valor_parametro,
    tipo_valor: extracao.tipo_valor,
    contexto_original: extracao.contexto_original
  });

  const handleApprove = async () => {
    try {
      await onApprove(extracao.id);
    } catch (error) {
      console.error('Erro ao aprovar extração:', error);
    }
  };

  const handleEditSave = async () => {
    try {
      await onEdit(extracao.id, editedValues);
      setIsEditDialogOpen(false);
    } catch (error) {
      console.error('Erro ao editar extração:', error);
    }
  };

  const handleEditCancel = () => {
    // Restaurar valores originais
    setEditedValues({
      nome_parametro: extracao.nome_parametro,
      valor_parametro: extracao.valor_parametro,
      tipo_valor: extracao.tipo_valor,
      contexto_original: extracao.contexto_original
    });
    setIsEditDialogOpen(false);
  };

  const getConfidenceColor = (score?: number): 'success' | 'warning' | 'error' | 'default' => {
    if (!score) return 'default';
    if (score >= 0.8) return 'success';
    if (score >= 0.6) return 'warning';
    return 'error';
  };

  const formatConfidenceScore = (score?: number): string => {
    if (!score) return 'N/A';
    return `${Math.round(score * 100)}%`;
  };

  return (
    <>
      <Box 
        sx={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center', 
          p: 2, 
          borderBottom: '1px solid #e0e0e0',
          backgroundColor: isProcessing ? '#f5f5f5' : 'transparent',
          opacity: isProcessing ? 0.7 : 1
        }}
      >
        <Box sx={{ flex: 1 }}>
          <Typography variant="h6" sx={{ fontWeight: 'bold', mb: 1 }}>
            {extracao.nome_parametro}
          </Typography>
          
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', mb: 1 }}>
            <Typography variant="body2">
              <strong>Valor:</strong> {extracao.valor_parametro}
            </Typography>
            
            <Chip 
              label={extracao.tipo_valor} 
              size="small" 
              color="primary" 
              variant="outlined" 
            />
            
            <Chip 
              label={`Confiança: ${formatConfidenceScore(extracao.ia_confidence_score)}`}
              size="small"
              color={getConfidenceColor(extracao.ia_confidence_score)}
              variant="outlined"
            />
          </Box>
          
          <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
            <strong>Contexto:</strong> "{extracao.contexto_original}"
          </Typography>
          
          <Typography variant="caption" color="text.secondary">
            Modelo: {extracao.modelo_utilizado} | 
            Extraído em: {new Date(extracao.criado_em).toLocaleString('pt-BR')}
          </Typography>
        </Box>

        <Box sx={{ display: 'flex', gap: 1, ml: 2 }}>
          <Button 
            onClick={handleApprove}
            disabled={isProcessing}
            startIcon={<Check />}
            variant="contained"
            color="success"
            size="small"
          >
            Aprovar
          </Button>
          
          <Button 
            onClick={() => setIsEditDialogOpen(true)}
            disabled={isProcessing}
            startIcon={<Edit />}
            variant="contained"
            color="warning"
            size="small"
          >
            Editar
          </Button>
        </Box>
      </Box>

      {/* Dialog de Edição */}
      <Dialog 
        open={isEditDialogOpen} 
        onClose={handleEditCancel}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
            <Edit />
            Editar Extração da IA
          </Box>
        </DialogTitle>
        
        <DialogContent>
          <Alert 
            severity="info" 
            sx={{ mb: 2 }}
            icon={<Info />}
          >
            Revise e corrija os dados extraídos pela IA antes de aprovar. 
            Suas correções ajudam o sistema a aprender.
          </Alert>

          <TextField
            label="Nome do Parâmetro"
            value={editedValues.nome_parametro}
            onChange={(e) => setEditedValues(prev => ({
              ...prev,
              nome_parametro: e.target.value
            }))}
            fullWidth
            margin="normal"
            helperText="Ex: aliquota_inss_faixa_1, valor_salario_minimo"
          />

          <TextField
            label="Valor do Parâmetro"
            value={editedValues.valor_parametro}
            onChange={(e) => setEditedValues(prev => ({
              ...prev,
              valor_parametro: e.target.value
            }))}
            fullWidth
            margin="normal"
            helperText="Ex: 7.5, 1550.00"
          />

          <TextField
            label="Tipo do Valor"
            value={editedValues.tipo_valor}
            onChange={(e) => setEditedValues(prev => ({
              ...prev,
              tipo_valor: e.target.value
            }))}
            fullWidth
            margin="normal"
            helperText="Ex: percentual, moeda, inteiro, texto"
          />

          <TextField
            label="Contexto Original"
            value={editedValues.contexto_original}
            onChange={(e) => setEditedValues(prev => ({
              ...prev,
              contexto_original: e.target.value
            }))}
            fullWidth
            multiline
            rows={3}
            margin="normal"
            helperText="Trecho do documento de onde esta informação foi extraída"
          />
        </DialogContent>

        <DialogActions>
          <Button onClick={handleEditCancel}>
            Cancelar
          </Button>
          <Button 
            onClick={handleEditSave}
            variant="contained"
            color="primary"
          >
            Salvar e Aprovar
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};