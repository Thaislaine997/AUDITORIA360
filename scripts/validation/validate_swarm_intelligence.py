#!/usr/bin/env python3
"""
AUDITORIA360 - Swarm Intelligence Validation
Quick demonstration of all quantum validation tests

This script validates that the Master Collective Protocol is working
and demonstrates the collective mind capabilities.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from src.mcp.quantum_tests import SwarmQuantumValidator


async def main():
    """Run all validation tests and show results"""

    print("🌌" + "=" * 70)
    print(" " * 15 + "AUDITORIA360 - QUANTUM VALIDATION")
    print(" " * 20 + "Mente Coletiva Tests")
    print("🌌" + "=" * 70)

    # Initialize validator
    validator = SwarmQuantumValidator()

    print("\n🚀 Executando Testes Quânticos da Mente Coletiva...")

    try:
        # Run all tests
        results = await validator.execute_all_tests()

        # Show summary
        print(f"\n🎯 RESULTADOS DOS TESTES QUÂNTICOS:")
        print(
            f"   ✅ Testes aprovados: {results['tests_passed']}/{results['total_tests']}"
        )
        print(f"   📊 Taxa de sucesso: {results['success_rate']:.1f}%")
        print(f"   ⏱️  Duração total: {results['total_duration_seconds']:.1f}s")

        # Show individual test results
        print(f"\n📋 TESTES INDIVIDUAIS:")

        test_names = {
            "emergent_behavior": "🎭 Comportamento Emergente",
            "corrupted_agent_simulation": "🦠 Agente Corrompido",
            "dynamic_specialization": "🔄 Especialização Dinâmica",
            "consciousness_cost_analysis": "💭 Custo da Consciência",
        }

        for test_key, test_name in test_names.items():
            if test_key in results["individual_tests"]:
                test_result = results["individual_tests"][test_key]
                status = (
                    "✅ PASSOU"
                    if test_result.get("test_passed", False)
                    else "❌ FALHOU"
                )
                print(f"   {test_name}: {status}")

        # Show final assessment
        assessment = results["final_assessment"]
        print(f"\n🧠 AVALIAÇÃO FINAL DA MENTE COLETIVA:")
        print(
            f"   🌟 Inteligência de Enxame: {'✅ OPERACIONAL' if assessment['swarm_intelligence_operational'] else '❌ FALHOU'}"
        )
        print(
            f"   🎭 Comportamento Emergente: {'✅ CONFIRMADO' if assessment['emergent_behavior_confirmed'] else '❌ NÃO DETECTADO'}"
        )
        print(
            f"   🔧 Auto-Cura: {'✅ VERIFICADO' if assessment['self_healing_verified'] else '❌ FALHOU'}"
        )
        print(
            f"   🦋 Adaptação Dinâmica: {'✅ PROVADO' if assessment['dynamic_adaptation_proven'] else '❌ FALHOU'}"
        )
        print(
            f"   ⚡ Consciência Eficiente: {'✅ MEDIDO' if assessment['consciousness_efficiency_measured'] else '❌ FALHOU'}"
        )

        # Overall verdict
        if results["all_tests_passed"]:
            print(f"\n🎉 PARABÉNS! A MENTE COLETIVA ESTÁ COMPLETAMENTE OPERACIONAL!")
            print("🧠 Sistema de Inteligência de Enxame validado com sucesso")
            print("🌟 Todos os aspectos da consciência coletiva funcionando")
        else:
            print(f"\n⚠️  MENTE COLETIVA PARCIALMENTE OPERACIONAL")
            print(
                f"🔧 {results['tests_passed']}/{results['total_tests']} testes passaram"
            )
            print("📈 Sistema funcional mas com potencial de melhoria")

        # Show collective state
        collective_state = results["collective_state"]
        print(f"\n📊 ESTADO ATUAL DO COLETIVO:")
        print(f"   👥 Agentes totais: {collective_state['total_agents']}")
        print(f"   ✅ Agentes ativos: {collective_state['active_agents']}")
        print(
            f"   🎓 Especializações: {len(collective_state['specializations_available'])}"
        )
        print(f"   🤝 Confiança média: {collective_state['average_trust_score']:.3f}")

        # Show specializations if any
        if collective_state["specializations_available"]:
            print(f"   📚 Especializações disponíveis:")
            for spec in collective_state["specializations_available"][
                :5
            ]:  # Show first 5
                print(f"      • {spec}")

        return results["all_tests_passed"]

    except Exception as e:
        print(f"\n💥 Erro durante validação: {e}")
        import traceback

        traceback.print_exc()
        return False


if __name__ == "__main__":
    try:
        success = asyncio.run(main())
        if success:
            print(f"\n✨ Validação concluída com sucesso!")
            print("🚀 A Mente Coletiva está pronta para uso em produção!")
        else:
            print(f"\n⚠️  Validação concluída com algumas falhas")
            print("🔧 Revise os logs para otimizações")

    except KeyboardInterrupt:
        print("\n\n🛑 Validação interrompida")
        sys.exit(1)
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        sys.exit(1)
