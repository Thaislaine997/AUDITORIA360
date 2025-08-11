"""
ConhecimentoService - The "Living Library" of AUDITORIA360
Implementation of Phase 1 from the Grand Tomo Architecture

This service transforms the chaos of legislation (PDFs) into structured,
actionable knowledge (JSON), creating intellectual nourishment for all our robots.
"""

import asyncio
import json
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Union
from uuid import UUID

from portal_demandas.db import (
    get_db, 
    LogOperacoesDB,
    DeclaracoesFiscaisDB
)
from portal_demandas.services import DocumentAIClient

logger = logging.getLogger(__name__)


class ConhecimentoService:
    """
    🧠 The "Robot Librarian" - Intelligent Knowledge Management Service
    
    This service implements the complete knowledge extraction and validation workflow:
    1. Upload -> 2. AI Extraction -> 3. Human Validation -> 4. Rule Publication
    
    Philosophy: Transform unstructured legal documents into structured, 
    auditable business rules that feed the entire audit ecosystem.
    """
    
    def __init__(self):
        self.ai_client = DocumentAIClient()
        
    async def iniciar_processamento_cct(
        self, 
        documento_id: int, 
        user_id: UUID, 
        contabilidade_id: int,
        instruction: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Initiate CCT (Collective Bargaining Agreement) processing workflow
        
        Phase 1: Raw AI Extraction
        - Load the document from storage
        - Extract structured data using AI
        - Store raw extractions in ExtracoesIA table
        - Log all operations for audit trail
        
        Args:
            documento_id: ID of the uploaded document
            user_id: UUID of the user initiating the process
            contabilidade_id: ID of the accounting firm
            instruction: Optional specific instruction for AI processing
            
        Returns:
            Dict with status and extracted data summary
        """
        logger.info(f"🔄 Iniciando processamento de CCT para documento {documento_id}")
        
        # Get database session
        with next(get_db()) as db:
            try:
                # 1. Log the start of the operation
                self._log_operacao(
                    db, user_id, contabilidade_id, 
                    'INICIO_PROCESSAMENTO_CCT',
                    f'Documento {documento_id} iniciando extração AI'
                )
                
                # 2. Simulate document loading (in real implementation, load from storage)
                documento_content = self._load_documento_from_storage(documento_id)
                
                # 3. Process with AI using specialized CCT instruction
                ai_instruction = instruction or "Extrair todos os parâmetros da Convenção Coletiva de Trabalho: salários, benefícios, vigência, horas extras, etc."
                
                extracted_data = await self.ai_client.process(documento_content, ai_instruction)
                
                # 4. Store raw extractions in ExtracoesIA table
                extracoes_ids = self._store_ai_extractions(
                    db, documento_id, extracted_data, user_id
                )
                
                # 5. Update document status to "PROCESSADO"
                self._update_document_status(db, documento_id, 'PROCESSADO')
                
                # 6. Log successful completion
                self._log_operacao(
                    db, user_id, contabilidade_id,
                    'PROCESSAMENTO_CCT_CONCLUIDO',
                    f'Documento {documento_id}: {len(extracoes_ids)} extrações criadas'
                )
                
                db.commit()
                
                return {
                    "status": "success",
                    "documento_id": documento_id,
                    "total_extracoes": len(extracoes_ids),
                    "extracoes_ids": extracoes_ids,
                    "proximo_passo": "validacao_humana",
                    "link_validacao": f"/validacao-ia/{documento_id}"
                }
                
            except Exception as e:
                db.rollback()
                logger.error(f"❌ Erro no processamento CCT: {e}")
                
                # Log the error
                self._log_operacao(
                    db, user_id, contabilidade_id,
                    'ERRO_PROCESSAMENTO_CCT',
                    f'Documento {documento_id}: {str(e)}'
                )
                
                return {
                    "status": "error",
                    "documento_id": documento_id,
                    "error": str(e),
                    "retry_available": True
                }
    
    async def validar_e_publicar_regras(
        self, 
        documento_id: int, 
        validacoes: Dict[int, Any], 
        user_id: UUID, 
        contabilidade_id: int
    ) -> Dict[str, Any]:
        """
        Validate AI extractions and publish business rules
        
        Phase 2: Human Validation and Rule Publication
        - Receive validation corrections from ValidationIA page
        - Create validated rules in RegrasValidadas table
        - Update document status to CONCLUIDO
        - Trigger business rule publication events
        
        Args:
            documento_id: ID of the processed document
            validacoes: Dict where key is ExtracoesIA.id and value is corrected data
            user_id: UUID of the validating user
            contabilidade_id: ID of the accounting firm
            
        Returns:
            Dict with publication results
        """
        logger.info(f"✅ Iniciando validação humana para documento {documento_id}")
        
        with next(get_db()) as db:
            try:
                validated_rules = []
                
                # Process each validation
                for extracao_id, valor_corrigido in validacoes.items():
                    # Get original extraction
                    extracao_original = self._get_extracao_by_id(db, extracao_id)
                    if not extracao_original:
                        continue
                    
                    # Create validated rule in RegrasValidadas
                    rule_data = {
                        "documento_id": documento_id,
                        "nome_parametro": extracao_original["nome_parametro"],
                        "valor_parametro": str(valor_corrigido),
                        "tipo_valor": extracao_original["tipo_valor"],
                        "contexto_original": extracao_original["contexto_original"],
                        "validado_por_humano": True,
                        "id_previsao_original": extracao_id,
                        "validado_por": str(user_id),
                        "validado_em": datetime.utcnow()
                    }
                    
                    rule_id = self._criar_regra_validada(db, rule_data)
                    validated_rules.append(rule_id)
                    
                    # Update extraction status
                    self._update_extracao_status(db, extracao_id, 'APROVADO')
                
                # Update document status to CONCLUIDO
                self._update_document_status(db, documento_id, 'CONCLUIDO')
                
                # Log the validation operation
                self._log_operacao(
                    db, user_id, contabilidade_id,
                    'VALIDACAO_HUMANA_CONCLUIDA',
                    f'Documento {documento_id}: {len(validated_rules)} regras publicadas'
                )
                
                # Trigger notification event (in real implementation, use pg_notify)
                self._trigger_notification_event(
                    'REGRAS_PUBLICADAS',
                    {
                        'documento_id': documento_id,
                        'total_regras': len(validated_rules),
                        'contabilidade_id': contabilidade_id
                    }
                )
                
                db.commit()
                
                return {
                    "status": "Regras publicadas e prontas para uso",
                    "documento_id": documento_id,
                    "regras_validadas": len(validated_rules),
                    "rules_ids": validated_rules
                }
                
            except Exception as e:
                db.rollback()
                logger.error(f"❌ Erro na validação: {e}")
                
                self._log_operacao(
                    db, user_id, contabilidade_id,
                    'ERRO_VALIDACAO',
                    f'Documento {documento_id}: {str(e)}'
                )
                
                raise e
    
    def buscar_regras_por_parametro(
        self, 
        nome_parametro: str, 
        contabilidade_id: int,
        empresa_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for validated rules by parameter name
        
        This method feeds the audit engines with validated business rules
        
        Args:
            nome_parametro: Name of the parameter to search for
            contabilidade_id: ID of the accounting firm
            empresa_id: Optional specific company filter
            
        Returns:
            List of validated rules matching the criteria
        """
        with next(get_db()) as db:
            try:
                # In a real implementation, this would query RegrasValidadas table
                # For now, we'll simulate the query
                rules = self._query_regras_validadas(
                    db, nome_parametro, contabilidade_id, empresa_id
                )
                
                logger.info(f"📚 Encontradas {len(rules)} regras para parâmetro '{nome_parametro}'")
                return rules
                
            except Exception as e:
                logger.error(f"❌ Erro na busca de regras: {e}")
                return []
    
    # ========== PRIVATE HELPER METHODS ==========
    
    def _load_documento_from_storage(self, documento_id: int) -> bytes:
        """Load document content from storage system"""
        # In real implementation, this would load from R2/S3 storage
        # For now, simulate PDF content
        return b"PDF_CONTENT_SIMULATION"
    
    def _store_ai_extractions(
        self, 
        db, 
        documento_id: int, 
        extracted_data: Dict[str, Any],
        user_id: UUID
    ) -> List[int]:
        """Store AI extractions in ExtracoesIA table"""
        # In real implementation, this would insert into ExtracoesIA
        # For now, simulate the storage
        extracoes_ids = []
        
        # Extract individual parameters from AI response
        if extracted_data.get("tipo_documento") == "cct":
            parameters = [
                ("piso_salarial", extracted_data.get("piso_salarial"), "DECIMAL"),
                ("vigencia_inicio", extracted_data.get("vigencia_inicio"), "DATE"),
                ("vigencia_fim", extracted_data.get("vigencia_fim"), "DATE"),
                ("adicional_noturno", extracted_data.get("adicional_noturno"), "PERCENTAGE")
            ]
            
            for nome_param, valor_param, tipo_valor in parameters:
                if valor_param is not None:
                    # Simulate insertion and return mock ID
                    extracao_id = len(extracoes_ids) + 1
                    extracoes_ids.append(extracao_id)
        
        return extracoes_ids
    
    def _update_document_status(self, db, documento_id: int, new_status: str):
        """Update document processing status"""
        # In real implementation, this would update Documentos table
        logger.info(f"📝 Documento {documento_id} status atualizado para {new_status}")
    
    def _get_extracao_by_id(self, db, extracao_id: int) -> Optional[Dict[str, Any]]:
        """Get extraction record by ID"""
        # In real implementation, query ExtracoesIA table
        return {
            "id": extracao_id,
            "nome_parametro": "piso_salarial",
            "valor_parametro": "1850.00",
            "tipo_valor": "DECIMAL",
            "contexto_original": "O piso salarial da categoria é de R$ 1.850,00"
        }
    
    def _criar_regra_validada(self, db, rule_data: Dict[str, Any]) -> int:
        """Create validated rule in RegrasValidadas table"""
        # In real implementation, insert into RegrasValidadas
        rule_id = 123  # Mock ID
        logger.info(f"📋 Regra validada criada: {rule_data['nome_parametro']}")
        return rule_id
    
    def _update_extracao_status(self, db, extracao_id: int, new_status: str):
        """Update extraction validation status"""
        # In real implementation, update ExtracoesIA table
        logger.info(f"✅ Extração {extracao_id} status: {new_status}")
    
    def _query_regras_validadas(
        self, 
        db, 
        nome_parametro: str, 
        contabilidade_id: int,
        empresa_id: Optional[int] = None
    ) -> List[Dict[str, Any]]:
        """Query validated rules from RegrasValidadas table"""
        # In real implementation, complex query with joins
        # For now, return mock data
        return [
            {
                "id": 1,
                "nome_parametro": nome_parametro,
                "valor_parametro": "1850.00",
                "tipo_valor": "DECIMAL",
                "validado_em": datetime.utcnow().isoformat(),
                "validado_por": "user123"
            }
        ]
    
    def _log_operacao(
        self, 
        db, 
        user_id: UUID, 
        contabilidade_id: int, 
        operacao: str, 
        detalhes: str
    ):
        """Log operation to LOGOPERACOES table"""
        # In real implementation, insert into LOGOPERACOES
        log_entry = LogOperacoesDB(
            user_id=user_id,
            contabilidade_id=contabilidade_id,
            operacao=operacao,
            tabela_afetada='Documentos',
            detalhes_operacao={"message": detalhes},
            timestamp_operacao=datetime.utcnow(),
            resultado='SUCCESS'
        )
        logger.info(f"📊 LOG: {operacao} - {detalhes}")
    
    def _trigger_notification_event(self, event_type: str, data: Dict[str, Any]):
        """Trigger notification event for background processing"""
        # In real implementation, use pg_notify
        logger.info(f"🔔 Evento disparado: {event_type} - {data}")


# Singleton instance for the application
conhecimento_service = ConhecimentoService()