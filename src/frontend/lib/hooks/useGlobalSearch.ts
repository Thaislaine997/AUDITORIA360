import { useTickets } from './useTickets';
import { useAuditorias, useRelatorios, useUploads } from './usePortalDemandasAuditoria';
import { useEmpresas, useSindicatos, useCCTs, useTarefas } from './usePortalDemandasDomain';

export interface GlobalSearchResult {
  label: string;
  path: string;
  type: string;
}

export function useGlobalSearch(query: string): GlobalSearchResult[] {
  const { tickets } = useTickets();
  const auditorias = useAuditorias();
  const relatorios = useRelatorios();
  const uploads = useUploads();
  const empresas = useEmpresas();
  const sindicatos = useSindicatos();
  const ccts = useCCTs();
  const tarefas = useTarefas();

  if (!query.trim()) return [];
  const q = query.toLowerCase();
  const results: GlobalSearchResult[] = [];

  tickets.forEach(t => {
    if (
      t.titulo.toLowerCase().includes(q) ||
      (t.descricao && t.descricao.toLowerCase().includes(q))
    ) {
      results.push({
        label: `Ticket: ${t.titulo}`,
        path: `/demandas/ticket/${t.id}`,
        type: 'ticket',
      });
    }
  });
  auditorias.forEach(a => {
    if (
      a.descricao.toLowerCase().includes(q) ||
      (a.responsavel && a.responsavel.toLowerCase().includes(q))
    ) {
      results.push({
        label: `Auditoria: ${a.descricao}`,
        path: `/demandas/auditoria/${a.id}`,
        type: 'auditoria',
      });
    }
  });
  relatorios.forEach(r => {
    if (
      r.titulo.toLowerCase().includes(q)
    ) {
      results.push({
        label: `Relatório: ${r.titulo}`,
        path: `/demandas/relatorio/${r.id}`,
        type: 'relatorio',
      });
    }
  });
  uploads.forEach(u => {
    if (
      u.nome_arquivo.toLowerCase().includes(q)
    ) {
      results.push({
        label: `Upload: ${u.nome_arquivo}`,
        path: `/demandas/upload/${u.id}`,
        type: 'upload',
      });
    }
  });
  empresas.forEach(e => {
    if (e.nome.toLowerCase().includes(q)) {
      results.push({
        label: `Empresa: ${e.nome}`,
        path: `/demandas/empresa/${e.id}`,
        type: 'empresa',
      });
    }
  });
  sindicatos.forEach(s => {
    if (s.nome_sindicato.toLowerCase().includes(q)) {
      results.push({
        label: `Sindicato: ${s.nome_sindicato}`,
        path: `/demandas/sindicato/${s.id}`,
        type: 'sindicato',
      });
    }
  });
  ccts.forEach(c => {
    if (c.numero_registro_mte.toLowerCase().includes(q)) {
      results.push({
        label: `CCT: ${c.numero_registro_mte}`,
        path: `/demandas/cct/${c.id}`,
        type: 'cct',
      });
    }
  });
  tarefas.forEach(t => {
    if (t.nome_tarefa.toLowerCase().includes(q)) {
      results.push({
        label: `Tarefa: ${t.nome_tarefa}`,
        path: `/demandas/tarefa/${t.id}`,
        type: 'tarefa',
      });
    }
  });

  return results;
}
