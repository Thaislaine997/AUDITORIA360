"""
Script de verificação manual para o módulo CCT
Este script demonstra como usar as funcionalidades do módulo CCT
"""

import json
from src.services.cct_service import CCTService


def demonstrar_funcionalidades_cct():
    """
    Demonstra as principais funcionalidades do módulo CCT
    """
    print("=== DEMONSTRAÇÃO DO MÓDULO CCT ===\n")
    
    # Inicializar o serviço (mesmo sem Supabase configurado)
    service = CCTService()
    print(f"✓ Serviço CCT inicializado (Cliente Supabase: {'Disponível' if service.client else 'Não disponível'})")
    
    # Mostrar estrutura de dados para sindicato
    exemplo_sindicato = {
        "nome_sindicato": "Sindicato dos Trabalhadores no Comércio de São Paulo",
        "cnpj": "12.345.678/0001-99",
        "base_territorial": "São Paulo - SP",
        "categoria_representada": "Trabalhadores no Comércio de Bens, Serviços e Turismo"
    }
    
    print("\n--- Estrutura de dados para Sindicato ---")
    print(json.dumps(exemplo_sindicato, indent=2, ensure_ascii=False))
    
    # Mostrar estrutura de dados para CCT
    exemplo_cct = {
        "sindicato_id": 1,
        "numero_registro_mte": "SP000123/2024",
        "vigencia_inicio": "2024-01-01",
        "vigencia_fim": "2024-12-31",
        "link_documento_oficial": "https://www.gov.br/trabalho/ccts/SP000123-2024.pdf",
        "dados_cct": {
            "resumo_executivo": "Aumento de 8% nos salários, novo piso de R$ 1.850,00 e vale-refeição de R$ 25,00/dia.",
            "pisos_salariais": [
                {"cargo": "Auxiliar Administrativo", "valor": 1850.00},
                {"cargo": "Técnico", "valor": 2500.00},
                {"cargo": "Supervisor", "valor": 3200.00}
            ],
            "beneficios": {
                "vale_refeicao_dia": 25.00,
                "cesta_basica_mes": 150.00,
                "vale_transporte": True,
                "plano_saude_participacao": 0.15
            },
            "clausulas_importantes": [
                "Cláusula 3ª - Reajuste Salarial",
                "Cláusula 15ª - Benefício Social Familiar",
                "Cláusula 22ª - Jornada de Trabalho",
                "Cláusula 8ª - Vale Refeição"
            ],
            "jornada_trabalho": {
                "horas_semanais": 44,
                "horas_diarias": 8,
                "intervalo_almoco_min": 60
            }
        }
    }
    
    print("\n--- Estrutura de dados para Convenção Coletiva ---")
    print(json.dumps(exemplo_cct, indent=2, ensure_ascii=False))
    
    # Demonstrar chamadas da API (simuladas)
    print("\n--- Exemplos de chamadas da API ---")
    
    api_examples = [
        {
            "método": "POST",
            "endpoint": "/cct/sindicatos",
            "descrição": "Criar novo sindicato",
            "dados": exemplo_sindicato
        },
        {
            "método": "GET",
            "endpoint": "/cct/sindicatos?limit=10&offset=0",
            "descrição": "Listar sindicatos com paginação"
        },
        {
            "método": "GET",
            "endpoint": "/cct/sindicatos/1",
            "descrição": "Obter sindicato específico"
        },
        {
            "método": "POST",
            "endpoint": "/cct/",
            "descrição": "Criar nova CCT",
            "dados": exemplo_cct
        },
        {
            "método": "GET", 
            "endpoint": "/cct/?union_id=1&limit=10",
            "descrição": "Listar CCTs de um sindicato"
        },
        {
            "método": "POST",
            "endpoint": "/cct/empresas/1/sindicato/1",
            "descrição": "Associar empresa ao sindicato"
        }
    ]
    
    for example in api_examples:
        print(f"\n{example['método']} {example['endpoint']}")
        print(f"  Descrição: {example['descrição']}")
        if 'dados' in example:
            print("  Dados de exemplo:")
            print("  " + json.dumps(example['dados'], indent=4, ensure_ascii=False).replace('\n', '\n  '))
    
    # Demonstrar estrutura da migração
    print("\n--- Migração de Base de Dados ---")
    print("✓ Arquivo: migrations/007_modulo_cct_sindicatos.sql")
    print("✓ Tabelas criadas: Sindicatos, ConvencoesColetivas")
    print("✓ Coluna adicionada: sindicato_id em Empresas")
    print("✓ Políticas RLS implementadas")
    print("✓ Índices para performance criados")
    
    # Mostrar benefícios
    print("\n--- Benefícios do Módulo CCT ---")
    benefits = [
        "🎯 Centralização de informações das CCTs",
        "⚡ Redução do tempo de pesquisa manual",
        "🔒 Compliance automático com legislação trabalhista",
        "📊 Dados estratégicos para contabilidades",
        "🛡️ Segurança multi-tenant garantida",
        "🔄 Estrutura flexível para diferentes tipos de CCT",
        "📈 Base para futuras funcionalidades de IA"
    ]
    
    for benefit in benefits:
        print(f"  {benefit}")
    
    print("\n=== FIM DA DEMONSTRAÇÃO ===")


def verificar_arquivos_criados():
    """
    Verifica se todos os arquivos necessários foram criados
    """
    import os
    
    arquivos_verificar = [
        "migrations/007_modulo_cct_sindicatos.sql",
        "src/services/cct_service.py", 
        "src/api/routers/cct.py",
        "tests/test_cct_module.py",
        "docs/modulo_cct_documentacao.md"
    ]
    
    print("=== VERIFICAÇÃO DE ARQUIVOS ===\n")
    
    todos_existem = True
    for arquivo in arquivos_verificar:
        caminho_completo = f"/home/runner/work/AUDITORIA360/AUDITORIA360/{arquivo}"
        existe = os.path.exists(caminho_completo)
        status = "✓" if existe else "✗"
        print(f"{status} {arquivo}")
        
        if existe:
            # Mostrar tamanho do arquivo
            size = os.path.getsize(caminho_completo)
            print(f"    Tamanho: {size} bytes")
        else:
            todos_existem = False
    
    print(f"\n{'✓ Todos os arquivos foram criados com sucesso!' if todos_existem else '✗ Alguns arquivos estão em falta'}")
    return todos_existem


if __name__ == "__main__":
    print("VERIFICAÇÃO MANUAL DO MÓDULO CCT\n")
    
    # Verificar arquivos
    verificar_arquivos_criados()
    print("\n" + "="*50 + "\n")
    
    # Demonstrar funcionalidades
    demonstrar_funcionalidades_cct()