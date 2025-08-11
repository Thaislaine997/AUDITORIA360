#!/bin/bash

# AUDITORIA360 - Production Deployment Script
# Script para deploy seguro em produção

set -e  # Exit on any error

echo "🚀 AUDITORIA360 - Deploy para Produção"
echo "===================================="

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[DEPLOY]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Configuration
BACKUP_DIR="backups/$(date +%Y%m%d_%H%M%S)"
HEALTH_CHECK_URL="${HEALTH_CHECK_URL:-http://localhost:8001/api/health/status}"
MAX_DEPLOYMENT_TIME=300  # 5 minutes max deployment time
ROLLBACK_ENABLED="${ROLLBACK_ENABLED:-true}"

# Create backup directory
mkdir -p "$BACKUP_DIR"

print_status "Iniciando processo de deploy..."
print_status "Backup será salvo em: $BACKUP_DIR"

# Step 1: Pre-deployment health check
print_status "=== 1. Verificação Pré-Deploy ==="
print_status "Executando health check pré-deploy..."

if ! python automation/update_status.py; then
    print_error "Health check pré-deploy falhou!"
    if [ "$ROLLBACK_ENABLED" = "true" ]; then
        print_warning "Deploy abortado devido a falhas no sistema"
        exit 1
    else
        print_warning "Prosseguindo com deploy apesar das falhas (ROLLBACK_ENABLED=false)"
    fi
else
    print_success "Health check pré-deploy aprovado ✓"
fi

# Check system metrics
if [ -f "automation/metrics_collector.py" ]; then
    print_status "Coletando métricas do sistema..."
    if python automation/metrics_collector.py; then
        print_success "Métricas coletadas ✓"
        # Save metrics to backup
        cp system_metrics_report.* "$BACKUP_DIR/" 2>/dev/null || true
    else
        print_warning "Falha na coleta de métricas (continuando deploy)"
    fi
fi

echo ""

# Step 2: Security audit
print_status "=== 2. Auditoria de Segurança ==="
if [ -f "automation/security_audit.py" ]; then
    print_status "Executando auditoria de segurança..."
    if python automation/security_audit.py; then
        print_success "Auditoria de segurança aprovada ✓"
        # Save security report to backup
        cp security_audit_report.* "$BACKUP_DIR/" 2>/dev/null || true
    else
        print_error "Auditoria de segurança falhou!"
        if [ "$ROLLBACK_ENABLED" = "true" ]; then
            print_error "Deploy abortado devido a falhas de segurança"
            exit 1
        else
            print_warning "Prosseguindo com deploy apesar das falhas de segurança"
        fi
    fi
else
    print_warning "Script de auditoria de segurança não encontrado"
fi

echo ""

# Step 3: Backup current state
print_status "=== 3. Backup do Estado Atual ==="
print_status "Criando backup dos arquivos críticos..."

# Backup critical files
CRITICAL_FILES=(
    ".env"
    "processos_status_auditoria360.md"
    "status_report_auditoria360.json"
    "incidents_log.json"
)

for file in "${CRITICAL_FILES[@]}"; do
    if [ -f "$file" ]; then
        cp "$file" "$BACKUP_DIR/"
        print_success "Backup de $file ✓"
    else
        print_warning "Arquivo $file não encontrado para backup"
    fi
done

# Backup configuration and logs
if [ -d "logs" ]; then
    cp -r logs "$BACKUP_DIR/" 2>/dev/null || true
    print_success "Backup dos logs ✓"
fi

if [ -d "config" ]; then
    cp -r config "$BACKUP_DIR/" 2>/dev/null || true
    print_success "Backup das configurações ✓"
fi

print_success "Backup completo em $BACKUP_DIR ✓"

echo ""

# Step 4: Build and test
print_status "=== 4. Build e Testes ==="

# Run tests
print_status "Executando bateria de testes..."
if [ -f "scripts/test_runner.sh" ]; then
    if bash scripts/test_runner.sh; then
        print_success "Todos os testes passaram ✓"
    else
        print_error "Alguns testes falharam!"
        if [ "$ROLLBACK_ENABLED" = "true" ]; then
            print_error "Deploy abortado devido a falhas nos testes"
            exit 1
        else
            print_warning "Prosseguindo com deploy apesar das falhas nos testes"
        fi
    fi
else
    print_warning "Script de testes não encontrado"
fi

# Build frontend if exists
if [ -d "src/frontend" ] && [ -f "src/frontend/package.json" ]; then
    print_status "Construindo frontend..."
    cd src/frontend
    if npm run build; then
        print_success "Frontend construído ✓"
    else
        print_error "Falha na construção do frontend"
        cd ../..
        exit 1
    fi
    cd ../..
fi

echo ""

# Step 5: Deploy application
print_status "=== 5. Deploy da Aplicação ==="
print_status "Iniciando deploy da aplicação..."

DEPLOY_START_TIME=$(date +%s)

# Here you would add your actual deployment logic
# Examples:
# - Docker build and push
# - Update Kubernetes deployments
# - Upload to cloud providers
# - Restart services

print_status "Simulando deploy da aplicação..."

# Simulate deployment steps
DEPLOY_STEPS=(
    "Construindo imagem Docker..."
    "Enviando para registry..."
    "Atualizando configuração de produção..."
    "Reiniciando serviços..."
    "Aguardando estabilização..."
)

for step in "${DEPLOY_STEPS[@]}"; do
    print_status "$step"
    sleep 2  # Simulate deployment time
    print_success "Concluído ✓"
done

DEPLOY_END_TIME=$(date +%s)
DEPLOY_DURATION=$((DEPLOY_END_TIME - DEPLOY_START_TIME))

print_success "Deploy da aplicação concluído em ${DEPLOY_DURATION}s ✓"

echo ""

# Step 6: Post-deployment verification
print_status "=== 6. Verificação Pós-Deploy ==="
print_status "Aguardando estabilização do sistema..."
sleep 10

# Health check with retry logic
print_status "Executando health check pós-deploy..."
HEALTH_CHECK_ATTEMPTS=0
MAX_HEALTH_CHECK_ATTEMPTS=5
HEALTH_CHECK_PASSED=false

while [ $HEALTH_CHECK_ATTEMPTS -lt $MAX_HEALTH_CHECK_ATTEMPTS ] && [ "$HEALTH_CHECK_PASSED" = false ]; do
    ((HEALTH_CHECK_ATTEMPTS++))
    print_status "Tentativa de health check $HEALTH_CHECK_ATTEMPTS/$MAX_HEALTH_CHECK_ATTEMPTS"
    
    if python automation/update_status.py; then
        print_success "Health check pós-deploy aprovado ✓"
        HEALTH_CHECK_PASSED=true
    else
        print_warning "Health check falhou (tentativa $HEALTH_CHECK_ATTEMPTS)"
        if [ $HEALTH_CHECK_ATTEMPTS -lt $MAX_HEALTH_CHECK_ATTEMPTS ]; then
            print_status "Aguardando 30s antes da próxima tentativa..."
            sleep 30
        fi
    fi
done

if [ "$HEALTH_CHECK_PASSED" = false ]; then
    print_error "Health check pós-deploy falhou após $MAX_HEALTH_CHECK_ATTEMPTS tentativas!"
    
    if [ "$ROLLBACK_ENABLED" = "true" ]; then
        print_error "Iniciando rollback..."
        # Here you would implement rollback logic
        print_warning "ROLLBACK NÃO IMPLEMENTADO - INTERVENÇÃO MANUAL NECESSÁRIA"
        exit 1
    else
        print_warning "Rollback desabilitado - sistema pode estar instável"
    fi
fi

# API endpoint check (if applicable)
if command -v curl &> /dev/null; then
    print_status "Testando endpoints da API..."
    if curl -s "$HEALTH_CHECK_URL" >/dev/null 2>&1; then
        print_success "API respondendo corretamente ✓"
    else
        print_warning "API não está respondendo em $HEALTH_CHECK_URL"
    fi
fi

echo ""

# Step 7: Final verification and monitoring setup
print_status "=== 7. Verificação Final e Monitoramento ==="

# Update monitoring
print_status "Atualizando configuração de monitoramento..."
if python automation/metrics_collector.py; then
    print_success "Métricas pós-deploy coletadas ✓"
fi

# Create deployment record
DEPLOYMENT_RECORD="deployments/deployment_$(date +%Y%m%d_%H%M%S).json"
mkdir -p deployments

cat > "$DEPLOYMENT_RECORD" << EOF
{
    "deployment_id": "deploy_$(date +%Y%m%d_%H%M%S)",
    "timestamp": "$(date -Iseconds)",
    "duration_seconds": $DEPLOY_DURATION,
    "backup_location": "$BACKUP_DIR",
    "health_check_passed": $HEALTH_CHECK_PASSED,
    "rollback_enabled": $ROLLBACK_ENABLED,
    "version": "$(git rev-parse HEAD 2>/dev/null || echo 'unknown')",
    "environment": "production",
    "deployed_by": "$(whoami)",
    "status": "$([ "$HEALTH_CHECK_PASSED" = true ] && echo 'success' || echo 'failed')"
}
EOF

print_success "Registro de deployment criado: $DEPLOYMENT_RECORD"

echo ""

# Final summary
echo "=========================================="
print_success "🎉 DEPLOY CONCLUÍDO COM SUCESSO!"
echo "=========================================="
echo ""
echo "📊 Resumo do Deploy:"
echo "   🕒 Duração total: ${DEPLOY_DURATION}s"
echo "   📁 Backup: $BACKUP_DIR"
echo "   🏥 Health check: $([ "$HEALTH_CHECK_PASSED" = true ] && echo '✅ Passou' || echo '❌ Falhou')"
echo "   📋 Registro: $DEPLOYMENT_RECORD"
echo ""
echo "🔗 Links úteis:"
echo "   📊 Dashboard: ${HEALTH_CHECK_URL%/api/health/status}"
echo "   🏥 Health Status: $HEALTH_CHECK_URL"
echo "   📈 Métricas: ${HEALTH_CHECK_URL%/api/health/status}/metrics"
echo ""
echo "📝 Próximos passos:"
echo "   1. Monitorar logs por 30 minutos"
echo "   2. Verificar métricas de performance"
echo "   3. Confirmar funcionalidades críticas"
echo "   4. Notificar stakeholders sobre deploy"
echo ""

# Create post-deployment checklist
POST_DEPLOY_CHECKLIST="post_deploy_checklist_$(date +%Y%m%d_%H%M%S).md"
cat > "$POST_DEPLOY_CHECKLIST" << EOF
# 📋 AUDITORIA360 - Checklist Pós-Deploy

**Deploy ID:** deploy_$(date +%Y%m%d_%H%M%S)
**Data/Hora:** $(date '+%Y-%m-%d %H:%M:%S')

## ✅ Verificações Obrigatórias (primeiros 30 minutos)

- [ ] Verificar logs de erro
- [ ] Confirmar funcionamento de módulos críticos
- [ ] Testar fluxo de auditoria completo
- [ ] Verificar integração com IA
- [ ] Confirmar acesso de usuários
- [ ] Validar geração de relatórios

## 📊 Monitoramento (primeiras 2 horas)

- [ ] Acompanhar métricas de performance
- [ ] Monitorar taxa de erro
- [ ] Verificar tempo de resposta
- [ ] Confirmar disponibilidade da API
- [ ] Validar backup automático

## 🔔 Comunicação

- [ ] Notificar equipe de desenvolvimento
- [ ] Informar suporte sobre mudanças
- [ ] Atualizar documentação se necessário
- [ ] Comunicar clientes se houver breaking changes

## 🆘 Rollback (se necessário)

- [ ] Backup disponível em: $BACKUP_DIR
- [ ] Comando de rollback: [definir processo]
- [ ] Contato de emergência: [definir equipe]

---

*Checklist gerado automaticamente em $(date)*
EOF

print_success "Checklist pós-deploy criado: $POST_DEPLOY_CHECKLIST"

echo ""
print_success "🚀 Deploy para produção finalizado!"
print_warning "👀 Não se esqueça de seguir o checklist pós-deploy!"

exit 0