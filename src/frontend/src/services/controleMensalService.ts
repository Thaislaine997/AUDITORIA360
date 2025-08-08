// src/frontend/src/services/controleMensalService.ts

import api from './api';

// Tipos que espelham os nossos schemas Pydantic
// (Idealmente, estes tipos podem ser partilhados entre frontend e backend)
export interface Tarefa {
  id: number;
  nome_tarefa: string;
  concluido: boolean;
  data_conclusao?: string;
}

export interface ControleMensalDetalhado {
  id_controle: number;
  mes: number;
  ano: number;
  status_dados: string;
  id_empresa: number;
  nome_empresa: string;
  tarefas: Tarefa[];
}

export const getControlesDoMes = async (ano: number, mes: number): Promise<ControleMensalDetalhado[]> => {
  const response = await api.get(`/controles-mensais/${ano}/${mes}`);
  return response.data;
};

export const atualizarStatusTarefa = async (tarefaId: number, concluido: boolean): Promise<Tarefa> => {
  const response = await api.patch(`/controles-mensais/tarefas/${tarefaId}/status?concluido=${concluido}`);
  return response.data;
};