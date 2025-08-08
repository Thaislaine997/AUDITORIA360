"""
🤖 Serviço de Monitorização Automática de Legislação
Sistema inteligente que busca proativamente por novas CCTs e legislação

O "Web Scraper Vigia" que:
1. Configura fontes de informação para monitorização
2. Executa buscas agendadas automaticamente
3. Procura por novas publicações usando palavras-chave
4. Gera alertas e sugestões de cadastro quando encontra novos documentos

Integra-se perfeitamente com o módulo de Gestão de Legislação do AUDITORIA360
"""

import datetime
import logging
import os
import sys
import json
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
import asyncio

import requests

# Add project root to path
_project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _project_root not in sys.path:
    sys.path.insert(0, _project_root)

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Data directory setup
DATA_DIR = "data/legislacao_updates"
os.makedirs(DATA_DIR, exist_ok=True)

@dataclass
class FonteMonitorizada:
    """Represents a monitored source for legislation"""
    nome: str
    url_base: str
    palavras_chave: List[str]
    ativa: bool = True
    ultimo_check: Optional[datetime.datetime] = None

@dataclass
class NovaLegislacao:
    """Represents newly found legislation"""
    titulo: str
    url: str
    tipo_documento: str
    data_publicacao: str
    orgao_emissor: str
    relevancia_score: float
    fonte: str

class MonitorLegislacao:
    """
    🔍 Monitor Inteligente de Legislação
    
    Implementa a lógica de monitorização automática descrita nos requisitos:
    - Configuração de fontes de informação
    - Busca ativa por novos documentos
    - Geração de alertas contextuais
    """
    
    def __init__(self):
        self.fontes_monitorização = [
            FonteMonitorizada(
                nome="Sistema Mediador MTE",
                url_base="https://www3.mte.gov.br/sistemas/mediador/",
                palavras_chave=["convenção coletiva", "cct", "acordo coletivo"]
            ),
            FonteMonitorizada(
                nome="Diário Oficial da União",
                url_base="https://www.in.gov.br/consulta",
                palavras_chave=["decreto", "lei", "medida provisória", "portaria"]
            ),
            FonteMonitorizada(
                nome="TST - Tribunal Superior do Trabalho",
                url_base="https://www.tst.jus.br/",
                palavras_chave=["súmula", "orientação jurisprudencial", "precedente normativo"]
            )
        ]
        
        # Keywords for client companies (would come from database in production)
        self.clientes_palavras_chave = [
            "comércio", "comerciários", "vendedores",
            "saúde", "hospitalar", "enfermagem", 
            "educação", "docentes", "professores",
            "bancário", "financeiro", "seguros"
        ]
    
    async def executar_monitorizacao_completa(self) -> Dict[str, Any]:
        """
        Executa o ciclo completo de monitorização
        Retorna relatório com novos documentos encontrados e alertas gerados
        """
        hoje = datetime.date.today()
        logger.info(f"🔍 Iniciando monitorização automática - {hoje}")
        
        resultados = {
            "data_execucao": hoje.isoformat(),
            "fontes_verificadas": 0,
            "documentos_encontrados": 0,
            "alertas_gerados": 0,
            "novos_documentos": [],
            "alertas": [],
            "tempo_processamento": 0
        }
        
        inicio = datetime.datetime.now()
        
        try:
            # Simular verificação de cada fonte
            for fonte in self.fontes_monitorização:
                if not fonte.ativa:
                    continue
                    
                logger.info(f"📡 Verificando fonte: {fonte.nome}")
                novos_docs = await self.verificar_fonte(fonte)
                resultados["novos_documentos"].extend(novos_docs)
                resultados["fontes_verificadas"] += 1
                
                # Simulate processing delay
                await asyncio.sleep(0.5)
            
            # Gerar alertas para documentos relevantes
            alertas = self.gerar_alertas_inteligentes(resultados["novos_documentos"])
            resultados["alertas"] = alertas
            
            resultados["documentos_encontrados"] = len(resultados["novos_documentos"])
            resultados["alertas_gerados"] = len(alertas)
            
            # Salvar relatório
            await self.salvar_relatorio_monitorizacao(resultados)
            
        except Exception as e:
            logger.error(f"❌ Erro na monitorização: {e}")
            resultados["erro"] = str(e)
        
        finally:
            fim = datetime.datetime.now()
            resultados["tempo_processamento"] = (fim - inicio).total_seconds()
            
        logger.info(
            f"✅ Monitorização concluída: {resultados['documentos_encontrados']} documentos, "
            f"{resultados['alertas_gerados']} alertas em {resultados['tempo_processamento']:.1f}s"
        )
        
        return resultados
    
    async def verificar_fonte(self, fonte: FonteMonitorizada) -> List[NovaLegislacao]:
        """
        Verifica uma fonte específica por novos documentos
        Em produção, faria scraping real dos sites
        """
        # Mock data for demonstration
        import random
        
        novos_documentos = []
        
        # Simulate finding 0-3 new documents per source
        num_docs = random.randint(0, 3)
        
        for i in range(num_docs):
            # Generate realistic mock document based on source
            if "MTE" in fonte.nome:
                doc = NovaLegislacao(
                    titulo=f"CCT {2024}/{random.randint(100, 999)} - Sindicato dos Comerciários",
                    url=f"{fonte.url_base}documento/{random.randint(10000, 99999)}",
                    tipo_documento="cct",
                    data_publicacao=datetime.date.today().isoformat(),
                    orgao_emissor="Ministério do Trabalho e Emprego",
                    relevancia_score=random.uniform(0.6, 0.95),
                    fonte=fonte.nome
                )
            elif "Diário" in fonte.nome:
                tipos = ["decreto", "lei", "portaria"]
                tipo = random.choice(tipos)
                doc = NovaLegislacao(
                    titulo=f"{tipo.title()} nº {random.randint(10000, 99999)} - Regulamenta disposições trabalhistas",
                    url=f"{fonte.url_base}/documento/{random.randint(1000, 9999)}",
                    tipo_documento=tipo,
                    data_publicacao=datetime.date.today().isoformat(),
                    orgao_emissor="Diário Oficial da União",
                    relevancia_score=random.uniform(0.5, 0.85),
                    fonte=fonte.nome
                )
            else:
                doc = NovaLegislacao(
                    titulo=f"Súmula {random.randint(400, 600)} - Direitos trabalhistas",
                    url=f"{fonte.url_base}/jurisprudencia/{random.randint(1000, 9999)}",
                    tipo_documento="súmula",
                    data_publicacao=datetime.date.today().isoformat(),
                    orgao_emissor="TST",
                    relevancia_score=random.uniform(0.4, 0.8),
                    fonte=fonte.nome
                )
            
            novos_documentos.append(doc)
        
        return novos_documentos
    
    def gerar_alertas_inteligentes(self, documentos: List[NovaLegislacao]) -> List[Dict[str, Any]]:
        """
        Gera alertas contextuais baseados nos documentos encontrados
        Implementa a lógica de "Sugestões de Cadastro" dos requisitos
        """
        alertas = []
        
        for doc in documentos:
            # Só gera alerta para documentos com alta relevância
            if doc.relevancia_score < 0.7:
                continue
                
            # Determinar nível de prioridade baseado no tipo e relevância
            if doc.tipo_documento == "cct" and doc.relevancia_score > 0.9:
                prioridade = "ALTA"
                motivo = "Nova CCT detectada com alta relevância para clientes"
            elif doc.tipo_documento in ["lei", "decreto"] and doc.relevancia_score > 0.8:
                prioridade = "MÉDIA"
                motivo = "Nova legislação pode impactar compliance trabalhista"
            else:
                prioridade = "BAIXA"
                motivo = "Documento encontrado para análise"
            
            alerta = {
                "id": f"ALERTA-{datetime.datetime.now().strftime('%Y%m%d')}-{len(alertas)+1:03d}",
                "prioridade": prioridade,
                "titulo": f"📋 {doc.tipo_documento.upper()} - Novo documento encontrado",
                "descricao": doc.titulo,
                "motivo": motivo,
                "documento": {
                    "titulo": doc.titulo,
                    "url": doc.url,
                    "tipo": doc.tipo_documento,
                    "data_publicacao": doc.data_publicacao,
                    "orgao_emissor": doc.orgao_emissor,
                    "relevancia_score": doc.relevancia_score,
                    "fonte": doc.fonte
                },
                "acoes_sugeridas": [
                    "Analisar documento completo",
                    "Verificar impacto nos clientes",
                    "Cadastrar na base de conhecimento" if doc.relevancia_score > 0.85 else "Marcar para revisão posterior"
                ],
                "criado_em": datetime.datetime.now().isoformat()
            }
            
            alertas.append(alerta)
        
        # Ordenar alertas por prioridade e relevância
        ordem_prioridade = {"ALTA": 0, "MÉDIA": 1, "BAIXA": 2}
        alertas.sort(key=lambda x: (ordem_prioridade[x["prioridade"]], -x["documento"]["relevancia_score"]))
        
        return alertas
    
    async def salvar_relatorio_monitorizacao(self, resultados: Dict[str, Any]):
        """Salva o relatório de monitorização para histórico"""
        hoje = datetime.date.today()
        arquivo_relatorio = os.path.join(DATA_DIR, f"monitorizacao_{hoje.isoformat()}.json")
        
        try:
            with open(arquivo_relatorio, 'w', encoding='utf-8') as f:
                json.dump(resultados, f, ensure_ascii=False, indent=2)
            logger.info(f"📄 Relatório salvo: {arquivo_relatorio}")
        except Exception as e:
            logger.error(f"❌ Erro ao salvar relatório: {e}")

# Legacy functions for compatibility
def buscar_legislacao():
    """Legacy function - runs the new intelligent monitoring"""
    monitor = MonitorLegislacao()
    return asyncio.run(monitor.executar_monitorizacao_completa())

def buscar_legislacao_diaria():
    """Alias para buscar_legislacao para compatibilidade com testes existentes."""
    return buscar_legislacao()

async def main():
    """Main execution function"""
    monitor = MonitorLegislacao()
    resultados = await monitor.executar_monitorizacao_completa()
    
    print("\n" + "="*50)
    print("📊 RELATÓRIO DE MONITORIZAÇÃO")
    print("="*50)
    print(f"📅 Data: {resultados['data_execucao']}")
    print(f"📡 Fontes verificadas: {resultados['fontes_verificadas']}")
    print(f"📋 Documentos encontrados: {resultados['documentos_encontrados']}")
    print(f"🚨 Alertas gerados: {resultados['alertas_gerados']}")
    print(f"⏱️ Tempo de processamento: {resultados['tempo_processamento']:.1f}s")
    
    if resultados["alertas"]:
        print("\n🚨 ALERTAS DE ALTA PRIORIDADE:")
        for alerta in resultados["alertas"][:3]:  # Show top 3 alerts
            print(f"  • {alerta['titulo']}")
            print(f"    {alerta['descricao'][:80]}...")
            print(f"    Relevância: {alerta['documento']['relevancia_score']:.1%}")
    
    print("\n✅ Monitorização concluída com sucesso!")

if __name__ == "__main__":
    asyncio.run(main())
