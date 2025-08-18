import { Auditoria, Relatorio, Upload } from './portalDemandasTypes';

// MOCK DATA
const auditorias: Auditoria[] = [
  { id: 1, empresa_id: 1, descricao: 'Auditoria Fiscal 2025', status: 'em_andamento', data_inicio: '2025-01-10', data_fim: '', responsavel: 'Equipe Fiscal', criado_em: new Date().toISOString() },
];
const relatorios: Relatorio[] = [
  { id: 1, titulo: 'Relatório de Auditoria 2025', empresa_id: 1, data_emissao: '2025-08-01', link_documento: '', criado_em: new Date().toISOString() },
];
const uploads: Upload[] = [
  { id: 1, nome_arquivo: 'folha_pagamento_jan2025.pdf', empresa_id: 1, usuario_upload: 'admin', data_upload: '2025-01-31', url: '', criado_em: new Date().toISOString() },
];

export const portalDemandasAuditoriaService = {
  listarAuditorias: async (): Promise<Auditoria[]> => auditorias,
  listarRelatorios: async (): Promise<Relatorio[]> => relatorios,
  listarUploads: async (): Promise<Upload[]> => uploads,
};
