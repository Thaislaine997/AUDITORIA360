import { useEffect, useState } from 'react';
import { Empresa, Sindicato, ConvencaoColetivaCCT, Tarefa } from '../portalDemandasTypes';
import { portalDemandasDomainService } from '../portalDemandasDomainService';

export function useEmpresas() {
  const [empresas, setEmpresas] = useState<Empresa[]>([]);
  useEffect(() => { portalDemandasDomainService.listarEmpresas().then(setEmpresas); }, []);
  return empresas;
}

export function useSindicatos() {
  const [sindicatos, setSindicatos] = useState<Sindicato[]>([]);
  useEffect(() => { portalDemandasDomainService.listarSindicatos().then(setSindicatos); }, []);
  return sindicatos;
}

export function useCCTs() {
  const [ccts, setCCTs] = useState<ConvencaoColetivaCCT[]>([]);
  useEffect(() => { portalDemandasDomainService.listarCCTs().then(setCCTs); }, []);
  return ccts;
}

export function useTarefas() {
  const [tarefas, setTarefas] = useState<Tarefa[]>([]);
  useEffect(() => { portalDemandasDomainService.listarTarefas().then(setTarefas); }, []);
  return tarefas;
}
