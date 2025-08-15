import { useEffect, useState } from 'react';
import { Auditoria, Relatorio, Upload } from '../portalDemandasTypes';
import { portalDemandasAuditoriaService } from '../portalDemandasAuditoriaService';

export function useAuditorias() {
  const [auditorias, setAuditorias] = useState<Auditoria[]>([]);
  useEffect(() => { portalDemandasAuditoriaService.listarAuditorias().then(setAuditorias); }, []);
  return auditorias;
}

export function useRelatorios() {
  const [relatorios, setRelatorios] = useState<Relatorio[]>([]);
  useEffect(() => { portalDemandasAuditoriaService.listarRelatorios().then(setRelatorios); }, []);
  return relatorios;
}

export function useUploads() {
  const [uploads, setUploads] = useState<Upload[]>([]);
  useEffect(() => { portalDemandasAuditoriaService.listarUploads().then(setUploads); }, []);
  return uploads;
}
