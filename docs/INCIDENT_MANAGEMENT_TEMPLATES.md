# AUDITORIA360 - Templates de Gerenciamento de Incidentes

## Template de Incident Report

```markdown
# 🚨 INCIDENT REPORT - [INCIDENT-ID]

## Informações Básicas
- **Data/Hora de Detecção:** [YYYY-MM-DD HH:MM UTC]
- **Severidade:** [P0-Critical | P1-High | P2-Medium | P3-Low]
- **Status:** [Investigando | Identificado | Corrigindo | Resolvido | Pós-Mortem]
- **Reporter:** [Nome/Email]
- **Responsible:** [Nome do Responsável pela Resolução]

## Resumo do Incidente
[Breve descrição do problema]

## Impacto
- **Usuários Afetados:** [Número/Percentual]
- **Módulos Afetados:** [Lista dos módulos]
- **Funcionalidades Impactadas:** [Lista das funcionalidades]
- **Clientes Críticos Afetados:** [Lista se houver]

## Timeline
- **[HH:MM]** - Incidente detectado
- **[HH:MM]** - Equipe notificada
- **[HH:MM]** - Investigação iniciada
- **[HH:MM]** - Causa identificada
- **[HH:MM]** - Correção aplicada
- **[HH:MM]** - Incidente resolvido

## Causa Raiz
[Descrição técnica da causa do problema]

## Resolução Aplicada
[Descrição das ações tomadas para resolver]

## Ações Preventivas
- [ ] [Ação 1] - Responsável: [Nome] - Prazo: [Data]
- [ ] [Ação 2] - Responsável: [Nome] - Prazo: [Data]
- [ ] [Ação 3] - Responsável: [Nome] - Prazo: [Data]

## Lições Aprendidas
[O que aprendemos com este incidente]

## Comunicações
- **Clientes Notificados:** [Sim/Não] - [Método]
- **Stakeholders Internos:** [Lista]
- **Canal de Comunicação:** [Slack/Email/Teams]

---
**Criado por:** [Nome]  
**Data:** [YYYY-MM-DD]
```

## Template de Comunicação Externa (Clientes)

```markdown
**Assunto:** AUDITORIA360 - Resolução de Incidente [INCIDENT-ID]

Prezado(a) Cliente,

Identificamos e resolvemos um incidente que afetou [MÓDULOS/FUNCIONALIDADES] do sistema AUDITORIA360.

**Resumo do Incidente:**
[Breve descrição não técnica]

**Período de Impacto:**
De [DATA/HORA] até [DATA/HORA] (Total: [X] horas)

**Funcionalidades Afetadas:**
- [Funcionalidade 1]
- [Funcionalidade 2]

**Status:** ✅ RESOLVIDO

**Ações Tomadas:**
- [Ação 1]
- [Ação 2]

**Prevenção Futura:**
- [Medida 1]
- [Medida 2]

Pedimos desculpas pelo inconveniente e agradecemos sua compreensão.

Para dúvidas, entre em contato: suporte@auditoria360.com

Atenciosamente,
Equipe AUDITORIA360
```

## Template de Comunicação Interna

```markdown
**🚨 INCIDENT ALERT - [SEVERITY]**

**Incident ID:** [INCIDENT-ID]
**Time:** [YYYY-MM-DD HH:MM UTC]
**Status:** [Status Atual]

**Affected Systems:**
- [Sistema 1]
- [Sistema 2]

**Impact:**
- Users affected: [Número]
- Business impact: [High/Medium/Low]

**Current Actions:**
- [Ação em andamento]

**Next Steps:**
- [Próxima ação]
- ETA: [Tempo estimado]

**War Room:** [Link/Canal]
**Incident Commander:** [Nome]

**Updates:** Will provide updates every 30 minutes until resolved.
```

## Severity Levels

### P0 - Critical
- **Definição:** Sistema completamente indisponível ou perda de dados
- **SLA Resposta:** 15 minutos
- **SLA Resolução:** 1 hora
- **Escalation:** Imediata para CTO
- **Comunicação:** Clientes em 30 minutos

### P1 - High  
- **Definição:** Funcionalidade crítica indisponível
- **SLA Resposta:** 30 minutos
- **SLA Resolução:** 4 horas
- **Escalation:** Tech Lead em 1 hora
- **Comunicação:** Clientes em 1 hora

### P2 - Medium
- **Definição:** Degradação de performance ou funcionalidade secundária
- **SLA Resposta:** 2 horas
- **SLA Resolução:** 8 horas
- **Escalation:** Não automática
- **Comunicação:** Clientes se solicitado

### P3 - Low
- **Definição:** Issues menores sem impacto crítico
- **SLA Resposta:** 24 horas
- **SLA Resolução:** 72 horas
- **Escalation:** Não necessária
- **Comunicação:** Release notes

## Processo de Escalation

### 0-15 minutos
- Suporte de plantão identifica e classifica
- Notifica on-call engineer
- Cria incident ticket

### 15-30 minutos
- Tech Lead assume comando
- War room estabelecida
- Primeira comunicação interna

### 30-60 minutos
- Se P0/P1: CTO notificado
- Comunicação externa se necessário
- Additional resources mobilized

### 1+ hora
- Regular updates (a cada 30 min para P0/P1)
- Stakeholder updates
- Documentation ongoing

## War Room Guidelines

### Participantes Obrigatórios
- **Incident Commander:** Tech Lead ou Senior Dev
- **Communications Lead:** PO ou Customer Success
- **Technical Lead:** Especialista no módulo afetado

### Participantes Opcionais
- DevOps Engineer
- QA Lead  
- Customer Support

### Regras da War Room
1. **Incident Commander** tem autoridade final
2. Updates a cada 15 minutos (P0) ou 30 minutos (P1)
3. Ações têm owner e deadline claros
4. Documentação em tempo real
5. Foco na resolução, blame depois

## Post-Mortem Process

### Quando Necessário
- Todos os incidentes P0 e P1
- P2 com impacto significativo
- Quando solicitado por stakeholders

### Timeline
- **24 horas:** Primeiro draft
- **72 horas:** Review e finalização
- **1 semana:** Implementação de ações

### Template Post-Mortem
```markdown
# Post-Mortem: [INCIDENT TITLE]

## Incident Summary
[O que aconteceu, quando, impacto]

## Timeline
[Timeline detalhado com horários precisos]

## Root Cause Analysis
[Causa raiz técnica detalhada]

## What Went Well
- [Item 1]
- [Item 2]

## What Went Wrong
- [Item 1] 
- [Item 2]

## Action Items
| Action | Owner | Due Date | Status |
|--------|-------|----------|--------|
| [Ação 1] | [Nome] | [Data] | [Status] |
| [Ação 2] | [Nome] | [Data] | [Status] |

## Lessons Learned
[Key takeaways]
```

---

**Criado:** 2025-08-11  
**Última Atualização:** 2025-08-11  
**Próxima Revisão:** 2025-11-11