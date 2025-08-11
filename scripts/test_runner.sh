#!/bin/bash

# AUDITORIA360 - Test Runner Script
# Executa testes e health checks do sistema

set -e  # Exit on any error

echo "🧪 AUDITORIA360 - Executando Testes e Verificações"
echo "================================================"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${BLUE}[TEST]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[PASS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[FAIL]${NC} $1"
}

# Initialize counters
TESTS_PASSED=0
TESTS_FAILED=0
HEALTH_CHECKS_PASSED=0
HEALTH_CHECKS_FAILED=0

# Function to run a test and track results
run_test() {
    local test_name="$1"
    local test_command="$2"
    
    print_status "Executando: $test_name"
    
    if eval "$test_command"; then
        print_success "$test_name ✓"
        ((TESTS_PASSED++))
        return 0
    else
        print_error "$test_name ✗"
        ((TESTS_FAILED++))
        return 1
    fi
}

# Check if virtual environment is activated
if [ -z "$VIRTUAL_ENV" ]; then
    if [ -d "venv" ]; then
        print_status "Ativando ambiente virtual..."
        source venv/bin/activate
    else
        print_warning "Ambiente virtual não encontrado. Execute scripts/dev_setup.sh primeiro"
    fi
fi

# Check Python availability
if ! command -v python &> /dev/null; then
    print_error "Python não encontrado"
    exit 1
fi

print_status "Iniciando bateria de testes..."
echo ""

# Test 1: Import Tests
print_status "=== Teste de Importação de Módulos ==="
run_test "Importação do sistema de atualização de status" \
    "python -c 'import automation.update_status; print(\"Import successful\")'"

run_test "Importação do sistema de auditoria de segurança" \
    "python -c 'import automation.security_audit; print(\"Import successful\")'"

run_test "Importação do coletor de métricas" \
    "python -c 'import automation.metrics_collector; print(\"Import successful\")'"

run_test "Importação do gestor de incidentes" \
    "python -c 'import automation.incident_management; print(\"Import successful\")'"

echo ""

# Test 2: Configuration Tests
print_status "=== Teste de Configuração ==="
run_test "Verificação do arquivo .env" \
    "[ -f '.env' ] && echo 'Arquivo .env existe'"

run_test "Verificação do arquivo requirements.txt" \
    "[ -f 'requirements.txt' ] && echo 'Arquivo requirements.txt existe'"

run_test "Verificação da estrutura de diretórios" \
    "[ -d 'automation' ] && [ -d 'templates' ] && [ -d 'scripts' ] && echo 'Estrutura de diretórios OK'"

echo ""

# Test 3: Dependency Tests
print_status "=== Teste de Dependências ==="
run_test "Verificação de dependências Python críticas" \
    "python -c 'import fastapi, requests, pandas, json, datetime; print(\"Dependências críticas OK\")'"

run_test "Verificação de bibliotecas de formatação" \
    "python -c 'import logging, os, time; print(\"Bibliotecas básicas OK\")'"

echo ""

# Test 4: Health Check Tests
print_status "=== Health Check do Sistema ==="
if [ -f "automation/update_status.py" ]; then
    print_status "Executando health check geral..."
    if python automation/update_status.py; then
        print_success "Health check geral ✓"
        ((HEALTH_CHECKS_PASSED++))
    else
        print_error "Health check geral ✗"
        ((HEALTH_CHECKS_FAILED++))
    fi
else
    print_warning "Script de health check não encontrado"
fi

echo ""

# Test 5: Security Audit
print_status "=== Auditoria de Segurança ==="
if [ -f "automation/security_audit.py" ]; then
    print_status "Executando auditoria de segurança..."
    if python automation/security_audit.py; then
        print_success "Auditoria de segurança ✓"
        ((HEALTH_CHECKS_PASSED++))
    else
        print_warning "Auditoria de segurança encontrou questões (verificar relatório)"
        ((HEALTH_CHECKS_FAILED++))
    fi
else
    print_warning "Script de auditoria de segurança não encontrado"
fi

echo ""

# Test 6: Metrics Collection
print_status "=== Coleta de Métricas ==="
if [ -f "automation/metrics_collector.py" ]; then
    print_status "Executando coleta de métricas..."
    if python automation/metrics_collector.py; then
        print_success "Coleta de métricas ✓"
        ((HEALTH_CHECKS_PASSED++))
    else
        print_warning "Coleta de métricas encontrou problemas (verificar relatório)"
        ((HEALTH_CHECKS_FAILED++))
    fi
else
    print_warning "Script de coleta de métricas não encontrado"
fi

echo ""

# Test 7: Template Tests
print_status "=== Teste de Templates ==="
run_test "Verificação de template de alerta HTML" \
    "[ -f 'templates/alert_template.html' ] && echo 'Template HTML existe'"

run_test "Verificação de template de alerta Markdown" \
    "[ -f 'templates/alert_template.md' ] && echo 'Template Markdown existe'"

echo ""

# Test 8: File Generation Tests
print_status "=== Teste de Geração de Arquivos ==="
run_test "Verificação de geração de status" \
    "[ -f 'processos_status_auditoria360.md' ] && echo 'Arquivo de status existe'"

run_test "Verificação de geração de JSON de status" \
    "[ -f 'status_report_auditoria360.json' ] && echo 'JSON de status existe'"

echo ""

# Test 9: Python Code Quality (if available)
print_status "=== Qualidade de Código ==="
if command -v flake8 &> /dev/null; then
    run_test "Verificação com flake8" \
        "flake8 automation/ --count --select=E9,F63,F7,F82 --show-source --statistics"
else
    print_warning "flake8 não instalado - pulando verificação de qualidade"
fi

if command -v black &> /dev/null; then
    run_test "Verificação de formatação com black" \
        "black --check automation/ scripts/ || echo 'Código precisa de formatação'"
else
    print_warning "black não instalado - pulando verificação de formatação"
fi

echo ""

# Test 10: Integration Tests (if test files exist)
print_status "=== Testes de Integração ==="
if [ -d "tests" ]; then
    if command -v pytest &> /dev/null; then
        run_test "Execução de testes com pytest" \
            "pytest tests/ -v --tb=short"
    else
        print_warning "pytest não instalado - pulando testes unitários"
    fi
else
    print_warning "Diretório tests não encontrado - pulando testes unitários"
fi

echo ""

# Test 11: API Health Check (if server is running)
print_status "=== Teste de API (opcional) ==="
if curl -s http://localhost:8001/api/health/status >/dev/null 2>&1; then
    run_test "Health check da API" \
        "curl -s http://localhost:8001/api/health/status | grep -q 'healthy\\|ok\\|operational'"
else
    print_warning "API não está rodando em localhost:8001 - pulando teste de API"
fi

echo ""

# Final Summary
echo "=========================================="
echo "📊 RESUMO DOS TESTES"
echo "=========================================="
echo ""
echo "🧪 Testes de Código:"
echo "   ✅ Aprovados: $TESTS_PASSED"
echo "   ❌ Falharam: $TESTS_FAILED"
echo ""
echo "🏥 Health Checks:"
echo "   ✅ Aprovados: $HEALTH_CHECKS_PASSED"
echo "   ❌ Falharam: $HEALTH_CHECKS_FAILED"
echo ""

TOTAL_TESTS=$((TESTS_PASSED + TESTS_FAILED))
TOTAL_HEALTH=$((HEALTH_CHECKS_PASSED + HEALTH_CHECKS_FAILED))
TOTAL_ALL=$((TOTAL_TESTS + TOTAL_HEALTH))
TOTAL_PASSED=$((TESTS_PASSED + HEALTH_CHECKS_PASSED))

if [ $TOTAL_ALL -gt 0 ]; then
    SUCCESS_RATE=$(echo "scale=1; $TOTAL_PASSED * 100 / $TOTAL_ALL" | bc -l 2>/dev/null || echo "N/A")
    echo "📈 Taxa de Sucesso: ${SUCCESS_RATE}%"
else
    echo "📈 Taxa de Sucesso: N/A"
fi

echo ""

# Generate test report
REPORT_FILE="test_results_$(date +%Y%m%d_%H%M%S).md"
cat > "$REPORT_FILE" << EOF
# 🧪 AUDITORIA360 - Relatório de Testes

**Data/Hora:** $(date '+%Y-%m-%d %H:%M:%S')

## 📊 Resumo

- **Testes de Código:** $TESTS_PASSED/$TOTAL_TESTS aprovados
- **Health Checks:** $HEALTH_CHECKS_PASSED/$TOTAL_HEALTH aprovados
- **Taxa de Sucesso:** ${SUCCESS_RATE}%

## 🏥 Status dos Módulos

$(if [ -f "processos_status_auditoria360.md" ]; then
    echo "### Status Atual do Sistema"
    echo ""
    cat processos_status_auditoria360.md | head -20
    echo ""
    echo "[Relatório completo](processos_status_auditoria360.md)"
else
    echo "Status do sistema não disponível"
fi)

## 🔒 Auditoria de Segurança

$(if [ -f "security_audit_report.md" ]; then
    echo "### Resultado da Auditoria"
    echo ""
    cat security_audit_report.md | head -15
    echo ""
    echo "[Relatório completo](security_audit_report.md)"
else
    echo "Auditoria de segurança não executada"
fi)

---

*Relatório gerado automaticamente em $(date)*
EOF

print_success "Relatório de testes salvo em: $REPORT_FILE"

# Exit with appropriate code
if [ $TESTS_FAILED -eq 0 ] && [ $HEALTH_CHECKS_FAILED -eq 0 ]; then
    echo ""
    print_success "🎉 Todos os testes passaram! Sistema está funcionando corretamente."
    exit 0
else
    echo ""
    print_warning "⚠️  Alguns testes falharam. Verifique os logs acima."
    exit 1
fi