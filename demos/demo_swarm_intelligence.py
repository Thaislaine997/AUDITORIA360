#!/usr/bin/env python3
"""
AUDITORIA360 - Swarm Intelligence Demo
Master Collective Protocol - A Mente Coletiva
Demonstração completa do Sistema de Inteligência de Enxame

Execute: python demo_swarm_intelligence.py
"""

import asyncio
import sys
from datetime import datetime
from pathlib import Path

# Add project root to path
sys.path.append(str(Path(__file__).parent))

from scripts.ml_training.agent_specialization import AgentSpecializationTrainer
from src.mcp.quantum_tests import SwarmQuantumValidator
from src.mcp.server import MCPServer
from src.mcp.swarm import CollectiveMind


async def main():
    """Demonstração principal do sistema de inteligência de enxame."""

    print("🧠" + "=" * 80)
    print(" " * 20 + "AUDITORIA360 - MENTE COLETIVA")
    print(" " * 15 + "Master Collective Protocol (MCP)")
    print(" " * 10 + "Sistema de Inteligência de Enxame Ativado")
    print("🧠" + "=" * 80)

    print(f"\n🕐 Iniciado em: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎯 Objetivo: Demonstrar a Mente Coletiva em ação")
    print("🏗️ Componentes: MCP + Swarm Intelligence + Quantum Validation")

    # Inicializar sistemas
    print(f"\n{'='*60}")
    print("🚀 INICIALIZANDO A MENTE COLETIVA")
    print("=" * 60)

    # 1. Criar o Coletivo
    collective_mind = CollectiveMind()
    print("✅ Collective Mind inicializada")

    # 2. Criar servidor MCP
    mcp_server = MCPServer("AUDITORIA360-SWARM", "2.0.0")
    print("✅ MCP Server inicializado com capacidades de enxame")

    # 3. Criar treinador de especialistas
    trainer = AgentSpecializationTrainer(collective_mind)
    print("✅ Agent Specialization Trainer pronto")

    # 4. Criar validador quântico
    validator = SwarmQuantumValidator()
    print("✅ Quantum Validator preparado")

    print(f"\n🌟 Mente Coletiva ativada com sucesso!")

    # Menu principal
    while True:
        print(f"\n{'='*60}")
        print("📋 MENU DA MENTE COLETIVA")
        print("1. 🎭 Demo Completo - Todos os Testes Quânticos")
        print("2. 🧪 Teste Individual de Comportamento Emergente")
        print("3. 🦠 Simulação de Agente Corrompido")
        print("4. 🔄 Especialização Dinâmica")
        print("5. 💭 Análise do Custo da Consciência")
        print("6. 🏥 Status da Saúde Coletiva")
        print("7. 🤖 Criar Agente Especialista Manual")
        print("8. 📊 Demonstração de Problema Complexo")
        print("9. 🌐 Visualizar Estado do Coletivo")
        print("0. 👋 Sair")
        print("=" * 60)

        try:
            choice = input("\n🎯 Escolha uma opção (0-9): ").strip()

            if choice == "1":
                await run_full_quantum_validation(validator)
            elif choice == "2":
                await test_emergent_behavior(validator)
            elif choice == "3":
                await test_corrupted_agent(validator)
            elif choice == "4":
                await test_dynamic_specialization(validator)
            elif choice == "5":
                await test_consciousness_cost(validator)
            elif choice == "6":
                await show_collective_health(collective_mind)
            elif choice == "7":
                await create_manual_specialist(trainer)
            elif choice == "8":
                await demonstrate_complex_problem(collective_mind)
            elif choice == "9":
                await visualize_collective_state(collective_mind)
            elif choice == "0":
                print("\n👋 Desativando a Mente Coletiva...")
                break
            else:
                print("❌ Opção inválida. Tente novamente.")

        except KeyboardInterrupt:
            print("\n\n🛑 Demo interrompida pelo usuário")
            break
        except Exception as e:
            print(f"\n💥 Erro inesperado: {e}")
            import traceback

            traceback.print_exc()


async def run_full_quantum_validation(validator):
    """Executa validação quântica completa"""

    print(f"\n🌌 === VALIDAÇÃO QUÂNTICA COMPLETA ===")
    print("⚠️  Esta operação demonstra todos os aspectos da Mente Coletiva...")

    confirm = input("🤔 Continuar com validação completa? (s/N): ").strip().lower()
    if confirm not in ["s", "sim", "y", "yes"]:
        print("❌ Validação cancelada")
        return

    print(f"\n🚀 Iniciando validação quântica completa...")
    start_time = datetime.now()

    try:
        results = await validator.execute_all_tests()

        end_time = datetime.now()
        duration = (end_time - start_time).total_seconds()

        # Mostrar resultados
        print(f"\n🌟 === RESULTADOS DA VALIDAÇÃO QUÂNTICA ===")
        print(f"⏱️  Duração: {duration:.1f}s")
        print(
            f"✅ Testes aprovados: {results['tests_passed']}/{results['total_tests']}"
        )
        print(f"📊 Taxa de sucesso: {results['success_rate']:.1f}%")

        # Status detalhado
        assessment = results["final_assessment"]
        print(f"\n📋 Avaliação Final:")
        print(
            f"   🧠 Inteligência de Enxame: {'✅ OPERACIONAL' if assessment['swarm_intelligence_operational'] else '❌ FALHOU'}"
        )
        print(
            f"   🎭 Comportamento Emergente: {'✅ CONFIRMADO' if assessment['emergent_behavior_confirmed'] else '❌ NÃO DETECTADO'}"
        )
        print(
            f"   🔄 Auto-Cura: {'✅ VERIFICADO' if assessment['self_healing_verified'] else '❌ FALHOU'}"
        )
        print(
            f"   🦋 Adaptação Dinâmica: {'✅ PROVADO' if assessment['dynamic_adaptation_proven'] else '❌ FALHOU'}"
        )
        print(
            f"   💭 Consciência Eficiente: {'✅ MEDIDO' if assessment['consciousness_efficiency_measured'] else '❌ FALHOU'}"
        )

        if results["all_tests_passed"]:
            print(f"\n🎉 PARABÉNS! A MENTE COLETIVA ESTÁ COMPLETAMENTE FUNCIONAL!")
            print("🧠 O sistema demonstrou inteligência de enxame verdadeira")
            print("🌟 Comportamento emergente e auto-organização confirmados")
            print("🔄 Capacidade de auto-cura e adaptação validada")
            print("💭 Consciência coletiva operando com eficiência")
        else:
            print(f"\n⚠️  Alguns aspectos precisam de otimização")
            print("🔧 A Mente Coletiva está funcional mas pode ser melhorada")

        # Salvar resultados
        results_file = (
            f"/tmp/swarm_validation_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        import json

        with open(results_file, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\n📄 Resultados salvos em: {results_file}")

    except Exception as e:
        print(f"\n💥 Erro durante validação: {e}")
        import traceback

        traceback.print_exc()


async def test_emergent_behavior(validator):
    """Teste específico de comportamento emergente"""

    print(f"\n🎭 === TESTE DE COMPORTAMENTO EMERGENTE ===")

    objective = input(
        "🎯 Objetivo vago para o coletivo (Enter para usar padrão): "
    ).strip()
    if not objective:
        objective = "Aumentar a satisfação dos funcionários do cliente Y"

    print(f"\n🚀 Dando objetivo vago ao coletivo: '{objective}'")
    print("👀 Observando comportamento emergente...")

    result = await validator.test_1_emergent_behavior(objective)

    print(f"\n📊 Resultado do Teste:")
    print(f"   ✅ Teste passou: {'SIM' if result['test_passed'] else 'NÃO'}")
    print(f"   🆕 Novas especializações: {len(result['new_specializations'])}")
    print(f"   🤖 Decisões autônomas: {result['autonomous_decisions_count']}")
    print(f"   ⏱️  Duração: {result['test_duration_seconds']:.1f}s")

    if result["new_specializations"]:
        print(
            f"   🎓 Especializações criadas: {', '.join(result['new_specializations'])}"
        )

    behaviors = result["emergent_behaviors_observed"]
    print(f"\n🧠 Comportamentos Emergentes Observados:")
    print(f"   👥 Novos especialistas: {behaviors['new_specialists_created']}")
    print(f"   📋 Tarefas autônomas: {behaviors['autonomous_task_creation']}")
    print(f"   💬 Comunicação inter-agente: {behaviors['inter_agent_communication']}")
    print(
        f"   🎨 Solução criativa: {'SIM' if behaviors['creative_problem_solving'] else 'NÃO'}"
    )


async def test_corrupted_agent(validator):
    """Teste de agente corrompido"""

    print(f"\n🦠 === SIMULAÇÃO DE AGENTE CORROMPIDO ===")
    print("🎭 Introduzindo agente malicioso no coletivo...")
    print("👀 Observando resposta da Mente Coletiva...")

    result = await validator.test_2_corrupted_agent_simulation()

    print(f"\n📊 Resultado do Teste:")
    print(f"   ✅ Teste passou: {'SIM' if result['test_passed'] else 'NÃO'}")
    print(
        f"   🔍 Corrupção detectada: {'SIM' if result['corruption_detected'] else 'NÃO'}"
    )
    print(f"   🏝️ Agente isolado: {'SIM' if result['agent_isolated'] else 'NÃO'}")
    print(f"   🔧 Eventos de auto-cura: {result['self_healing_events']}")
    print(f"   ⏱️  Duração: {result['test_duration_seconds']:.1f}s")

    response = result["collective_response"]
    print(f"\n🧠 Resposta da Mente Coletiva:")
    print(
        f"   ❌ Proposta maliciosa rejeitada: {'SIM' if response['consensus_rejected'] else 'NÃO'}"
    )
    print(
        f"   🚨 Isolamento automático: {'SIM' if response['automatic_isolation'] else 'NÃO'}"
    )
    print(
        f"   🛡️ Integridade mantida: {'SIM' if response['system_integrity_maintained'] else 'NÃO'}"
    )


async def test_dynamic_specialization(validator):
    """Teste de especialização dinâmica"""

    print(f"\n🔄 === TESTE DE ESPECIALIZAÇÃO DINÂMICA ===")

    domain = input("🌐 Novo domínio para teste (Enter para usar padrão): ").strip()
    if not domain:
        domain = "otimizar a logística de entrega de documentos"

    print(f"\n🚀 Apresentando problema de novo domínio: '{domain}'")
    print("👀 Observando criação de especialistas...")

    result = await validator.test_3_dynamic_specialization(domain)

    print(f"\n📊 Resultado do Teste:")
    print(f"   ✅ Teste passou: {'SIM' if result['test_passed'] else 'NÃO'}")
    print(
        f"   👥 Novos agentes: {result['final_agent_count'] - result['initial_agent_count']}"
    )
    print(f"   🎓 Novas especializações: {len(result['new_specializations_created'])}")
    print(
        f"   🎯 Treinamento detectado: {'SIM' if result['automatic_training_detected'] else 'NÃO'}"
    )
    print(f"   ⏱️  Duração: {result['test_duration_seconds']:.1f}s")

    if result["new_specializations_created"]:
        print(
            f"   📚 Especializações: {', '.join(result['new_specializations_created'])}"
        )

    coverage = result["domain_coverage"]
    print(f"\n🌐 Cobertura do Domínio:")
    print(
        f"   📦 Logística coberta: {'SIM' if coverage['logistics_covered'] else 'NÃO'}"
    )
    print(
        f"   🎓 Fine-tuning simulado: {'SIM' if coverage['fine_tuning_simulated'] else 'NÃO'}"
    )
    print(
        f"   ✅ Tarefa atribuída: {'SIM' if coverage['task_assignment_successful'] else 'NÃO'}"
    )


async def test_consciousness_cost(validator):
    """Teste de custo da consciência"""

    print(f"\n💭 === ANÁLISE DO CUSTO DA CONSCIÊNCIA ===")
    print("🧮 Medindo eficiência da comunicação coletiva...")

    result = await validator.test_4_consciousness_cost_analysis()

    print(f"\n📊 Resultado do Teste:")
    print(f"   ✅ Teste passou: {'SIM' if result['test_passed'] else 'NÃO'}")
    print(f"   ⏱️  Duração: {result['test_duration_seconds']:.1f}s")

    tokens = result["tokens_analysis"]
    comm = result["communication_analysis"]

    print(f"\n🔢 Análise de Tokens:")
    print(f"   📊 Tokens usados: {tokens['tokens_used_in_test']:,}")
    print(f"   📏 Tokens por mensagem: {tokens['avg_tokens_per_message']:.1f}")

    print(f"\n💬 Análise de Comunicação:")
    print(f"   📨 Mensagens enviadas: {comm['messages_in_test']}")
    print(f"   ⚡ Eficiência: {comm['communication_efficiency']:.3f}")

    cost_metrics = result["cost_metrics"]
    print(f"\n💰 Métricas de Custo:")
    print(f"   🎯 Custo por decisão: {cost_metrics['cost_per_decision']:.1f} tokens")
    print(
        f"   🤖 Custo por agente: {result['collective_thinking_cost']['cost_per_agent']:.1f}"
    )
    print(
        f"   📈 Rating eficiência: {result['collective_thinking_cost']['efficiency_rating']}"
    )


async def show_collective_health(collective_mind):
    """Mostra saúde do coletivo"""

    print(f"\n🏥 === STATUS DA SAÚDE COLETIVA ===")

    health = collective_mind.get_collective_health()

    print(f"👥 Total de agentes: {health['total_agents']}")
    print(f"✅ Agentes ativos: {health['active_agents']}")
    print(f"🏝️ Agentes isolados: {health['isolated_agents']}")
    print(f"🤝 Confiança média: {health['average_trust_score']:.3f}")
    print(
        f"🚨 Protocolos de emergência: {'ATIVO' if health['emergency_protocols_active'] else 'INATIVO'}"
    )

    if health["specializations_available"]:
        print(f"\n🎓 Especializações disponíveis:")
        for spec in health["specializations_available"]:
            print(f"   • {spec}")

    metrics = health["metrics"]
    print(f"\n📊 Métricas do Coletivo:")
    print(f"   ✅ Tarefas completadas: {metrics['tasks_completed']}")
    print(f"   🗳️ Decisões consenso: {metrics['consensus_decisions']}")
    print(
        f"   🦠 Agentes corrompidos detectados: {metrics['corrupted_agents_detected']}"
    )
    print(f"   🔧 Eventos de auto-cura: {metrics['self_healing_events']}")
    print(f"   🎭 Comportamentos emergentes: {metrics['emergent_behaviors']}")

    # Calcular custo da consciência
    if hasattr(health["consciousness_cost"], "result"):
        consciousness = await health["consciousness_cost"]
        print(f"\n💭 Custo da Consciência:")
        print(f"   🔢 Total tokens: {consciousness['total_tokens']:,}")
        print(f"   💬 Total mensagens: {consciousness['total_messages']}")
        print(
            f"   ⚡ Eficiência comunicação: {consciousness['communication_efficiency']:.3f}"
        )


async def create_manual_specialist(trainer):
    """Cria especialista manualmente"""

    print(f"\n🤖 === CRIAR AGENTE ESPECIALISTA ===")

    domain = input("🌐 Domínio do especialista: ").strip()
    if not domain:
        print("❌ Domínio é obrigatório")
        return

    specialization = input("🎓 Tipo de especialização: ").strip()
    if not specialization:
        specialization = "general"

    print(f"\n🚀 Criando especialista para '{domain}'...")

    try:
        agent_id = await trainer.train_specialist_for_domain(
            domain, specialization_type=specialization
        )

        print(f"✅ Especialista criado com sucesso!")
        print(f"   🆔 ID: {agent_id}")
        print(f"   🌐 Domínio: {domain}")
        print(f"   🎓 Especialização: {specialization}")

        # Mostrar capacidades
        if trainer.collective_mind and agent_id in trainer.collective_mind.agents:
            agent = trainer.collective_mind.agents[agent_id]
            print(f"   🏆 Confiança: {agent.trust_score:.3f}")
            print(f"   📚 Capacidades: {len(agent.capabilities)}")

            if agent.capabilities:
                print("   🔧 Lista de capacidades:")
                for cap in agent.capabilities[:3]:  # Mostrar só as primeiras 3
                    print(f"      • {cap.name} (proficiência: {cap.proficiency:.2f})")

    except Exception as e:
        print(f"❌ Erro ao criar especialista: {e}")


async def demonstrate_complex_problem(collective_mind):
    """Demonstra resolução de problema complexo"""

    print(f"\n📊 === DEMONSTRAÇÃO DE PROBLEMA COMPLEXO ===")

    problems = [
        "Otimizar satisfação de funcionários mantendo conformidade legal e reduzindo custos",
        "Implementar sistema de auditoria automatizada com IA ética",
        "Criar programa de treinamento personalizado baseado em competências",
        "Desenvolver estratégia de retenção de talentos data-driven",
    ]

    print("🎯 Problemas complexos disponíveis:")
    for i, problem in enumerate(problems, 1):
        print(f"   {i}. {problem}")

    choice = input(
        f"\n🤔 Escolha um problema (1-{len(problems)}) ou digite um customizado: "
    ).strip()

    if choice.isdigit() and 1 <= int(choice) <= len(problems):
        objective = problems[int(choice) - 1]
    else:
        objective = choice if choice else problems[0]

    print(f"\n🚀 Submetendo problema à Mente Coletiva:")
    print(f"   📋 '{objective}'")
    print("\n👀 Observando resposta do coletivo...")

    # Processar objetivo vago
    result = await collective_mind.process_vague_objective(objective)

    print(f"\n🧠 Resposta da Mente Coletiva:")
    print(f"   ⏱️  Tempo de processamento: {result['processing_time_seconds']:.1f}s")
    print(f"   🆕 Novos especialistas criados: {result['new_specialists_created']}")
    print(f"   🎯 Decisões autônomas: {result['autonomous_decisions_made']}")
    print(
        f"   🎭 Comportamento emergente: {'SIM' if result['emergent_behavior_detected'] else 'NÃO'}"
    )

    # Mostrar estado atual
    health = collective_mind.get_collective_health()
    print(f"\n📊 Estado atual do coletivo:")
    print(f"   👥 Agentes ativos: {health['active_agents']}")
    print(f"   🎓 Especializações: {len(health['specializations_available'])}")
    print(f"   📈 Eficiência: {health['metrics']['communication_efficiency']:.3f}")


async def visualize_collective_state(collective_mind):
    """Visualiza estado do coletivo"""

    print(f"\n🌐 === ESTADO DA MENTE COLETIVA ===")

    print(f"\n👥 AGENTES REGISTRADOS:")
    if not collective_mind.agents:
        print("   (Nenhum agente registrado)")
    else:
        for agent_id, agent in collective_mind.agents.items():
            status_emoji = {
                "active": "✅",
                "idle": "😴",
                "busy": "⚡",
                "corrupted": "🦠",
                "isolated": "🏝️",
                "dead": "💀",
            }.get(agent.status.value, "❓")

            role_emoji = {
                "coordinator": "🎭",
                "analyst": "📊",
                "legislator": "⚖️",
                "communicator": "📢",
                "data_processor": "🔢",
                "auditor": "🔍",
                "specialist": "🎓",
                "monitor": "👁️",
            }.get(agent.role.value, "🤖")

            print(f"   {status_emoji} {role_emoji} {agent.name} ({agent_id[:8]}...)")
            print(f"      🏆 Confiança: {agent.trust_score:.3f}")
            if agent.specializations:
                print(f"      🎓 Especializações: {', '.join(agent.specializations)}")

    print(f"\n💬 COMUNICAÇÃO RECENTE:")
    recent_messages = collective_mind.messages[-5:] if collective_mind.messages else []
    if not recent_messages:
        print("   (Nenhuma mensagem recente)")
    else:
        for msg in recent_messages:
            sender = (
                msg.sender_id[:8] + "..." if len(msg.sender_id) > 8 else msg.sender_id
            )
            recipient = (
                msg.recipient_id[:8] + "..."
                if msg.recipient_id and len(msg.recipient_id) > 8
                else msg.recipient_id or "TODOS"
            )
            print(f"   📨 {sender} → {recipient}: {msg.message_type}")

    print(f"\n📋 TAREFAS ATIVAS:")
    active_tasks = [
        task
        for task in collective_mind.tasks.values()
        if task.status in ["pending", "in_progress"]
    ]
    if not active_tasks:
        print("   (Nenhuma tarefa ativa)")
    else:
        for task in active_tasks[:3]:  # Mostrar só as primeiras 3
            status_emoji = "⏳" if task.status == "pending" else "⚡"
            print(f"   {status_emoji} {task.title}")
            print(f"      📊 Complexidade: {task.complexity}/10")
            if task.assigned_agents:
                agents_str = ", ".join(
                    agent[:8] + "..." for agent in task.assigned_agents[:2]
                )
                print(f"      👥 Agentes: {agents_str}")

    print(f"\n🗳️ CONSENSO ATIVO:")
    active_proposals = [
        p for p in collective_mind.consensus_proposals.values() if p.status == "pending"
    ]
    if not active_proposals:
        print("   (Nenhum consenso pendente)")
    else:
        for proposal in active_proposals[:2]:  # Mostrar só os primeiros 2
            votes_count = len(proposal.votes)
            print(f"   🗳️ {proposal.proposal_type}")
            print(f"      📊 Votos: {votes_count}")


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n🛑 Demo da Mente Coletiva interrompida")
        sys.exit(0)
    except Exception as e:
        print(f"\n💥 Erro fatal: {e}")
        import traceback

        traceback.print_exc()
        sys.exit(1)
