# 🚨 AUDITORIA360 - Alerta do Sistema

**{{alert_type}}**

---

## 📋 Detalhes do Alerta

- **Módulo:** {{module_name}}
- **Status:** {{status}}
- **Severidade:** {{severity}}
- **Timestamp:** {{timestamp}}
- **Detalhes:** {{details}}

{{#action_required}}
## 🎯 Ação Requerida

{{action_required}}
{{/action_required}}

{{#recommendations}}
## 💡 Recomendações

{{#items}}
- {{.}}
{{/items}}
{{/recommendations}}

---

## 🔗 Links Úteis

- [📊 Dashboard de Status]({{dashboard_url}})
- [📈 Métricas do Sistema]({{dashboard_url}}/metrics)
- [🔍 Logs Detalhados]({{dashboard_url}}/logs)

---

*Alerta automático do Sistema de Monitoramento AUDITORIA360*
*Gerado em {{generation_time}}*