import React, { useState } from 'react';
import { useAuditorias, useRelatorios, useUploads } from '../lib/hooks/usePortalDemandasAuditoria';
import { Box, Card, CardContent, Typography, Chip, Button } from '@mui/material';
import Grid from '@mui/material/Grid';
import Link from 'next/link';
import { IAAnalysisButton } from './IAAnalysisButton';
import { Assignment, Assessment, CloudUpload } from '@mui/icons-material';

export const AuditoriasList: React.FC = () => {
  const auditorias = useAuditorias();
  const [busca, setBusca] = useState('');
    const [filtroStatus, setFiltroStatus] = useState<'todas' | 'em_andamento' | 'concluida' | 'pendente' | 'cancelada'>('todas');
  const [filtroResponsavel, setFiltroResponsavel] = useState('');
  const [filtroData, setFiltroData] = useState('');
  let auditoriasFiltradas = auditorias.filter(a => a.descricao.toLowerCase().includes(busca.toLowerCase()));
  if (filtroStatus !== 'todas') {
    auditoriasFiltradas = auditoriasFiltradas.filter(a => a.status === filtroStatus);
  }
  if (filtroResponsavel) auditoriasFiltradas = auditoriasFiltradas.filter(a => a.responsavel && a.responsavel.toLowerCase().includes(filtroResponsavel.toLowerCase()));
  if (filtroData) auditoriasFiltradas = auditoriasFiltradas.filter(a => a.data_inicio && a.data_inicio.startsWith(filtroData));
  if (!auditorias.length) return <div>Nenhuma auditoria encontrada.</div>;
  // Badge de status
  const emAndamento = auditorias.filter(a => a.status === 'em_andamento').length;
  const pendentes = auditorias.filter(a => a.status === 'pendente').length;
  // Função para marcar como concluída (placeholder, sem parâmetro)
  const marcarComoConcluida = () => {
    // Aqui você pode implementar a lógica para marcar como concluída, se necessário.
    // Atualmente, esta função não faz nada porque auditoriasState foi removido.
  };
  return (
    <Box>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Typography variant="h5" fontWeight={700}>Auditorias</Typography>
        {emAndamento > 0 && <Chip label={`${emAndamento} em andamento`} color="primary" size="small" />}
        {pendentes > 0 && <Chip label={`${pendentes} pendente${pendentes > 1 ? 's' : ''}`} color="warning" size="small" />}
      </Box>
      <Box mb={2} display="flex" gap={2} flexWrap="wrap">
        <input
          type="text"
          placeholder="Buscar por descrição..."
          value={busca}
          onChange={e => setBusca(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: 180 }}
        />
        <input
          type="text"
          placeholder="Responsável..."
          value={filtroResponsavel}
          onChange={e => setFiltroResponsavel(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: 140 }}
        />
        <input
          type="date"
          value={filtroData}
          onChange={e => setFiltroData(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: 150 }}
        />
  <Button variant={filtroStatus === 'todas' ? 'contained' : 'outlined'} onClick={() => setFiltroStatus('todas' as typeof filtroStatus)}>Todas</Button>
        <Button variant={filtroStatus === 'em_andamento' ? 'contained' : 'outlined'} color="primary" onClick={() => setFiltroStatus('em_andamento')}>Em andamento</Button>
        <Button variant={filtroStatus === 'concluida' ? 'contained' : 'outlined'} color="success" onClick={() => setFiltroStatus('concluida')}>Concluídas</Button>
        <Button variant={filtroStatus === 'pendente' ? 'contained' : 'outlined'} color="warning" onClick={() => setFiltroStatus('pendente')}>Pendentes</Button>
        <Button variant={filtroStatus === 'cancelada' ? 'contained' : 'outlined'} color="error" onClick={() => setFiltroStatus('cancelada')}>Canceladas</Button>
      </Box>
      <Grid container spacing={2}>
        {auditoriasFiltradas.map(a => (
          <Grid size={{ xs: 12, sm: 6, md: 4 }} key={a.id}>
            <Card sx={{ borderRadius: 2, boxShadow: 2, mb: 2, background: a.status === 'concluida' ? '#e8f5e9' : '#fff' }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Chip icon={<Assignment />} label={`ID: ${a.id}`} size="small" />
                  {a.status === 'em_andamento' && <Chip label="Em andamento" color="primary" size="small" />}
                  {a.status === 'pendente' && <Chip label="Pendente" color="warning" size="small" />}
                  {a.status === 'concluida' && <Chip label="Concluída" color="success" size="small" />}
                  {a.status === 'cancelada' && <Chip label="Cancelada" color="error" size="small" />}
                </Box>
                <Typography variant="h6" fontWeight={600}>{a.descricao}</Typography>
                <Typography variant="body2" color="text.secondary">Empresa: {a.empresa_id}</Typography>
                <Typography variant="body2" color="text.secondary">Início: {a.data_inicio}</Typography>
                {a.data_fim && <Typography variant="body2" color="text.secondary">Fim: {a.data_fim}</Typography>}
                <Typography variant="body2" color="text.secondary">Responsável: {a.responsavel}</Typography>
                <Box mt={2} display="flex" justifyContent="flex-end" gap={1}>
                  {a.status !== 'concluida' && a.status !== 'cancelada' && (
                    <Button size="small" color="success" variant="contained" onClick={marcarComoConcluida}>Concluir</Button>
                  )}
                  <Link href={`/demandas/auditoria/${a.id}`} passHref>
                    <Button
                      size="small"
                      variant="outlined"
                    >
                      Detalhes
                    </Button>
                  </Link>
                  <IAAnalysisButton context={`Auditoria: ${a.descricao} (ID: ${a.id})`} />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export const RelatoriosList: React.FC = () => {
  const relatorios = useRelatorios();
  const [busca, setBusca] = useState('');
  const [filtroEmpresa, setFiltroEmpresa] = useState('');
  const [filtroData, setFiltroData] = useState('');
  let relatoriosFiltrados = relatorios.filter(r => r.titulo.toLowerCase().includes(busca.toLowerCase()));
  if (filtroEmpresa) relatoriosFiltrados = relatoriosFiltrados.filter(r => r.empresa_id && String(r.empresa_id).includes(filtroEmpresa));
  if (filtroData) relatoriosFiltrados = relatoriosFiltrados.filter(r => r.data_emissao && r.data_emissao.startsWith(filtroData));
  if (!relatorios.length) return <div>Nenhum relatório encontrado.</div>;
  // Badge de documentos recentes (últimos 7 dias)
  const recentes = relatorios.filter(r => {
    const data = new Date(r.data_emissao);
    const agora = new Date();
    return (agora.getTime() - data.getTime()) < 7 * 24 * 60 * 60 * 1000;
  }).length;
  return (
    <Box>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Typography variant="h5" fontWeight={700}>Relatórios</Typography>
        {recentes > 0 && <Chip label={`${recentes} novo${recentes > 1 ? 's' : ''}`} color="info" size="small" />}
      </Box>
      <Box mb={2} display="flex" gap={2} flexWrap="wrap">
        <input
          type="text"
          placeholder="Buscar por título..."
          value={busca}
          onChange={e => setBusca(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: 180 }}
        />
        <input
          type="text"
          placeholder="Empresa..."
          value={filtroEmpresa}
          onChange={e => setFiltroEmpresa(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: 120 }}
        />
        <input
          type="date"
          value={filtroData}
          onChange={e => setFiltroData(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: 150 }}
        />
      </Box>
      <Grid container spacing={2}>
        {relatoriosFiltrados.map(r => (
          <Grid size={{ xs: 12, sm: 6, md: 4 }} key={r.id}>
            <Card sx={{ borderRadius: 2, boxShadow: 2, mb: 2 }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Chip icon={<Assessment />} label={`ID: ${r.id}`} size="small" />
                  <Chip label={`Empresa: ${r.empresa_id}`} size="small" />
                  {r.link_documento && <Chip label="Documento" color="primary" size="small" />}
                </Box>
                <Typography variant="h6" fontWeight={600}>{r.titulo}</Typography>
                <Typography variant="body2" color="text.secondary">Emissão: {r.data_emissao}</Typography>
                {r.link_documento && <Button href={r.link_documento} target="_blank" rel="noopener noreferrer" size="small" color="primary" sx={{ mt: 1 }}>Ver documento</Button>}
                <Box mt={2} display="flex" justifyContent="flex-end" gap={1}>
                  <Link href={`/demandas/relatorio/${r.id}`} passHref>
                    <Button
                      size="small"
                      variant="outlined"
                    >
                      Detalhes
                    </Button>
                  </Link>
                  <IAAnalysisButton context={`Relatório: ${r.titulo} (ID: ${r.id})`} />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

export const UploadsList: React.FC = () => {
  const uploads = useUploads();
  const [busca, setBusca] = useState('');
  const uploadsFiltrados = uploads.filter(u => u.nome_arquivo.toLowerCase().includes(busca.toLowerCase()));
  if (!uploads.length) return <div>Nenhum upload realizado.</div>;
  // Badge de uploads recentes (últimos 3 dias)
  const recentes = uploads.filter(u => {
    const data = new Date(u.data_upload);
    const agora = new Date();
    return (agora.getTime() - data.getTime()) < 3 * 24 * 60 * 60 * 1000;
  }).length;
  return (
    <Box>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Typography variant="h5" fontWeight={700}>Uploads</Typography>
        {recentes > 0 && <Chip label={`${recentes} novo${recentes > 1 ? 's' : ''}`} color="info" size="small" />}
      </Box>
      <Box mb={2}>
        <input
          type="text"
          placeholder="Buscar por nome do arquivo..."
          value={busca}
          onChange={e => setBusca(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: '100%', maxWidth: 320 }}
        />
      </Box>
      <Grid container spacing={2}>
        {uploadsFiltrados.map(u => (
          <Grid size={{ xs: 12, sm: 6, md: 4 }} key={u.id}>
            <Card sx={{ borderRadius: 2, boxShadow: 2, mb: 2 }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Chip icon={<CloudUpload />} label={`ID: ${u.id}`} size="small" />
                  <Chip label={`Empresa: ${u.empresa_id}`} size="small" />
                  {u.url && <Chip label="Arquivo" color="primary" size="small" />}
                </Box>
                <Typography variant="h6" fontWeight={600}>{u.nome_arquivo}</Typography>
                <Typography variant="body2" color="text.secondary">Data: {u.data_upload}</Typography>
                <Typography variant="body2" color="text.secondary">Usuário: {u.usuario_upload}</Typography>
                <Box mt={2} display="flex" justifyContent="flex-end" gap={1}>
                  {u.url && <Button href={u.url} target="_blank" rel="noopener noreferrer" size="small" color="success">Baixar</Button>}
                  <Link href={`/demandas/upload/${u.id}`} passHref>
                    <Button
                      size="small"
                      variant="outlined"
                    >
                      Detalhes
                    </Button>
                  </Link>
                  <IAAnalysisButton context={`Upload: ${u.nome_arquivo} (ID: ${u.id})`} />
                </Box>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};
