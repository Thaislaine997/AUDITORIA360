
import React, { useState } from 'react';
import TextField from '@mui/material/TextField';
// Função mock para simular atualização (substitua por chamada real de API se necessário)
function mockUpdate(item: any, updates: any) {
  return { ...item, ...updates };
}
  // Estados para edição rápida
  const [empresaEdit, setEmpresaEdit] = useState<any | null>(null);
  const [empresaEditValues, setEmpresaEditValues] = useState<any>({});
import Dialog from '@mui/material/Dialog';
import DialogTitle from '@mui/material/DialogTitle';
import DialogContent from '@mui/material/DialogContent';
import DialogActions from '@mui/material/DialogActions';
import IconButton from '@mui/material/IconButton';
import CloseIcon from '@mui/icons-material/Close';
import { useEmpresas, useSindicatos, useCCTs, useTarefas } from '../lib/hooks/usePortalDemandasDomain';
import { Box, Card, CardContent, Typography, Chip, Grid, Button, MenuItem, Select, InputLabel, FormControl } from '@mui/material';
import { Link as RouterLink } from 'react-router-dom';
import { IAAnalysisButton } from './IAAnalysisButton';
import { Business, Groups, Gavel, TaskAlt, CheckCircle, Info } from '@mui/icons-material';

  // EmpresasList
  const [empresaModal, setEmpresaModal] = useState<any | null>(null);
  const empresas = useEmpresas();
  const [buscaEmpresas, setBuscaEmpresas] = useState('');
  const [ordemEmpresas, setOrdemEmpresas] = useState<'nome' | 'criado_em'>('nome');
  let empresasFiltradas = empresas.filter(e => e.nome.toLowerCase().includes(buscaEmpresas.toLowerCase()));
  empresasFiltradas = empresasFiltradas.sort((a, b) => {
    if (ordemEmpresas === 'nome') return a.nome.localeCompare(b.nome);
    if (ordemEmpresas === 'criado_em') return (new Date(b.criado_em || 0).getTime()) - (new Date(a.criado_em || 0).getTime());
    return 0;
  });
  if (!empresas.length) return <div>Nenhuma empresa cadastrada.</div>;
  return (
    <Box>
      <Typography variant="h5" fontWeight={700} mb={2}>Empresas</Typography>
      <Box mb={2} display="flex" gap={2} alignItems="center">
        <input
          type="text"
          placeholder="Buscar por nome..."
          value={buscaEmpresas}
          onChange={e => setBuscaEmpresas(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: '100%', maxWidth: 320 }}
        />
        <FormControl size="small" sx={{ minWidth: 160 }}>
          <InputLabel id="ordem-empresas-label">Ordenar por</InputLabel>
          <Select
            labelId="ordem-empresas-label"
            value={ordemEmpresas}
            label="Ordenar por"
            onChange={e => setOrdemEmpresas(e.target.value as 'nome' | 'criado_em')}
          >
            <MenuItem value="nome">Nome (A-Z)</MenuItem>
            <MenuItem value="criado_em">Data de Criação (Mais recente)</MenuItem>
          </Select>
        </FormControl>
      </Box>
      <Grid container spacing={2}>
        {empresasFiltradas.map(e => (
          <Grid item xs={12} sm={6} md={4} key={e.id}>
            <Card sx={{ borderRadius: 2, boxShadow: 2, mb: 2 }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Chip icon={<Business />} label={`ID: ${e.id}`} size="small" />
                  {e.sindicato_id && <Chip icon={<Groups />} label={`Sindicato: ${e.sindicato_id}`} size="small" />}
                </Box>
                <Typography variant="h6" fontWeight={600}>{e.nome}</Typography>
                <Typography variant="body2" color="text.secondary">Criada em: {e.criado_em ? new Date(e.criado_em).toLocaleDateString() : '-'}</Typography>
                <Box mt={2} display="flex" justifyContent="flex-end" gap={1}>
                  <Button
                    size="small"
                    variant="contained"
                    color="secondary"
                    onClick={() => {
                      setEmpresaEdit(e);
                      setEmpresaEditValues({ nome: e.nome, sindicato_id: e.sindicato_id });
                    }}
                  >
                    Editar
                  </Button>
      {/* Modal de edição rápida Empresa */}
      <Dialog open={!!empresaEdit} onClose={() => setEmpresaEdit(null)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Editar Empresa
          <IconButton aria-label="close" onClick={() => setEmpresaEdit(null)} sx={{ position: 'absolute', right: 8, top: 8 }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {empresaEdit && (
            <Box display="flex" flexDirection="column" gap={2}>
              <TextField label="Nome" value={empresaEditValues.nome || ''} onChange={e => setEmpresaEditValues((v: any) => ({ ...v, nome: e.target.value }))} fullWidth />
              <TextField label="Sindicato ID" value={empresaEditValues.sindicato_id || ''} onChange={e => setEmpresaEditValues((v: any) => ({ ...v, sindicato_id: e.target.value }))} fullWidth />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEmpresaEdit(null)}>Cancelar</Button>
          <Button variant="contained" onClick={() => { setEmpresaEdit(mockUpdate(empresaEdit, empresaEditValues)); setEmpresaEdit(null); }}>Salvar</Button>
        </DialogActions>
      </Dialog>
  const [sindicatoEdit, setSindicatoEdit] = useState<any | null>(null);
  const [sindicatoEditValues, setSindicatoEditValues] = useState<any>({});
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => setEmpresaModal(e)}
                  >
                    Visualizar
                  </Button>
                  <Button
                    size="small"
                    variant="outlined"
                    component={RouterLink}
                    to={`/demandas/empresa/${e.id}`}
                  >
                    Detalhes
                  </Button>
                  <IAAnalysisButton context={`Empresa: ${e.nome} (ID: ${e.id})`} />
                </Box>
      {/* Modal de detalhe rápido Empresa */}
      <Dialog open={!!empresaModal} onClose={() => setEmpresaModal(null)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Detalhes da Empresa
          <IconButton aria-label="close" onClick={() => setEmpresaModal(null)} sx={{ position: 'absolute', right: 8, top: 8 }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {empresaModal && (
            <Box>
              <Typography variant="h6">{empresaModal.nome}</Typography>
              <Typography>ID: {empresaModal.id}</Typography>
              <Typography>Sindicato: {empresaModal.sindicato_id || '-'}</Typography>
              <Typography>Criada em: {empresaModal.criado_em ? new Date(empresaModal.criado_em).toLocaleDateString() : '-'}</Typography>
              {/* Adicione outros campos relevantes */}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setEmpresaModal(null)}>Fechar</Button>
        </DialogActions>
      </Dialog>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

  // SindicatosList
  const [sindicatoModal, setSindicatoModal] = useState<any | null>(null);
  const sindicatos = useSindicatos();
  const [buscaSindicatos, setBuscaSindicatos] = useState('');
  const [ordemSindicatos, setOrdemSindicatos] = useState<'nome' | 'id'>('nome');
  let sindicatosFiltrados = sindicatos.filter(s => s.nome_sindicato.toLowerCase().includes(buscaSindicatos.toLowerCase()));
  sindicatosFiltrados = sindicatosFiltrados.sort((a, b) => {
    if (ordemSindicatos === 'nome') return a.nome_sindicato.localeCompare(b.nome_sindicato);
    if (ordemSindicatos === 'id') return a.id - b.id;
    return 0;
  });
  if (!sindicatos.length) return <div>Nenhum sindicato cadastrado.</div>;
  return (
    <Box>
      <Typography variant="h5" fontWeight={700} mb={2}>Sindicatos</Typography>
      <Box mb={2} display="flex" gap={2} alignItems="center">
        <input
          type="text"
          placeholder="Buscar por nome..."
          value={buscaSindicatos}
          onChange={e => setBuscaSindicatos(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: '100%', maxWidth: 320 }}
        />
        <FormControl size="small" sx={{ minWidth: 160 }}>
          <InputLabel id="ordem-sindicatos-label">Ordenar por</InputLabel>
          <Select
            labelId="ordem-sindicatos-label"
            value={ordemSindicatos}
            label="Ordenar por"
            onChange={e => setOrdemSindicatos(e.target.value as 'nome' | 'id')}
          >
            <MenuItem value="nome">Nome (A-Z)</MenuItem>
            <MenuItem value="id">ID (Crescente)</MenuItem>
          </Select>
        </FormControl>
      </Box>
      <Grid container spacing={2}>
        {sindicatosFiltrados.map(s => (
          <Grid item xs={12} sm={6} md={4} key={s.id}>
            <Card sx={{ borderRadius: 2, boxShadow: 2, mb: 2 }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Chip icon={<Groups />} label={`ID: ${s.id}`} size="small" />
                  {s.cnpj && <Chip icon={<Info />} label={`CNPJ: ${s.cnpj}`} size="small" />}
                </Box>
                <Typography variant="h6" fontWeight={600}>{s.nome_sindicato}</Typography>
                <Typography variant="body2" color="text.secondary">Base: {s.base_territorial || '-'}</Typography>
                <Typography variant="body2" color="text.secondary">Categoria: {s.categoria_representada || '-'}</Typography>
                <Box mt={2} display="flex" justifyContent="flex-end" gap={1}>
                  <Button
                    size="small"
                    variant="contained"
                    color="secondary"
                    onClick={() => {
                      setSindicatoEdit(s);
                      setSindicatoEditValues({ nome_sindicato: s.nome_sindicato, cnpj: s.cnpj });
                    }}
                  >
                    Editar
                  </Button>
      {/* Modal de edição rápida Sindicato */}
      <Dialog open={!!sindicatoEdit} onClose={() => setSindicatoEdit(null)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Editar Sindicato
          <IconButton aria-label="close" onClick={() => setSindicatoEdit(null)} sx={{ position: 'absolute', right: 8, top: 8 }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {sindicatoEdit && (
            <Box display="flex" flexDirection="column" gap={2}>
              <TextField label="Nome do Sindicato" value={sindicatoEditValues.nome_sindicato || ''} onChange={e => setSindicatoEditValues((v: any) => ({ ...v, nome_sindicato: e.target.value }))} fullWidth />
              <TextField label="CNPJ" value={sindicatoEditValues.cnpj || ''} onChange={e => setSindicatoEditValues((v: any) => ({ ...v, cnpj: e.target.value }))} fullWidth />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSindicatoEdit(null)}>Cancelar</Button>
          <Button variant="contained" onClick={() => { setSindicatoEdit(mockUpdate(sindicatoEdit, sindicatoEditValues)); setSindicatoEdit(null); }}>Salvar</Button>
        </DialogActions>
      </Dialog>
  const [cctEdit, setCctEdit] = useState<any | null>(null);
  const [cctEditValues, setCctEditValues] = useState<any>({});
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => setSindicatoModal(s)}
                  >
                    Visualizar
                  </Button>
                  <Button
                    size="small"
                    variant="outlined"
                    component={RouterLink}
                    to={`/demandas/sindicato/${s.id}`}
                  >
                    Detalhes
                  </Button>
                  <IAAnalysisButton context={`Sindicato: ${s.nome_sindicato} (ID: ${s.id})`} />
                </Box>
      {/* Modal de detalhe rápido Sindicato */}
      <Dialog open={!!sindicatoModal} onClose={() => setSindicatoModal(null)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Detalhes do Sindicato
          <IconButton aria-label="close" onClick={() => setSindicatoModal(null)} sx={{ position: 'absolute', right: 8, top: 8 }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {sindicatoModal && (
            <Box>
              <Typography variant="h6">{sindicatoModal.nome_sindicato}</Typography>
              <Typography>ID: {sindicatoModal.id}</Typography>
              <Typography>CNPJ: {sindicatoModal.cnpj || '-'}</Typography>
              <Typography>Base: {sindicatoModal.base_territorial || '-'}</Typography>
              <Typography>Categoria: {sindicatoModal.categoria_representada || '-'}</Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setSindicatoModal(null)}>Fechar</Button>
        </DialogActions>
      </Dialog>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

  // CCTsList
  const [cctModal, setCctModal] = useState<any | null>(null);
  const ccts = useCCTs();
  const [buscaCCTs, setBuscaCCTs] = useState('');
  const [ordemCCTs, setOrdemCCTs] = useState<'registro' | 'vigencia_inicio'>('registro');
  let cctsFiltradas = ccts.filter(cct => cct.numero_registro_mte.toLowerCase().includes(buscaCCTs.toLowerCase()));
  cctsFiltradas = cctsFiltradas.sort((a, b) => {
    if (ordemCCTs === 'registro') return a.numero_registro_mte.localeCompare(b.numero_registro_mte);
    if (ordemCCTs === 'vigencia_inicio') return new Date(b.vigencia_inicio).getTime() - new Date(a.vigencia_inicio).getTime();
    return 0;
  });
  if (!ccts.length) return <div>Nenhuma CCT cadastrada.</div>;
  return (
    <Box>
      <Typography variant="h5" fontWeight={700} mb={2}>Convenções Coletivas (CCTs)</Typography>
      <Box mb={2} display="flex" gap={2} alignItems="center">
        <input
          type="text"
          placeholder="Buscar por registro MTE..."
          value={buscaCCTs}
          onChange={e => setBuscaCCTs(e.target.value)}
          style={{ padding: 8, borderRadius: 4, border: '1px solid #ccc', width: '100%', maxWidth: 320 }}
        />
        <FormControl size="small" sx={{ minWidth: 180 }}>
          <InputLabel id="ordem-ccts-label">Ordenar por</InputLabel>
          <Select
            labelId="ordem-ccts-label"
            value={ordemCCTs}
            label="Ordenar por"
            onChange={e => setOrdemCCTs(e.target.value as 'registro' | 'vigencia_inicio')}
          >
            <MenuItem value="registro">Registro MTE (A-Z)</MenuItem>
            <MenuItem value="vigencia_inicio">Vigência (Mais recente)</MenuItem>
          </Select>
        </FormControl>
      </Box>
      <Grid container spacing={2}>
        {cctsFiltradas.map(cct => (
          <Grid item xs={12} sm={6} md={4} key={cct.id}>
            <Card sx={{ borderRadius: 2, boxShadow: 2, mb: 2 }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Chip icon={<Gavel />} label={`Registro: ${cct.numero_registro_mte}`} size="small" />
                  <Chip label={`Sindicato: ${cct.sindicato_id}`} size="small" />
                </Box>
                <Typography variant="body2" color="text.secondary">Vigência: {cct.vigencia_inicio} a {cct.vigencia_fim}</Typography>
                <Box mt={2} display="flex" justifyContent="flex-end" gap={1}>
                  <Button
                    size="small"
                    variant="contained"
                    color="secondary"
                    onClick={() => {
                      setCctEdit(cct);
                      setCctEditValues({ numero_registro_mte: cct.numero_registro_mte, sindicato_id: cct.sindicato_id });
                    }}
                  >
                    Editar
                  </Button>
      {/* Modal de edição rápida CCT */}
      <Dialog open={!!cctEdit} onClose={() => setCctEdit(null)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Editar CCT
          <IconButton aria-label="close" onClick={() => setCctEdit(null)} sx={{ position: 'absolute', right: 8, top: 8 }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {cctEdit && (
            <Box display="flex" flexDirection="column" gap={2}>
              <TextField label="Registro MTE" value={cctEditValues.numero_registro_mte || ''} onChange={e => setCctEditValues((v: any) => ({ ...v, numero_registro_mte: e.target.value }))} fullWidth />
              <TextField label="Sindicato ID" value={cctEditValues.sindicato_id || ''} onChange={e => setCctEditValues((v: any) => ({ ...v, sindicato_id: e.target.value }))} fullWidth />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCctEdit(null)}>Cancelar</Button>
          <Button variant="contained" onClick={() => { setCctEdit(mockUpdate(cctEdit, cctEditValues)); setCctEdit(null); }}>Salvar</Button>
        </DialogActions>
      </Dialog>
  const [tarefaEdit, setTarefaEdit] = useState<any | null>(null);
  const [tarefaEditValues, setTarefaEditValues] = useState<any>({});
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => setCctModal(cct)}
                  >
                    Visualizar
                  </Button>
                  <Button
                    size="small"
                    variant="outlined"
                    component={RouterLink}
                    to={`/demandas/cct/${cct.id}`}
                  >
                    Detalhes
                  </Button>
                  <IAAnalysisButton context={`CCT: ${cct.numero_registro_mte} (ID: ${cct.id})`} />
                </Box>
      {/* Modal de detalhe rápido CCT */}
      <Dialog open={!!cctModal} onClose={() => setCctModal(null)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Detalhes da CCT
          <IconButton aria-label="close" onClick={() => setCctModal(null)} sx={{ position: 'absolute', right: 8, top: 8 }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {cctModal && (
            <Box>
              <Typography variant="h6">Registro: {cctModal.numero_registro_mte}</Typography>
              <Typography>ID: {cctModal.id}</Typography>
              <Typography>Sindicato: {cctModal.sindicato_id}</Typography>
              <Typography>Vigência: {cctModal.vigencia_inicio} a {cctModal.vigencia_fim}</Typography>
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setCctModal(null)}>Fechar</Button>
        </DialogActions>
      </Dialog>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};

  // TarefasList
  const [tarefaModal, setTarefaModal] = useState<any | null>(null);
  const tarefas = useTarefas();
  const [filtroTarefas, setFiltroTarefas] = useState<'todas' | 'pendentes' | 'concluidas'>('todas');
  const [ordemTarefas, setOrdemTarefas] = useState<'nome' | 'data' | 'status'>('nome');
  let tarefasFiltradas = tarefas;
  if (filtroTarefas === 'pendentes') tarefasFiltradas = tarefas.filter(t => !t.concluido);
  if (filtroTarefas === 'concluidas') tarefasFiltradas = tarefas.filter(t => t.concluido);
  tarefasFiltradas = tarefasFiltradas.sort((a, b) => {
    if (ordemTarefas === 'nome') return a.nome_tarefa.localeCompare(b.nome_tarefa);
    if (ordemTarefas === 'data') {
      const dataA = a.data_conclusao ? new Date(a.data_conclusao).getTime() : 0;
      const dataB = b.data_conclusao ? new Date(b.data_conclusao).getTime() : 0;
      return dataB - dataA;
    }
    if (ordemTarefas === 'status') return (a.concluido === b.concluido) ? 0 : a.concluido ? 1 : -1;
    return 0;
  });
  if (!tarefas.length) return <div>Nenhuma tarefa encontrada.</div>;
  const pendentes = tarefas.filter(t => !t.concluido).length;
  return (
    <Box>
      <Box display="flex" alignItems="center" gap={1} mb={2}>
        <Typography variant="h5" fontWeight={700}>Tarefas</Typography>
        {pendentes > 0 && <Chip label={`${pendentes} pendente${pendentes > 1 ? 's' : ''}`} color="warning" size="small" />}
      </Box>
      <Box mb={2} display="flex" gap={2} alignItems="center">
        <Button variant={filtroTarefas === 'todas' ? 'contained' : 'outlined'} onClick={() => setFiltroTarefas('todas')}>Todas</Button>
        <Button variant={filtroTarefas === 'pendentes' ? 'contained' : 'outlined'} color="warning" onClick={() => setFiltroTarefas('pendentes')}>Pendentes</Button>
        <Button variant={filtroTarefas === 'concluidas' ? 'contained' : 'outlined'} color="success" onClick={() => setFiltroTarefas('concluidas')}>Concluídas</Button>
        <FormControl size="small" sx={{ minWidth: 160 }}>
          <InputLabel id="ordem-tarefas-label">Ordenar por</InputLabel>
          <Select
            labelId="ordem-tarefas-label"
            value={ordemTarefas}
            label="Ordenar por"
            onChange={e => setOrdemTarefas(e.target.value as 'nome' | 'data' | 'status')}
          >
            <MenuItem value="nome">Nome (A-Z)</MenuItem>
            <MenuItem value="data">Data de Conclusão (Mais recente)</MenuItem>
            <MenuItem value="status">Status (Pendentes primeiro)</MenuItem>
          </Select>
        </FormControl>
      </Box>
      <Grid container spacing={2}>
        {tarefasFiltradas.map(t => (
          <Grid item xs={12} sm={6} md={4} key={t.id}>
            <Card sx={{ borderRadius: 2, boxShadow: 2, mb: 2, background: t.concluido ? '#e8f5e9' : '#fff' }}>
              <CardContent>
                <Box display="flex" alignItems="center" gap={1} mb={1}>
                  <Chip icon={<TaskAlt />} label={`ID: ${t.id}`} size="small" />
                  {!t.concluido && <Chip label="Pendente" color="warning" size="small" />}
                  {t.concluido && <Chip icon={<CheckCircle />} label="Concluída" color="success" size="small" />}
                </Box>
                <Typography variant="h6" fontWeight={600} sx={{ textDecoration: t.concluido ? 'line-through' : 'none' }}>{t.nome_tarefa}</Typography>
                {t.data_conclusao && <Typography variant="body2" color="text.secondary">Concluída em: {new Date(t.data_conclusao).toLocaleDateString()}</Typography>}
                <Box mt={2} display="flex" justifyContent="flex-end" gap={1}>
                  <Button
                    size="small"
                    variant="contained"
                    color="secondary"
                    onClick={() => {
                      setTarefaEdit(t);
                      setTarefaEditValues({ nome_tarefa: t.nome_tarefa });
                    }}
                  >
                    Editar
                  </Button>
      {/* Modal de edição rápida Tarefa */}
      <Dialog open={!!tarefaEdit} onClose={() => setTarefaEdit(null)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Editar Tarefa
          <IconButton aria-label="close" onClick={() => setTarefaEdit(null)} sx={{ position: 'absolute', right: 8, top: 8 }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {tarefaEdit && (
            <Box display="flex" flexDirection="column" gap={2}>
              <TextField label="Nome da Tarefa" value={tarefaEditValues.nome_tarefa || ''} onChange={e => setTarefaEditValues((v: any) => ({ ...v, nome_tarefa: e.target.value }))} fullWidth />
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTarefaEdit(null)}>Cancelar</Button>
          <Button variant="contained" onClick={() => { setTarefaEdit(mockUpdate(tarefaEdit, tarefaEditValues)); setTarefaEdit(null); }}>Salvar</Button>
        </DialogActions>
      </Dialog>
                  <Button
                    size="small"
                    variant="outlined"
                    onClick={() => setTarefaModal(t)}
                  >
                    Visualizar
                  </Button>
                  <Button
                    size="small"
                    variant="outlined"
                    component={RouterLink}
                    to={`/demandas/tarefa/${t.id}`}
                  >
                    Detalhes
                  </Button>
                  <IAAnalysisButton context={`Tarefa: ${t.nome_tarefa} (ID: ${t.id})`} />
                </Box>
      {/* Modal de detalhe rápido Tarefa */}
      <Dialog open={!!tarefaModal} onClose={() => setTarefaModal(null)} maxWidth="sm" fullWidth>
        <DialogTitle>
          Detalhes da Tarefa
          <IconButton aria-label="close" onClick={() => setTarefaModal(null)} sx={{ position: 'absolute', right: 8, top: 8 }}>
            <CloseIcon />
          </IconButton>
        </DialogTitle>
        <DialogContent dividers>
          {tarefaModal && (
            <Box>
              <Typography variant="h6">{tarefaModal.nome_tarefa}</Typography>
              <Typography>ID: {tarefaModal.id}</Typography>
              <Typography>Status: {tarefaModal.concluido ? 'Concluída' : 'Pendente'}</Typography>
              {tarefaModal.data_conclusao && <Typography>Concluída em: {new Date(tarefaModal.data_conclusao).toLocaleDateString()}</Typography>}
            </Box>
          )}
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setTarefaModal(null)}>Fechar</Button>
        </DialogActions>
      </Dialog>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Box>
  );
};
