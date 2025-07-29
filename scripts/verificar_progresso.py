#!/usr/bin/env python3
"""
Script para verificar o progresso dos itens pendentes do AUDITORIA360
Baseado no RELATORIO_UNIFICADO_FINAL.md
"""

import json
import os
import subprocess
from datetime import datetime
from pathlib import Path


def verificar_cobertura_testes():
    """Verifica a cobertura atual de testes"""
    try:
        result = subprocess.run(
            ["pytest", "--cov=src", "--cov=api", "--cov=services", "--cov-report=json"],
            capture_output=True,
            text=True,
            cwd="/home/runner/work/AUDITORIA360/AUDITORIA360",
        )
        if result.returncode == 0:
            # Tenta ler o arquivo de cobertura gerado
            if os.path.exists("coverage.json"):
                with open("coverage.json", "r") as f:
                    coverage_data = json.load(f)
                return coverage_data.get("totals", {}).get("percent_covered", 0)
        return "Não disponível"
    except Exception as e:
        return f"Erro: {e}"


def contar_arquivos_orfaos():
    """Conta arquivos órfãos potenciais identificados"""
    orfaos = []
    patterns = [
        "scripts/exemplo_*.py",
        "automation/legacy_*.py",
        "backups/temp_*",
        "configs/old_*.json",
    ]

    base_path = Path("/home/runner/work/AUDITORIA360/AUDITORIA360")

    for pattern in patterns:
        for file in base_path.glob(pattern):
            orfaos.append(str(file))

    return len(orfaos), orfaos


def verificar_dashboards_deploy():
    """Verifica se dashboards estão deployados"""
    # Verifica se existe configuração Vercel para dashboards
    vercel_config = Path("/home/runner/work/AUDITORIA360/AUDITORIA360/vercel.json")
    if vercel_config.exists():
        with open(vercel_config, "r") as f:
            config = json.load(f)
            builds = config.get("builds", [])
            for build in builds:
                if "dashboards" in build.get("src", ""):
                    return True
    return False


def verificar_automacao_serverless():
    """Verifica migração de automação para serverless"""
    github_workflows = Path(
        "/home/runner/work/AUDITORIA360/AUDITORIA360/.github/workflows"
    )
    automation_files = list(
        Path("/home/runner/work/AUDITORIA360/AUDITORIA360/automation").glob("*.py")
    )

    workflows_count = (
        len(list(github_workflows.glob("*.yml"))) if github_workflows.exists() else 0
    )
    automation_count = len(automation_files)

    # Estima progresso baseado na relação workflows/automation files
    if automation_count == 0:
        return 100
    else:
        return min(100, (workflows_count / automation_count) * 100)


def gerar_relatorio_progresso():
    """Gera relatório de progresso atual"""
    print("🔍 AUDITORIA360 - Verificação de Progresso")
    print("=" * 50)
    print(f"📅 Data: {datetime.now().strftime('%d/%m/%Y %H:%M:%S')}")
    print()

    # 1. Cobertura de testes
    cobertura = verificar_cobertura_testes()
    print(f"🧪 Cobertura de Testes: {cobertura}% (Meta: 85%)")
    if isinstance(cobertura, (int, float)):
        if cobertura >= 85:
            print("   ✅ Meta atingida!")
        else:
            print(f"   ⏳ Faltam {85 - cobertura:.1f}% para a meta")
    print()

    # 2. Arquivos órfãos
    num_orfaos, lista_orfaos = contar_arquivos_orfaos()
    print(f"🗑️ Arquivos Órfãos: {num_orfaos} encontrados (Meta: ≤10)")
    if num_orfaos <= 10:
        print("   ✅ Meta atingida!")
    else:
        print(f"   ⏳ Remover {num_orfaos - 10} arquivos para atingir meta")
        print("   📋 Arquivos encontrados:")
        for arquivo in lista_orfaos[:5]:  # Mostra apenas os primeiros 5
            print(f"      - {arquivo}")
        if len(lista_orfaos) > 5:
            print(f"      ... e mais {len(lista_orfaos) - 5} arquivos")
    print()

    # 3. Deploy dashboards
    dashboards_ok = verificar_dashboards_deploy()
    print(
        f"🚀 Deploy Dashboards: {'✅ Configurado' if dashboards_ok else '❌ Pendente'}"
    )
    if not dashboards_ok:
        print("   ⏳ Configurar vercel.json para dashboards Streamlit")
    print()

    # 4. Automação serverless
    progresso_auto = verificar_automacao_serverless()
    print(f"🤖 Automação Serverless: {progresso_auto:.0f}% (Meta: 100%)")
    if progresso_auto >= 100:
        print("   ✅ Meta atingida!")
    else:
        print(f"   ⏳ Migrar scripts restantes para GitHub Actions/Vercel")
    print()

    # Resumo geral
    print("📊 RESUMO GERAL")
    print("-" * 30)
    itens_ok = sum(
        [
            isinstance(cobertura, (int, float)) and cobertura >= 85,
            num_orfaos <= 10,
            dashboards_ok,
            progresso_auto >= 100,
        ]
    )

    progresso_geral = (itens_ok / 4) * 100
    print(f"Progresso Geral: {progresso_geral:.0f}% ({itens_ok}/4 itens completos)")

    if progresso_geral == 100:
        print("🎉 PROJETO 100% CONCLUÍDO!")
    else:
        print(f"⏳ Restam {4 - itens_ok} itens para conclusão total")

    print()
    print("📋 Para ver o plano completo, consulte:")
    print("   docs/RELATORIO_UNIFICADO_FINAL.md")


if __name__ == "__main__":
    gerar_relatorio_progresso()
