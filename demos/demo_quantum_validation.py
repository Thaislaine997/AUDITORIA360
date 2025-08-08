#!/usr/bin/env python3
"""
AUDITORIA360 - Quantum Validation Demo
Demonstração completa do Sistema Nervoso Descentralizado e Fogo de Artifício de Funções

Execute: python demo_quantum_validation.py
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.serverless.quantum_orchestrator import QuantumValidationOrchestrator


async def main():
    """Demonstração principal do sistema quântico."""

    print("🌌" + "=" * 80)
    print(" " * 15 + "AUDITORIA360 - QUANTUM VALIDATION DEMO")
    print(" " * 10 + "Sistema Nervoso Descentralizado + Fogo de Artifício")
    print("🌌" + "=" * 80)

    print(f"\n🕐 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Objetivo: Validar arquitetura serverless descentralizada")
    print("🏗️ Componentes: DuckDB + R2 + ML + Visualização")

    # Inicializar orquestrador
    orchestrator = QuantumValidationOrchestrator()

    print(f"\n{'='*60}")
    print("📋 MENU DE DEMONSTRAÇÃO")
    print("1. Demo Rápido - Testes Individuais")
    print("2. Validação Quântica Completa (4 testes)")
    print("3. Sair")
    print("=" * 60)

    while True:
        try:
            choice = input("\n🎯 Escolha uma opção (1-3): ").strip()

            if choice == "1":
                await run_quick_demo(orchestrator)
            elif choice == "2":
                await run_full_validation(orchestrator)
            elif choice == "3":
                print("\n👋 Até logo!")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")

        except KeyboardInterrupt:
            print("\n\n🛑 Demo interrompida pelo usuário")
            break
        except Exception as e:
            print(f"\n💥 Erro inesperado: {e}")
            break


async def run_quick_demo(orchestrator):
    """Executa demonstração rápida dos componentes."""

    print(f"\n🚀 === DEMO RÁPIDO ===")

    # Teste 1: Sistema Nervoso de Dados
    print(f"\n🧠 Testando Sistema Nervoso de Dados...")
    try:
        dataset_info = orchestrator.nervous_system.create_optimized_parquet_dataset(
            "demo_dataset", size_gb=0.01
        )

        result = await orchestrator.nervous_system.execute_distributed_query(
            "SELECT department, COUNT(*) as count FROM demo_dataset GROUP BY department LIMIT 3",
            "demo_dataset",
        )

        print(f"   ✅ Dataset criado: {len(dataset_info['partitions'])} partições")
        print(f"   ✅ Query executada em {result['execution_time_ms']:.1f}ms")

    except Exception as e:
        print(f"   ❌ Erro: {e}")

    # Teste 2: Fogo de Artifício de Funções
    print(f"\n🎆 Testando Fogo de Artifício de Funções...")
    try:
        # Função individual
        request_data = {"function_type": "analytics", "complexity": 1}
        firework = await orchestrator.fireworks.ignite_function(
            "analytics", request_data
        )
        await orchestrator.fireworks.execute_function(firework)
        await orchestrator.fireworks.extinguish_function(firework)

        print(f"   ✅ Função executada em {firework.execution_time_ms:.1f}ms")
        print(f"   ✅ Cold start: {firework.cold_start_ms:.1f}ms")

        # Mini tempestade
        storm_results = await orchestrator.fireworks.fireworks_storm_simulation(
            target_rps=5, ramp_up_seconds=1, sustain_seconds=2
        )

        print(
            f"   ✅ Mini tempestade: {storm_results['requests_completed']} requests processados"
        )

    except Exception as e:
        print(f"   ❌ Erro: {e}")

    # Teste 3: Preditor de Cold Start
    print(f"\n🔮 Testando Preditor de Cold Start...")
    try:
        function_analyses = orchestrator.cold_start_predictor.scan_codebase_functions()
        print(f"   ✅ Escaneados {len(function_analyses)} arquivos Python")

        if len(function_analyses) >= 5:
            training_df = orchestrator.cold_start_predictor.generate_training_data(
                function_analyses[:5]
            )
            X, y = orchestrator.cold_start_predictor.prepare_features(training_df)
            training_results = orchestrator.cold_start_predictor.train_model(X, y)

            print(f"   ✅ Modelo treinado: {training_results['best_model']}")
            print(f"   ✅ RMSE: {training_results['best_score']:.1f}ms")

    except Exception as e:
        print(f"   ❌ Erro: {e}")

    print(f"\n🎉 Demo rápido concluído!")


async def run_full_validation(orchestrator):
    """Executa validação quântica completa."""

    print(f"\n🌌 === VALIDAÇÃO QUÂNTICA COMPLETA ===")
    print("⚠️  Esta operação pode levar alguns minutos...")

    confirm = input("🤔 Continuar? (s/N): ").strip().lower()
    if confirm not in ["s", "sim", "y", "yes"]:
        print("❌ Validação cancelada")
        return

    # Parâmetros otimizados para demo
    parameters = {
        "test1": {"dataset_size_gb": 0.1, "concurrent_functions": 50},
        "test2": {},
        "test3": {"target_rps": 100, "ramp_up_seconds": 3, "sustain_seconds": 5},
        "test4": {},
    }

    print(f"\n🚀 Iniciando validação quântica com parâmetros otimizados...")
    start_time = datetime.now()

    try:
        results = await orchestrator.execute_full_quantum_validation(parameters)

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Mostrar resultados
        print(f"\n🌟 === RESULTADOS DA VALIDAÇÃO QUÂNTICA ===")
        print(f"🆔 Test ID: {results['test_id']}")
        print(f"⏱️  Duração: {duration:.1f}s")

        summary = results["overall_summary"]
        print(f"✅ Testes aprovados: {summary['tests_passed']}/4")
        print(f"📊 Taxa de sucesso: {summary['success_rate_percentage']:.1f}%")

        print(f"\n📋 Detalhes por teste:")

        test_names = {
            "massive_decentralized_query": "1. Consulta Descentralizada Massiva",
            "predictive_cold_start": "2. Cold Start Preditivo",
            "fireworks_storm": "3. Tempestade de Fogo de Artifício",
            "immutability_versioning": "4. Imutabilidade e Versionamento",
        }

        for test_key, test_name in test_names.items():
            if test_key in results["individual_tests"]:
                test_result = results["individual_tests"][test_key]
                passed = test_result.get("test_passed", False)
                status = "✅ APROVADO" if passed else "❌ REPROVADO"
                print(f"   {test_name}: {status}")

                # Mostrar métricas específicas
                if (
                    test_key == "massive_decentralized_query"
                    and "performance_metrics" in test_result
                ):
                    p99 = test_result["performance_metrics"]["p99_execution_time_ms"]
                    print(f"      • P99: {p99:.1f}ms (meta: <500ms)")

                elif (
                    test_key == "predictive_cold_start"
                    and "model_performance" in test_result
                ):
                    r2 = test_result["model_performance"]["r2_score"]
                    print(f"      • R²: {r2:.3f} (meta: >0.7)")

                elif test_key == "fireworks_storm" and "summary" in test_result:
                    requests = test_result["summary"]["requests_processed"]
                    throttling = test_result["summary"]["throttling_errors"]
                    print(f"      • Requests: {requests:,}, Throttling: {throttling}")

        # Verificação final
        if summary["all_tests_passed"]:
            print(f"\n🎉 PARABÉNS! Arquitetura completamente validada!")
            print("🧠 Sistema Nervoso Descentralizado: OPERACIONAL")
            print("🎆 Fogo de Artifício de Funções: OPERACIONAL")
            print("🔮 Predição de Cold Start: OPERACIONAL")
            print("🔄 Versionamento Imutável: OPERACIONAL")
            print(
                "\n✨ A plataforma é verdadeiramente distribuída, resiliente e instantânea!"
            )
        else:
            print(f"\n⚠️  Alguns testes falharam, mas a arquitetura base está funcional")
            print("🔧 Revise os logs para otimizações adicionais")

        # Salvar resultados
        results_file = f"/tmp/quantum_validation_{results['test_id'][:8]}.json"
        import json

        with open(results_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n📄 Resultados detalhados salvos em: {results_file}")

    except Exception as e:
        print(f"\n💥 Erro durante validação: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Demo interrompida")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        sys.exit(1)
