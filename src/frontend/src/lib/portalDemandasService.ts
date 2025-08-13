// portalDemandasService.ts
// Serviços utilitários para manipulação de tickets, tarefas, auditorias, notificações, etc.
// Simula integração futura com backend/API (mock/local por enquanto)

import {
  Ticket,
  TicketStatus,
  TicketPrioridade,
  TicketCategoria,
  TicketComment,
  Tarefa,
  ControleMensalDetalhado,
  Empresa,
  Sindicato,
  ConvencaoColetivaCCT,
  FuncionarioDivergencia,
  ProcessamentoFolhaResponse,
  Notificacao,
} from './portalDemandasTypes';

// MOCK DATA (pode ser substituído por fetch/axios futuramente)
const tickets: Ticket[] = [
  {
    id: 1,
    titulo: 'Revisão Folha Julho',
    descricao: 'Revisar divergências apontadas na folha de julho.',
    etapa: 'Auditoria',
    prazo: new Date(Date.now() + 86400000 * 5).toISOString(),
    responsavel: 'Maria Silva',
    status: TicketStatus.PENDENTE,
    prioridade: TicketPrioridade.ALTA,
    categoria: TicketCategoria.FOLHA,
    criado_em: new Date().toISOString(),
    atualizado_em: new Date().toISOString(),
  },
];

const notificacoes: Notificacao[] = [
  {
    id: 1,
    tipo_notificacao: 'ALERTA',
    titulo: 'Divergências Críticas na Folha',
    mensagem: 'Foram encontradas divergências críticas na folha de pagamento.',
    prioridade: 'CRITICA',
    criado_em: new Date().toISOString(),
    lida: false,
  },
];

export const portalDemandasService = {
  // Tickets
  listarTickets: async (): Promise<Ticket[]> => {
    // Simulação: substituir por chamada à API futuramente
    return tickets;
  },
  obterTicket: async (id: number): Promise<Ticket | undefined> => {
    return tickets.find(t => t.id === id);
  },
  criarTicket: async (ticket: Omit<Ticket, 'id' | 'criado_em' | 'atualizado_em'>): Promise<Ticket> => {
    const novo: Ticket = {
      ...ticket,
      id: tickets.length + 1,
      criado_em: new Date().toISOString(),
      atualizado_em: new Date().toISOString(),
    };
    tickets.push(novo);
    return novo;
  },
  // Notificações
  listarNotificacoes: async (): Promise<Notificacao[]> => {
    return notificacoes;
  },
  marcarNotificacaoComoLida: async (id: number): Promise<void> => {
    const n = notificacoes.find(n => n.id === id);
    if (n) n.lida = true;
  },
  // Tarefas, empresas, sindicatos, CCTs, auditorias, etc. podem ser expandidos conforme necessidade
};
