import api from './api';

// Serviços para consumir endpoints de automação

export const getBadges = async () => {
  const { data } = await api.get('/status/badges');
  return data;
};

export const getIncidentes = async () => {
  const { data } = await api.get('/incidentes');
  return data;
};

export const getMetrics = async () => {
  const { data } = await api.get('/metrics');
  return data;
};

export const getRelatoriosAgendados = async () => {
  const { data } = await api.get('/relatorios/agendados');
  return data;
};

export const getSecurityAudit = async () => {
  const { data } = await api.get('/auditoria/seguranca');
  return data;
};

export const getStatus = async () => {
  const { data } = await api.get('/status');
  return data;
};

export const getComunicados = async () => {
  const { data } = await api.get('/comunicados');
  return data;
};
