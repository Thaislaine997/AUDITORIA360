import React, { useEffect, useState } from 'react';
import { getBadges, getIncidentes, getMetrics, getRelatoriosAgendados, getSecurityAudit, getStatus, getComunicados } from '../services/automationApi';

const AutomationDashboard: React.FC = () => {
  const [badges, setBadges] = useState<any[]>([]);
  const [incidentes, setIncidentes] = useState<any[]>([]);
  const [metrics, setMetrics] = useState<any>(null);
  const [relatorios, setRelatorios] = useState<any[]>([]);
  const [securityAudit, setSecurityAudit] = useState<any>(null);
  const [status, setStatus] = useState<any>(null);
  const [comunicados, setComunicados] = useState<any[]>([]);

  useEffect(() => {
    getBadges().then(setBadges);
    getIncidentes().then(setIncidentes);
    getMetrics().then(setMetrics);
    getRelatoriosAgendados().then(setRelatorios);
    getSecurityAudit().then(setSecurityAudit);
    getStatus().then(setStatus);
    getComunicados().then(setComunicados);
  }, []);

  return (
    <div>
      <h2>Dashboard de Automação</h2>
      <section>
        <h3>Status e Badges</h3>
        <div>{badges && badges.map((b, i) => <span key={i}>{b.label}: {b.value} </span>)}</div>
      </section>
      <section>
        <h3>Incidentes Recentes</h3>
        <ul>{incidentes && incidentes.map((inc, i) => <li key={i}>{inc.titulo || inc.title}</li>)}</ul>
      </section>
      <section>
        <h3>Métricas do Sistema</h3>
        <pre>{metrics && JSON.stringify(metrics, null, 2)}</pre>
      </section>
      <section>
        <h3>Relatórios Agendados</h3>
        <ul>{relatorios && relatorios.map((r, i) => <li key={i}>{r.nome || r.name}</li>)}</ul>
      </section>
      <section>
        <h3>Auditoria de Segurança</h3>
        <pre>{securityAudit && JSON.stringify(securityAudit, null, 2)}</pre>
      </section>
      <section>
        <h3>Status do Sistema</h3>
        <pre>{status && JSON.stringify(status, null, 2)}</pre>
      </section>
      <section>
        <h3>Comunicados</h3>
        <ul>{comunicados && comunicados.map((c, i) => <li key={i}>{c.titulo || c.title}</li>)}</ul>
      </section>
    </div>
  );
};

export default AutomationDashboard;
