// --- Domínios: Auditoria, Relatório, Upload ---

export interface Auditoria {
  id: number;
  empresa_id: number;
  descricao: string;
  status: 'em_andamento' | 'concluida' | 'pendente' | 'cancelada';
  data_inicio: string;
  data_fim?: string;
  responsavel: string;
  criado_em: string;
}

export interface Relatorio {
  id: number;
  titulo: string;
  empresa_id: number;
  data_emissao: string;
  link_documento?: string;
  criado_em: string;
}

export interface Upload {
  id: number;
  nome_arquivo: string;
  empresa_id: number;
  usuario_upload: string;
  data_upload: string;
  url?: string;
  criado_em: string;
}
// Modelos TypeScript gerados a partir do portal_demandas
// Estes tipos podem ser expandidos conforme a evolução do frontend

export enum TicketStatus {
  PENDENTE = 'pendente',
  EM_ANDAMENTO = 'em_andamento',
  AGUARDANDO = 'aguardando',
  CONCLUIDO = 'concluido',
  CANCELADO = 'cancelado',
}

export enum TicketPrioridade {
  BAIXA = 'baixa',
  MEDIA = 'media',
  ALTA = 'alta',
  CRITICA = 'critica',
}

export enum TicketCategoria {
  GERAL = 'geral',
  AUDITORIA = 'auditoria',
  FOLHA = 'folha',
  DOCUMENTOS = 'documentos',
  CCT = 'cct',
  SISTEMA = 'sistema',
}

export interface Ticket {
  id: number;
  titulo: string;
  descricao?: string;
  etapa: string;
  prazo: string; // ISO date
  responsavel: string;
  status: TicketStatus;
  prioridade: TicketPrioridade;
  categoria: TicketCategoria;
  tags?: string;
  tempo_estimado?: number;
  tempo_gasto?: number;
  criado_em: string; // ISO date
  atualizado_em: string; // ISO date
  comentarios_internos?: string;
  arquivo_anexo?: string;
}

export interface TicketComment {
  id?: number;
  ticket_id: number;
  autor: string;
  comentario: string;
  tipo?: string;
  criado_em?: string;
}

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

export interface Empresa {
  id: number;
  nome: string;
  contabilidade_id: number;
  sindicato_id?: number;
  criado_em?: string;
}

export interface Sindicato {
  id: number;
  nome_sindicato: string;
  cnpj?: string;
  base_territorial?: string;
  categoria_representada?: string;
  criado_em?: string;
}

export interface ConvencaoColetivaCCT {
  id: number;
  sindicato_id: number;
  numero_registro_mte: string;
  vigencia_inicio: string;
  vigencia_fim: string;
  link_documento_oficial?: string;
  dados_cct?: Record<string, any>;
  criado_em?: string;
}

export interface FuncionarioDivergencia {
  nome_funcionario: string;
  tipo_divergencia: string;
  descricao_divergencia: string;
  valor_encontrado?: string;
  valor_esperado?: string;
  campo_afetado: string;
}

export interface ProcessamentoFolhaResponse {
  id: number;
  empresa_id: number;
  mes: number;
  ano: number;
  arquivo_pdf: string;
  total_funcionarios: number;
  total_divergencias: number;
  status_processamento: string;
  criado_em: string;
  concluido_em?: string;
  divergencias: FuncionarioDivergencia[];
}

export interface Notificacao {
  id: number;
  usuario_id?: string;
  tipo_notificacao: string;
  titulo: string;
  mensagem: string;
  link_acao?: string;
  prioridade: string;
  origem_notificacao?: string;
  criado_em: string;
  lida?: boolean;
  data_leitura?: string;
}
