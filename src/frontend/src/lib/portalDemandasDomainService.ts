import { Empresa, Sindicato, ConvencaoColetivaCCT, Tarefa } from './portalDemandasTypes';

// MOCK DATA
const empresas: Empresa[] = [
  { id: 1, nome: 'Empresa Exemplo', contabilidade_id: 1, sindicato_id: 1, criado_em: new Date().toISOString() },
];
const sindicatos: Sindicato[] = [
  { id: 1, nome_sindicato: 'Sindicato dos Comerciários', cnpj: '12.345.678/0001-99', base_territorial: 'São Paulo', categoria_representada: 'Comércio', criado_em: new Date().toISOString() },
];
const ccts: ConvencaoColetivaCCT[] = [
  { id: 1, sindicato_id: 1, numero_registro_mte: 'MTE-123456', vigencia_inicio: '2024-01-01', vigencia_fim: '2024-12-31', link_documento_oficial: '', dados_cct: {}, criado_em: new Date().toISOString() },
];
const tarefas: Tarefa[] = [
  { id: 1, nome_tarefa: 'Enviar folha de pagamento', concluido: false },
  { id: 2, nome_tarefa: 'Validar CCT', concluido: true, data_conclusao: new Date().toISOString() },
];

export const portalDemandasDomainService = {
  listarEmpresas: async (): Promise<Empresa[]> => empresas,
  listarSindicatos: async (): Promise<Sindicato[]> => sindicatos,
  listarCCTs: async (): Promise<ConvencaoColetivaCCT[]> => ccts,
  listarTarefas: async (): Promise<Tarefa[]> => tarefas,
};
