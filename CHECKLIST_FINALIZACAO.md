# ✅ AUDITORIA360 - Checklist de Finalização

> **Lista de verificação baseada no [Relatório Unificado Final](docs/RELATORIO_UNIFICADO_FINAL.md)**

## 🚨 Crítico - Próximos 7 dias

### Cobertura de Testes (75% → 85%)
- [ ] Implementar testes para `src/services/ml/components/` (0% cobertura)
- [ ] Expandir testes de `src/api/routers/compliance.py` (40% cobertura)
- [ ] Criar testes para `src/models/audit_models.py` (50% cobertura) 
- [ ] Implementar testes de integração para `services/ocr/paddle_service.py` (60% cobertura)
- [ ] Executar `pytest --cov=src --cov-fail-under=85` e verificar aprovação

### Limpeza de Arquivos Órfãos
- [ ] Remover `scripts/exemplo_*.py` (15 arquivos)
- [ ] Limpar `automation/legacy_*.py` (8 arquivos)
- [ ] Deletar `backups/temp_*` (12 arquivos)
- [ ] Consolidar `configs/old_*.json` (7 arquivos)
- [ ] Verificar que aplicação continua funcionando após limpeza

## 📅 Alto - Próximos 14 dias

### Deploy Dashboards Streamlit
- [ ] Configurar `vercel.json` para build do Streamlit
- [ ] Implementar variáveis de ambiente para produção dashboards
- [ ] Testar integração dashboards + API FastAPI em produção
- [ ] Configurar domínio/subdomínio para acesso

### Migração Automação Serverless
- [ ] Converter `automation/rpa_folha.py` → GitHub Actions workflow
- [ ] Migrar `automation/schedule_reports.py` → Vercel Cron Jobs
- [ ] Implementar `automation/backup_routine.py` → Cloudflare Workers
- [ ] Testar automação end-to-end completa

## 📊 Médio - Próximos 30 dias

### Consolidação de Duplicações
- [ ] Centralizar funções `get_api_token()` de 4 arquivos
- [ ] Criar base class para métodos `__repr__` de 8 models
- [ ] Unificar configurações de database em 3 locais
- [ ] Implementar imports centralizados

### Otimização de Performance
- [ ] Implementar cache Redis para `/api/v1/auditorias/relatorio` (3.2s → <1s)
- [ ] Otimizar queries DuckDB para `/api/v1/compliance/check` (2.8s → <1s) 
- [ ] Adicionar paginação para `/stats/` portal_demandas (1.5s → <0.5s)
- [ ] Implementar lazy loading onde aplicável

## 🎯 Critérios de Sucesso Final

### ✅ Métricas de Conclusão
- [ ] **Cobertura de testes**: ≥85% (atual: ~75%)
- [ ] **Arquivos órfãos**: ≤10 (atual: ~82)
- [ ] **Duplicações críticas**: 0 (atual: 12)
- [ ] **Performance API**: <1s (alguns endpoints >2s)
- [ ] **Dashboards deployados**: 100% (atual: 0%)
- [ ] **Automação serverless**: 100% (atual: 30%)

### 🔍 Verificação Final
Para validar conclusão total:
```bash
# 1. Executar verificador automático
python scripts/verificar_progresso.py

# 2. Testes com cobertura
pytest --cov=src --cov-fail-under=85

# 3. Verificar builds sem erro
python -m py_compile src/**/*.py

# 4. Testar API endpoints
curl http://localhost:8000/health
curl http://localhost:8001/health

# 5. Verificar dashboards (quando deployados)
curl https://dashboards.auditoria360.com.br/health
```

## 📝 Comandos Úteis

### Verificação de Progresso
```bash
# Status geral
python scripts/verificar_progresso.py

# Cobertura detalhada
pytest --cov=src --cov-report=html

# Encontrar arquivos órfãos
find . -name "exemplo_*.py" -o -name "legacy_*.py" -o -name "temp_*"

# Verificar duplicações
grep -r "get_api_token" src/ --include="*.py"
```

### Limpeza Segura
```bash
# Backup antes de limpar
git add . && git commit -m "Backup antes da limpeza"

# Remover órfãos (CUIDADO!)
rm scripts/exemplo_*.py
rm automation/legacy_*.py  
rm backups/temp_*

# Verificar se nada quebrou
python -m pytest
```

---

**Atualizado em**: 28 de Janeiro de 2025  
**Progresso atual**: 85% concluído  
**Estimativa para 100%**: 4 semanas  

> Marque os itens concluídos e execute `python scripts/verificar_progresso.py` para verificar o progresso automaticamente.