"""
Exemplo abrangente de uso do DuckDB com Analytics para AUDITORIA360.

Este exemplo demonstra:
- Análise de folha de pagamento
- Relatórios de compliance
- Análise de tendências
- Agregações complexas
- Performance de queries

Requer: duckdb, pandas, matplotlib, seaborn
"""

from datetime import datetime, timedelta
from pathlib import Path

import duckdb
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


class PayrollAnalytics:
    """Classe para análises de folha de pagamento com DuckDB."""

    def __init__(self, db_path: str = ":memory:"):
        """
        Inicializa conexão com DuckDB.

        Args:
            db_path: Caminho do banco (":memory:" para em memória)
        """
        self.con = duckdb.connect(database=db_path)
        self._setup_sample_data()

    def _setup_sample_data(self):
        """Cria dados de exemplo para demonstração."""
        print("📊 Criando dados de exemplo...")

        # Dados de funcionários
        employees_data = pd.DataFrame(
            {
                "id_funcionario": range(1, 101),
                "nome": [f"Funcionário {i}" for i in range(1, 101)],
                "departamento": np.random.choice(
                    ["RH", "TI", "Financeiro", "Vendas", "Marketing"], 100
                ),
                "cargo": np.random.choice(
                    ["Analista", "Coordenador", "Gerente", "Diretor", "Estagiário"], 100
                ),
                "salario_base": np.random.normal(5000, 2000, 100).round(2),
                "data_admissao": pd.date_range("2020-01-01", "2023-12-31", periods=100),
                "ativo": np.random.choice([True, False], 100, p=[0.9, 0.1]),
            }
        )

        # Dados de folha de pagamento (últimos 12 meses)
        folha_data = []
        base_date = datetime.now() - timedelta(days=365)

        for month in range(12):
            competencia = (base_date + timedelta(days=30 * month)).strftime("%Y-%m")

            for emp_id in employees_data["id_funcionario"]:
                emp = employees_data[employees_data["id_funcionario"] == emp_id].iloc[0]

                # Calcular valores com variações
                salario = emp["salario_base"] * np.random.uniform(0.95, 1.05)
                horas_extras = np.random.uniform(0, 20)
                valor_hora_extra = salario / 220 * 1.5

                folha_data.append(
                    {
                        "id_funcionario": emp_id,
                        "competencia": competencia,
                        "salario_base": salario,
                        "horas_extras": horas_extras,
                        "valor_horas_extras": horas_extras * valor_hora_extra,
                        "vale_transporte": 220.00,
                        "vale_refeicao": 350.00,
                        "plano_saude": 180.00,
                        "inss": salario * 0.11,
                        "irrf": max(0, (salario - 2112) * 0.15),
                        "fgts": salario * 0.08,
                    }
                )

        folha_df = pd.DataFrame(folha_data)

        # Registrar tabelas no DuckDB
        self.con.register("funcionarios", employees_data)
        self.con.register("folha_pagamento", folha_df)

        print(f"✅ Criados {len(employees_data)} funcionários")
        print(f"✅ Criados {len(folha_df)} registros de folha")

    def analise_departamental(self):
        """Análise por departamento."""
        print("\n🏢 === ANÁLISE DEPARTAMENTAL ===")

        query = """
        SELECT 
            f.departamento,
            COUNT(DISTINCT f.id_funcionario) as total_funcionarios,
            AVG(fp.salario_base) as salario_medio,
            SUM(fp.salario_base + fp.valor_horas_extras) as folha_bruta_total,
            AVG(fp.horas_extras) as media_horas_extras,
            SUM(fp.inss + fp.irrf) as total_impostos
        FROM funcionarios f
        JOIN folha_pagamento fp ON f.id_funcionario = fp.id_funcionario
        WHERE f.ativo = true
        GROUP BY f.departamento
        ORDER BY folha_bruta_total DESC
        """

        resultado = self.con.execute(query).fetchdf()

        print("📈 Análise por Departamento:")
        print(resultado.round(2))

        return resultado

    def tendencia_salarial(self):
        """Análise de tendência salarial."""
        print("\n📊 === TENDÊNCIA SALARIAL ===")

        query = """
        SELECT 
            fp.competencia,
            f.departamento,
            AVG(fp.salario_base) as salario_medio,
            COUNT(*) as total_funcionarios,
            SUM(fp.salario_base + fp.valor_horas_extras) as folha_bruta
        FROM funcionarios f
        JOIN folha_pagamento fp ON f.id_funcionario = fp.id_funcionario
        WHERE f.ativo = true
        GROUP BY fp.competencia, f.departamento
        ORDER BY fp.competencia, f.departamento
        """

        resultado = self.con.execute(query).fetchdf()

        # Criar gráfico de tendência
        plt.figure(figsize=(15, 8))

        for dept in resultado["departamento"].unique():
            dept_data = resultado[resultado["departamento"] == dept]
            plt.plot(
                dept_data["competencia"],
                dept_data["salario_medio"],
                marker="o",
                label=dept,
                linewidth=2,
            )

        plt.title("Evolução do Salário Médio por Departamento")
        plt.xlabel("Competência")
        plt.ylabel("Salário Médio (R$)")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True, alpha=0.3)
        plt.tight_layout()

        # Salvar gráfico
        output_dir = Path("/tmp")
        output_dir.mkdir(exist_ok=True)
        plt.savefig(output_dir / "tendencia_salarial.png", dpi=300, bbox_inches="tight")
        print(f"📈 Gráfico salvo em: {output_dir / 'tendencia_salarial.png'}")

        return resultado

    def analise_compliance(self):
        """Análise de compliance fiscal."""
        print("\n⚖️ === ANÁLISE DE COMPLIANCE ===")

        # Verificar limites de INSS
        query_inss = """
        SELECT 
            f.nome,
            f.departamento,
            fp.competencia,
            fp.salario_base,
            fp.inss,
            CASE 
                WHEN fp.salario_base > 7507.49 AND fp.inss > 826.82 THEN 'ERRO: INSS acima do teto'
                WHEN fp.inss != fp.salario_base * 0.11 THEN 'AVISO: Cálculo INSS inconsistente'
                ELSE 'OK'
            END as status_inss
        FROM funcionarios f
        JOIN folha_pagamento fp ON f.id_funcionario = fp.id_funcionario
        WHERE fp.competencia = (SELECT MAX(competencia) FROM folha_pagamento)
        """

        resultado_inss = self.con.execute(query_inss).fetchdf()

        # Contar problemas
        problemas = resultado_inss[resultado_inss["status_inss"] != "OK"]

        print(f"🔍 Verificação de INSS (competência atual):")
        print(f"Total de funcionários: {len(resultado_inss)}")
        print(f"Funcionários com problemas: {len(problemas)}")

        if len(problemas) > 0:
            print(f"\n⚠️ Problemas encontrados:")
            for _, row in problemas.head().iterrows():
                print(f"- {row['nome']}: {row['status_inss']}")

        # Análise de faixa salarial vs IRRF
        query_irrf = """
        SELECT 
            CASE 
                WHEN salario_base <= 2112 THEN 'Isento'
                WHEN salario_base <= 2826.65 THEN 'Faixa 7.5%'
                WHEN salario_base <= 3751.05 THEN 'Faixa 15%'
                WHEN salario_base <= 4664.68 THEN 'Faixa 22.5%'
                ELSE 'Faixa 27.5%'
            END as faixa_irrf,
            COUNT(*) as quantidade,
            AVG(irrf) as irrf_medio,
            AVG(salario_base) as salario_medio
        FROM folha_pagamento
        WHERE competencia = (SELECT MAX(competencia) FROM folha_pagamento)
        GROUP BY 1
        ORDER BY salario_medio
        """

        resultado_irrf = self.con.execute(query_irrf).fetchdf()

        print(f"\n💰 Distribuição por Faixa de IRRF:")
        print(resultado_irrf.round(2))

        return resultado_inss, resultado_irrf

    def analise_custos(self):
        """Análise detalhada de custos."""
        print("\n💸 === ANÁLISE DE CUSTOS ===")

        query = """
        SELECT 
            f.departamento,
            COUNT(DISTINCT f.id_funcionario) as funcionarios,
            SUM(fp.salario_base) as salarios_base,
            SUM(fp.valor_horas_extras) as total_horas_extras,
            SUM(fp.vale_transporte + fp.vale_refeicao) as beneficios,
            SUM(fp.plano_saude) as plano_saude,
            SUM(fp.inss + fp.fgts) as encargos_patronais,
            SUM(fp.salario_base + fp.valor_horas_extras + fp.vale_transporte + 
                fp.vale_refeicao + fp.plano_saude + fp.fgts) as custo_total
        FROM funcionarios f
        JOIN folha_pagamento fp ON f.id_funcionario = fp.id_funcionario
        WHERE fp.competencia = (SELECT MAX(competencia) FROM folha_pagamento)
          AND f.ativo = true
        GROUP BY f.departamento
        ORDER BY custo_total DESC
        """

        resultado = self.con.execute(query).fetchdf()

        # Calcular percentuais
        resultado["custo_por_funcionario"] = (
            resultado["custo_total"] / resultado["funcionarios"]
        )
        resultado["percentual_beneficios"] = (
            resultado["beneficios"] / resultado["custo_total"] * 100
        ).round(1)
        resultado["percentual_encargos"] = (
            resultado["encargos_patronais"] / resultado["custo_total"] * 100
        ).round(1)

        print("💰 Análise de Custos por Departamento:")
        print(resultado.round(2))

        # Criar gráfico de composição de custos
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))

        # Gráfico de barras - custo total por departamento
        ax1.bar(resultado["departamento"], resultado["custo_total"])
        ax1.set_title("Custo Total por Departamento")
        ax1.set_ylabel("Custo Total (R$)")
        ax1.tick_params(axis="x", rotation=45)

        # Gráfico de pizza - composição de custos (total)
        custos_composicao = [
            resultado["salarios_base"].sum(),
            resultado["total_horas_extras"].sum(),
            resultado["beneficios"].sum(),
            resultado["encargos_patronais"].sum(),
        ]
        labels = ["Salários Base", "Horas Extras", "Benefícios", "Encargos"]

        ax2.pie(custos_composicao, labels=labels, autopct="%1.1f%%", startangle=90)
        ax2.set_title("Composição dos Custos Totais")

        plt.tight_layout()
        output_path = Path("/tmp") / "analise_custos.png"
        plt.savefig(output_path, dpi=300, bbox_inches="tight")
        print(f"📊 Gráfico de custos salvo em: {output_path}")

        return resultado

    def relatorio_executivo(self):
        """Gera relatório executivo consolidado."""
        print("\n📋 === RELATÓRIO EXECUTIVO ===")

        # Métricas principais
        query_metricas = """
        SELECT 
            COUNT(DISTINCT f.id_funcionario) as total_funcionarios_ativos,
            AVG(fp.salario_base) as salario_medio,
            SUM(fp.salario_base + fp.valor_horas_extras + fp.vale_transporte + 
                fp.vale_refeicao + fp.plano_saude + fp.fgts) as custo_total_mensal,
            AVG(fp.horas_extras) as media_horas_extras,
            COUNT(DISTINCT f.departamento) as total_departamentos
        FROM funcionarios f
        JOIN folha_pagamento fp ON f.id_funcionario = fp.id_funcionario
        WHERE fp.competencia = (SELECT MAX(competencia) FROM folha_pagamento)
          AND f.ativo = true
        """

        metricas = self.con.execute(query_metricas).fetchdf().iloc[0]

        # Tendência de crescimento
        query_crescimento = """
        SELECT 
            fp.competencia,
            COUNT(DISTINCT f.id_funcionario) as funcionarios,
            SUM(fp.salario_base + fp.valor_horas_extras) as folha_bruta
        FROM funcionarios f
        JOIN folha_pagamento fp ON f.id_funcionario = fp.id_funcionario
        WHERE f.ativo = true
        GROUP BY fp.competencia
        ORDER BY fp.competencia
        """

        crescimento = self.con.execute(query_crescimento).fetchdf()

        # Calcular variação percentual
        if len(crescimento) >= 2:
            var_funcionarios = (
                (
                    crescimento.iloc[-1]["funcionarios"]
                    - crescimento.iloc[0]["funcionarios"]
                )
                / crescimento.iloc[0]["funcionarios"]
                * 100
            )
            var_folha = (
                (
                    crescimento.iloc[-1]["folha_bruta"]
                    - crescimento.iloc[0]["folha_bruta"]
                )
                / crescimento.iloc[0]["folha_bruta"]
                * 100
            )
        else:
            var_funcionarios = var_folha = 0

        print("📊 RESUMO EXECUTIVO - FOLHA DE PAGAMENTO")
        print("=" * 50)
        print(f"👥 Funcionários ativos: {metricas['total_funcionarios_ativos']}")
        print(f"💰 Salário médio: R$ {metricas['salario_medio']:,.2f}")
        print(f"💸 Custo total mensal: R$ {metricas['custo_total_mensal']:,.2f}")
        print(f"⏰ Média horas extras: {metricas['media_horas_extras']:.1f}h/mês")
        print(f"🏢 Departamentos: {metricas['total_departamentos']}")
        print(f"📈 Crescimento funcionários (12m): {var_funcionarios:+.1f}%")
        print(f"📈 Crescimento folha bruta (12m): {var_folha:+.1f}%")

        return {
            "metricas": metricas,
            "crescimento": crescimento,
            "variacao_funcionarios": var_funcionarios,
            "variacao_folha": var_folha,
        }

    def performance_queries(self):
        """Testa performance de queries complexas."""
        print("\n⚡ === TESTE DE PERFORMANCE ===")

        import time

        queries = [
            (
                "Agregação simples",
                """
                SELECT departamento, COUNT(*) as total
                FROM funcionarios 
                GROUP BY departamento
            """,
            ),
            (
                "Join com agregação",
                """
                SELECT f.departamento, AVG(fp.salario_base) as salario_medio
                FROM funcionarios f
                JOIN folha_pagamento fp ON f.id_funcionario = fp.id_funcionario
                GROUP BY f.departamento
            """,
            ),
            (
                "Query complexa com múltiplas condições",
                """
                SELECT 
                    f.departamento,
                    fp.competencia,
                    COUNT(*) as funcionarios,
                    AVG(fp.salario_base) as salario_medio,
                    SUM(fp.valor_horas_extras) as total_extras,
                    AVG(CASE WHEN fp.horas_extras > 10 THEN 1 ELSE 0 END) as pct_com_extras
                FROM funcionarios f
                JOIN folha_pagamento fp ON f.id_funcionario = fp.id_funcionario
                WHERE f.ativo = true
                  AND fp.salario_base > 3000
                GROUP BY f.departamento, fp.competencia
                HAVING COUNT(*) > 2
                ORDER BY fp.competencia, salario_medio DESC
            """,
            ),
        ]

        for nome, query in queries:
            start_time = time.time()
            resultado = self.con.execute(query).fetchdf()
            end_time = time.time()

            print(f"⚡ {nome}:")
            print(f"   Tempo: {(end_time - start_time)*1000:.2f}ms")
            print(f"   Linhas retornadas: {len(resultado)}")

    def close(self):
        """Fecha conexão com o banco."""
        self.con.close()


def main():
    """Função principal com todos os exemplos."""
    print("📊 EXEMPLOS AVANÇADOS - DUCKDB ANALYTICS AUDITORIA360")
    print("=" * 60)

    try:
        # Inicializar analytics
        analytics = PayrollAnalytics()

        # Executar análises
        analytics.analise_departamental()
        analytics.tendencia_salarial()
        analytics.analise_compliance()
        analytics.analise_custos()
        analytics.relatorio_executivo()
        analytics.performance_queries()

        print("\n✅ Todas as análises executadas com sucesso!")
        print("\n📚 Arquivos gerados:")
        print("- /tmp/tendencia_salarial.png")
        print("- /tmp/analise_custos.png")
        print("\n📖 Para mais informações, consulte:")
        print("- Documentação Analytics: docs/tecnico/analytics-guide.md")

        # Fechar conexão
        analytics.close()

    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        import traceback

        traceback.print_exc()


if __name__ == "__main__":
    main()
