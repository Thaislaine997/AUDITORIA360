// src/frontend/src/pages/ValidacaoIAPage.tsx

import React, { useState, useEffect } from 'react';
import {
  Box,
  Paper,
  Typography,
  Alert,
  CircularProgress,
  Button,
  Tabs,
  Tab,
  Badge,
  Chip,
  Divider
} from '@mui/material';
import { 
  Psychology, 
  CheckCircle, 
  Pending, 
  Cancel,
  Refresh 
} from '@mui/icons-material';
import { ValidacaoIARow } from '../components/ValidacaoIARow';
import { supabase } from '../lib/supabaseClient';

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
  Documentos?: {
    nome: string;
  };
}

interface TabPanelProps {
  children?: React.ReactNode;
  index: number;
  value: number;
}

function TabPanel({ children, value, index }: TabPanelProps) {
  return (
    <div hidden={value !== index}>
      {value === index && <Box sx={{ pt: 3 }}>{children}</Box>}
    </div>
  );
}

export const ValidacaoIAPage: React.FC = () => {
  const [extracoes, setExtracoes] = useState<ExtracaoIA[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [processingIds, setProcessingIds] = useState<Set<number>>(new Set());
  const [tabValue, setTabValue] = useState(0);

  // Contar extrações por status
  const contadores = {
    PENDENTE: extracoes.filter(e => e.status_validacao === 'PENDENTE').length,
    APROVADO: extracoes.filter(e => e.status_validacao === 'APROVADO').length,
    REJEITADO: extracoes.filter(e => e.status_validacao === 'REJEITADO').length,
    CONCLUIDO: extracoes.filter(e => e.status_validacao === 'CONCLUIDO').length,
  };

  const carregarExtracoes = async () => {
    try {
      setLoading(true);
      setError(null);

      const { data, error: supabaseError } = await supabase
        .from('ExtracoesIA')
        .select(`
          *,
          Documentos:documento_id (
            nome
          )
        `)
        .order('criado_em', { ascending: false });

      if (supabaseError) {
        throw supabaseError;
      }

      setExtracoes(data || []);
    } catch (err) {
      console.error('Erro ao carregar extrações:', err);
      setError(`Erro ao carregar extrações: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const aprovarExtracao = async (id: number) => {
    if (processingIds.has(id)) return;

    try {
      setProcessingIds(prev => new Set([...prev, id]));

      const extracaoOriginal = extracoes.find(e => e.id === id);
      if (!extracaoOriginal) {
        throw new Error('Extração não encontrada');
      }

      // 1. Mover dados para a tabela RegrasValidadas
      const { error: insertError } = await supabase
        .from('RegrasValidadas')
        .insert({
          documento_id: extracaoOriginal.documento_id,
          nome_parametro: extracaoOriginal.nome_parametro,
          valor_parametro: extracaoOriginal.valor_parametro,
          tipo_valor: extracaoOriginal.tipo_valor,
          contexto_original: extracaoOriginal.contexto_original,
          ia_confidence_score: extracaoOriginal.ia_confidence_score,
          validado_por_humano: true,
          id_previsao_original: id,
          validado_em: new Date().toISOString(),
          validado_por: 'usuario_atual' // TODO: usar ID do usuário real
        });

      if (insertError) {
        throw insertError;
      }

      // 2. Atualizar status da extração original
      const { error: updateError } = await supabase
        .from('ExtracoesIA')
        .update({ 
          status_validacao: 'CONCLUIDO',
          validado_em: new Date().toISOString(),
          validado_por: 'usuario_atual' // TODO: usar ID do usuário real
        })
        .eq('id', id);

      if (updateError) {
        throw updateError;
      }

      // 3. Atualizar estado local
      setExtracoes(prev => prev.map(e => 
        e.id === id 
          ? { ...e, status_validacao: 'CONCLUIDO' as const }
          : e
      ));

      console.log('Extração aprovada com sucesso');

    } catch (err) {
      console.error('Erro ao aprovar extração:', err);
      setError(`Erro ao aprovar: ${err.message}`);
    } finally {
      setProcessingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(id);
        return newSet;
      });
    }
  };

  const editarExtracao = async (id: number, dadosEditados: Partial<ExtracaoIA>) => {
    if (processingIds.has(id)) return;

    try {
      setProcessingIds(prev => new Set([...prev, id]));

      const extracaoOriginal = extracoes.find(e => e.id === id);
      if (!extracaoOriginal) {
        throw new Error('Extração não encontrada');
      }

      // 1. Mover dados editados para RegrasValidadas
      const { error: insertError } = await supabase
        .from('RegrasValidadas')
        .insert({
          documento_id: extracaoOriginal.documento_id,
          nome_parametro: dadosEditados.nome_parametro || extracaoOriginal.nome_parametro,
          valor_parametro: dadosEditados.valor_parametro || extracaoOriginal.valor_parametro,
          tipo_valor: dadosEditados.tipo_valor || extracaoOriginal.tipo_valor,
          contexto_original: dadosEditados.contexto_original || extracaoOriginal.contexto_original,
          ia_confidence_score: extracaoOriginal.ia_confidence_score,
          validado_por_humano: true,
          id_previsao_original: id,
          validado_em: new Date().toISOString(),
          validado_por: 'usuario_atual' // TODO: usar ID do usuário real
        });

      if (insertError) {
        throw insertError;
      }

      // 2. Atualizar status da extração original
      const { error: updateError } = await supabase
        .from('ExtracoesIA')
        .update({ 
          status_validacao: 'CONCLUIDO',
          validado_em: new Date().toISOString(),
          validado_por: 'usuario_atual'
        })
        .eq('id', id);

      if (updateError) {
        throw updateError;
      }

      // 3. Atualizar estado local
      setExtracoes(prev => prev.map(e => 
        e.id === id 
          ? { ...e, status_validacao: 'CONCLUIDO' as const }
          : e
      ));

      console.log('Extração editada e aprovada com sucesso');

    } catch (err) {
      console.error('Erro ao editar extração:', err);
      setError(`Erro ao editar: ${err.message}`);
    } finally {
      setProcessingIds(prev => {
        const newSet = new Set(prev);
        newSet.delete(id);
        return newSet;
      });
    }
  };

  const filtrarExtracoesPorStatus = (status?: string) => {
    if (!status) return extracoes;
    return extracoes.filter(e => e.status_validacao === status);
  };

  useEffect(() => {
    carregarExtracoes();
  }, []);

  const getStatusName = (tabIndex: number): string => {
    switch (tabIndex) {
      case 0: return 'PENDENTE';
      case 1: return 'CONCLUIDO';
      case 2: return 'APROVADO';
      case 3: return 'REJEITADO';
      default: return '';
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
        <Typography variant="h6" sx={{ ml: 2 }}>
          Carregando extrações da IA...
        </Typography>
      </Box>
    );
  }

  return (
    <Box sx={{ p: 3 }}>
      <Paper sx={{ p: 3 }}>
        <Box sx={{ display: 'flex', alignItems: 'center', mb: 3 }}>
          <Psychology sx={{ fontSize: 40, color: 'primary.main', mr: 2 }} />
          <Box>
            <Typography variant="h4" gutterBottom>
              Validação de Extrações da IA
            </Typography>
            <Typography variant="body1" color="text.secondary">
              Revise e valide os parâmetros extraídos pela IA para melhorar a precisão do sistema.
            </Typography>
          </Box>
          <Box sx={{ ml: 'auto' }}>
            <Button
              onClick={carregarExtracoes}
              startIcon={<Refresh />}
              variant="outlined"
            >
              Atualizar
            </Button>
          </Box>
        </Box>

        {error && (
          <Alert severity="error" sx={{ mb: 3 }}>
            {error}
          </Alert>
        )}

        {/* Estatísticas Resumidas */}
        <Box sx={{ display: 'flex', gap: 2, mb: 3 }}>
          <Chip 
            icon={<Pending />}
            label={`Pendentes: ${contadores.PENDENTE}`}
            color="warning"
            variant="outlined"
          />
          <Chip 
            icon={<CheckCircle />}
            label={`Concluídas: ${contadores.CONCLUIDO}`}
            color="success"
            variant="outlined"
          />
          <Chip 
            label={`Total: ${extracoes.length}`}
            color="primary"
            variant="outlined"
          />
        </Box>

        <Divider sx={{ mb: 3 }} />

        {/* Tabs para filtrar por status */}
        <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
          <Tabs value={tabValue} onChange={(_, newValue) => setTabValue(newValue)}>
            <Tab 
              label={
                <Badge badgeContent={contadores.PENDENTE} color="warning">
                  Pendentes
                </Badge>
              } 
            />
            <Tab 
              label={
                <Badge badgeContent={contadores.CONCLUIDO} color="success">
                  Concluídas
                </Badge>
              } 
            />
            <Tab 
              label={
                <Badge badgeContent={contadores.APROVADO} color="primary">
                  Aprovadas
                </Badge>
              } 
            />
            <Tab 
              label={
                <Badge badgeContent={contadores.REJEITADO} color="error">
                  Rejeitadas
                </Badge>
              } 
            />
          </Tabs>
        </Box>

        {/* Conteúdo das Tabs */}
        {[0, 1, 2, 3].map((tabIndex) => (
          <TabPanel key={tabIndex} value={tabValue} index={tabIndex}>
            {filtrarExtracoesPorStatus(getStatusName(tabIndex)).length === 0 ? (
              <Alert severity="info">
                Nenhuma extração encontrada nesta categoria.
              </Alert>
            ) : (
              <Box>
                {filtrarExtracoesPorStatus(getStatusName(tabIndex)).map((extracao) => (
                  <ValidacaoIARow
                    key={extracao.id}
                    extracao={extracao}
                    onApprove={aprovarExtracao}
                    onEdit={editarExtracao}
                    isProcessing={processingIds.has(extracao.id)}
                  />
                ))}
              </Box>
            )}
          </TabPanel>
        ))}
      </Paper>
    </Box>
  );
};