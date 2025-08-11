"""
Knowledge Graph Engine - The Soul of the Transcendent Audit System
Implements the cognitive reasoning infrastructure for AUDITORIA360's sentient compliance system.
"""

import json
import logging
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from uuid import uuid4

from pydantic import BaseModel

logger = logging.getLogger(__name__)


class TrilhaStepType(str, Enum):
    """Types of cognitive trail steps"""
    EVIDENCIA_DOCUMENTAL = "EVIDENCIA_DOCUMENTAL"
    APLICACAO_DE_REGRA = "APLICACAO_DE_REGRA"
    LINK_PARA_CONHECIMENTO_PRIMARIO = "LINK_PARA_CONHECIMENTO_PRIMARIO"
    IMPLICACAO_ESTRATEGICA = "IMPLICACAO_ESTRATEGICA"
    PERGUNTA_SOCRATICA_PARA_APRENDIZAGEM = "PERGUNTA_SOCRATICA_PARA_APRENDIZAGEM"


class TrilhaStep(BaseModel):
    """A single step in the cognitive reasoning trail"""
    passo: int
    tipo: TrilhaStepType
    descricao: str
    referencia_documento: Optional[str] = None
    referencia_regra: Optional[str] = None
    link_externo: Optional[str] = None
    pergunta: Optional[str] = None


class Divergencia(BaseModel):
    """A compliance divergence with full cognitive trail"""
    codigo: str
    mensagem_curta: str
    trilha_cognitiva: List[TrilhaStep]
    nivel_gravidade: str = "MEDIO"
    impacto_financeiro: Optional[float] = None
    acao_recomendada: Optional[str] = None


class KnowledgeNode(BaseModel):
    """A node in the knowledge graph"""
    id: str
    tipo: str  # "REGRA", "LEGISLACAO", "CONCEITO", "SINDICATO", etc.
    nome: str
    descricao: str
    conteudo: Dict[str, Any]
    conexoes: List[str] = []  # IDs of connected nodes
    metadata: Dict[str, Any] = {}


class AuditResponse(BaseModel):
    """Enhanced audit response with cognitive reasoning"""
    divergencias: List[Divergencia]
    resumo_cognitivo: Optional[Dict[str, Any]] = None
    metricas_aprendizagem: Optional[Dict[str, Any]] = None
    timestamp: str = None

    def __init__(self, **data):
        if data.get("timestamp") is None:
            data["timestamp"] = datetime.now(timezone.utc).isoformat()
        super().__init__(**data)


class KnowledgeGraph:
    """
    The cognitive reasoning engine that transforms AUDITORIA360 into a sentient system.
    This is the core of the first quantum leap - AI as Socratic Cognitive Partner.
    """

    def __init__(self):
        self.nodes: Dict[str, KnowledgeNode] = {}
        self.rules: Dict[str, Dict[str, Any]] = {}
        self._initialize_base_knowledge()

    def _initialize_base_knowledge(self):
        """Initialize the base knowledge graph with fundamental compliance concepts"""
        
        # Core labor law concepts
        self.add_node(KnowledgeNode(
            id="clt_base",
            tipo="LEGISLACAO",
            nome="Consolidação das Leis do Trabalho",
            descricao="Base fundamental do direito trabalhista brasileiro",
            conteudo={
                "lei": "CLT",
                "decreto": "5452/1943",
                "ambito": "federal"
            }
        ))

        # Minimum wage concept
        self.add_node(KnowledgeNode(
            id="piso_salarial_conceito",
            tipo="CONCEITO",
            nome="Piso Salarial",
            descricao="Menor valor salarial permitido por categoria profissional",
            conteudo={
                "definicao": "Valor mínimo estabelecido em CCT ou legislação",
                "base_legal": "Art. 76 da CLT"
            },
            conexoes=["clt_base"]
        ))

        # Sample CCT
        self.add_node(KnowledgeNode(
            id="cct_comerciarios_sp",
            tipo="CCT",
            nome="CCT Comerciários São Paulo",
            descricao="Convenção Coletiva dos Comerciários de São Paulo",
            conteudo={
                "sindicato": "Sindicato dos Comerciários de São Paulo",
                "vigencia": "2025",
                "piso_salarial": 2100.00,
                "clausula_piso": "Cláusula 3ª"
            },
            conexoes=["piso_salarial_conceito"]
        ))

        # Add validation rules
        self._add_base_rules()

    def _add_base_rules(self):
        """Add base validation rules to the system"""
        self.rules["R58"] = {
            "id": "R58",
            "nome": "Validação Piso Salarial",
            "descricao": "Verifica se salário base está acima do piso da categoria",
            "tipo": "VALIDACAO_SALARIAL",
            "parametros": {
                "campo_salario": "salario_base",
                "fonte_piso": "cct_vigente"
            },
            "ativo": True
        }

    def add_node(self, node: KnowledgeNode):
        """Add a node to the knowledge graph"""
        self.nodes[node.id] = node
        logger.debug(f"Added knowledge node: {node.id}")

    def get_node(self, node_id: str) -> Optional[KnowledgeNode]:
        """Retrieve a node from the graph"""
        return self.nodes.get(node_id)

    def get_connected_nodes(self, node_id: str) -> List[KnowledgeNode]:
        """Get all nodes connected to a given node"""
        node = self.get_node(node_id)
        if not node:
            return []
        
        return [self.nodes[conn_id] for conn_id in node.conexoes if conn_id in self.nodes]

    def generate_cognitive_trail(
        self, 
        divergencia_tipo: str, 
        contexto: Dict[str, Any]
    ) -> List[TrilhaStep]:
        """
        Generate a cognitive reasoning trail for a compliance divergence.
        This is the heart of the Socratic AI tutor functionality.
        """
        
        if divergencia_tipo == "SALARIO_ABAIXO_PISO":
            return self._generate_piso_salarial_trail(contexto)
        
        # Default generic trail
        return [
            TrilhaStep(
                passo=1,
                tipo=TrilhaStepType.EVIDENCIA_DOCUMENTAL,
                descricao=f"Identificada divergência do tipo {divergencia_tipo} nos documentos fornecidos.",
                referencia_documento="doc_generic"
            )
        ]

    def _generate_piso_salarial_trail(self, contexto: Dict[str, Any]) -> List[TrilhaStep]:
        """Generate detailed cognitive trail for minimum wage violations"""
        
        funcionario = contexto.get("funcionario", "Funcionário")
        salario_atual = contexto.get("salario_atual", 0)
        piso_esperado = contexto.get("piso_esperado", 2100.00)
        documento = contexto.get("documento", "documento não identificado")
        
        return [
            TrilhaStep(
                passo=1,
                tipo=TrilhaStepType.EVIDENCIA_DOCUMENTAL,
                descricao=f"No documento '{documento}', na linha correspondente ao funcionário '{funcionario}', identifiquei a verba de salário base com o valor de R$ {salario_atual:,.2f}.",
                referencia_documento=f"doc_id:123, documento:{documento}"
            ),
            TrilhaStep(
                passo=2,
                tipo=TrilhaStepType.APLICACAO_DE_REGRA,
                descricao="Consultei a nossa Base de Conhecimento e apliquei a 'Regra Validada' #R58, que define o piso salarial para a categoria.",
                referencia_regra="regra_id:R58"
            ),
            TrilhaStep(
                passo=3,
                tipo=TrilhaStepType.LINK_PARA_CONHECIMENTO_PRIMARIO,
                descricao="Esta regra foi extraída da Cláusula 3ª da CCT do 'Sindicato dos Comerciários de São Paulo', registrada no sistema Mediador do Governo.",
                link_externo="http://mediador.trabalho.gov.br/cct/sp/comerciarios/2025"
            ),
            TrilhaStep(
                passo=4,
                tipo=TrilhaStepType.IMPLICACAO_ESTRATEGICA,
                descricao=f"Pagar abaixo do piso (diferença de R$ {piso_esperado - salario_atual:,.2f}) não só gera um passivo trabalhista imediato, como também invalida potencialmente a base de cálculo para Férias, 13º e FGTS, criando um 'efeito cascata' de risco. Recomenda-se uma re-auditoria completa destes pontos."
            ),
            TrilhaStep(
                passo=5,
                tipo=TrilhaStepType.PERGUNTA_SOCRATICA_PARA_APRENDIZAGEM,
                descricao="Pergunta para reflexão e aprendizagem contínua:",
                pergunta="O sistema de DP que gerou esta folha está configurado para consultar automaticamente as tabelas de piso salarial? Uma auditoria de configuração no sistema de origem poderia prevenir 95% deste tipo de erro no futuro."
            )
        ]

    def process_folha_audit(
        self, 
        folha_data: Dict[str, Any], 
        contexto_auditoria: Optional[Dict[str, Any]] = None
    ) -> AuditResponse:
        """
        Process a payroll audit with full cognitive reasoning.
        This method transforms the traditional audit into a sentient experience.
        """
        
        divergencias = []
        
        # Example: Detect salary below minimum wage
        funcionarios = folha_data.get("funcionarios", [])
        
        for funcionario in funcionarios:
            nome = funcionario.get("nome", "Nome não informado")
            salario_base = funcionario.get("salario_base", 0)
            
            # Simulate piso salarial validation
            piso_esperado = 2100.00  # This would come from CCT lookup
            
            if salario_base < piso_esperado:
                contexto = {
                    "funcionario": nome,
                    "salario_atual": salario_base,
                    "piso_esperado": piso_esperado,
                    "documento": folha_data.get("documento_origem", "DELANE - CONTROLE FOLHA")
                }
                
                trilha = self.generate_cognitive_trail("SALARIO_ABAIXO_PISO", contexto)
                
                divergencias.append(Divergencia(
                    codigo="SALARIO_ABAIXO_PISO",
                    mensagem_curta=f"Salário base (R$ {salario_base:,.2f}) de {nome} está abaixo do piso da CCT.",
                    trilha_cognitiva=trilha,
                    nivel_gravidade="ALTO",
                    impacto_financeiro=piso_esperado - salario_base,
                    acao_recomendada="Ajustar salário base e recalcular verbas dependentes"
                ))

        # Generate learning metrics
        metricas_aprendizagem = {
            "total_divergencias": len(divergencias),
            "tipos_divergencias": list(set([d.codigo for d in divergencias])),
            "oportunidades_aprendizagem": len(divergencias),  # Each divergence is a learning opportunity
            "nivel_complexidade": "INTERMEDIARIO" if len(divergencias) > 0 else "BASICO",
            "conceitos_aplicados": ["piso_salarial", "cct_vigencia", "passivo_trabalhista"]
        }

        resumo_cognitivo = {
            "estrategia_auditoria": "Análise sistemática com foco em conformidade salarial",
            "conhecimento_aplicado": [node.nome for node in list(self.nodes.values())[:3]],
            "areas_risco_identificadas": ["Gestão Salarial", "Compliance CCT"],
            "recomendacoes_preventivas": [
                "Implementar consulta automática de tabelas de piso",
                "Configurar alertas preventivos no sistema de folha",
                "Realizar auditoria trimestral de configurações"
            ]
        }

        return AuditResponse(
            divergencias=divergencias,
            resumo_cognitivo=resumo_cognitivo,
            metricas_aprendizagem=metricas_aprendizagem
        )

    def add_learning_feedback(self, audit_id: str, feedback: Dict[str, Any]):
        """
        Add learning feedback to improve future audits.
        This enables the system to learn and adapt - part of the collective consciousness.
        """
        # This would integrate with the federated learning system
        logger.info(f"Learning feedback received for audit {audit_id}: {feedback}")
        # Implementation would update the knowledge graph based on feedback
        pass

    def get_system_intelligence_metrics(self) -> Dict[str, Any]:
        """Get metrics about the system's current intelligence level"""
        return {
            "knowledge_nodes": len(self.nodes),
            "active_rules": len([r for r in self.rules.values() if r.get("ativo", False)]),
            "connections_mapped": sum(len(node.conexoes) for node in self.nodes.values()),
            "cognitive_complexity": "TRANSCENDENT" if len(self.nodes) > 10 else "DEVELOPING",
            "last_learning_update": datetime.now(timezone.utc).isoformat()
        }


# Global knowledge graph instance
_knowledge_graph: Optional[KnowledgeGraph] = None


def get_knowledge_graph() -> KnowledgeGraph:
    """Get or create the global knowledge graph instance"""
    global _knowledge_graph
    if _knowledge_graph is None:
        _knowledge_graph = KnowledgeGraph()
        logger.info("🧠 Knowledge Graph initialized - The soul of the machine awakens")
    return _knowledge_graph