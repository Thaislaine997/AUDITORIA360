"""
Serviço para gestão de Convenções Coletivas de Trabalho (CCTs) e Sindicatos
Este módulo implementa a lógica de negócio para o novo módulo CCT.
"""

import logging
from typing import Any, Dict, List, Optional

try:
    from config.settings import settings
    from supabase import Client, create_client

    SUPABASE_AVAILABLE = True
except ImportError:
    SUPABASE_AVAILABLE = False
    logging.warning("Supabase not available - install supabase library")

logger = logging.getLogger(__name__)


def get_supabase_client() -> Client:
    """Cria e retorna uma instância do cliente Supabase"""
    if not SUPABASE_AVAILABLE:
        raise ImportError("Supabase library not available")

    try:
        url: str = settings.SUPABASE_URL
        key: str = settings.SUPABASE_SERVICE_KEY
    except Exception:
        # Settings not available in test environment
        raise RuntimeError("Supabase configuration not available")

    return create_client(url, key)


class CCTService:
    """Serviço para gestão de CCTs e Sindicatos"""

    def __init__(self):
        self.client = None
        try:
            if SUPABASE_AVAILABLE:
                self.client = get_supabase_client()
        except Exception as e:
            logger.warning(f"Failed to initialize Supabase client: {e}")
            self.client = None

    # Métodos para Sindicatos
    def criar_sindicato(self, dados_sindicato: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria um novo sindicato
        
        Args:
            dados_sindicato: Dados do sindicato (nome_sindicato, cnpj, etc.)
            
        Returns:
            Dict com os dados do sindicato criado
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            response = self.client.from_("Sindicatos").insert(dados_sindicato).execute()
            
            logger.info(f"Sindicato criado com sucesso: {dados_sindicato.get('nome_sindicato')}")
            return response.data[0] if response.data else {}
            
        except Exception as e:
            logger.error(f"Erro ao criar sindicato: {str(e)}")
            raise

    def listar_sindicatos(self, limit: int = 100, offset: int = 0) -> List[Dict[str, Any]]:
        """
        Lista os sindicatos disponíveis para a contabilidade atual
        
        Args:
            limit: Limite de registos por página
            offset: Offset para paginação
            
        Returns:
            Lista de sindicatos
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            response = (
                self.client
                .from_("Sindicatos")
                .select("*")
                .range(offset, offset + limit - 1)
                .execute()
            )
            
            return response.data or []
            
        except Exception as e:
            logger.error(f"Erro ao listar sindicatos: {str(e)}")
            raise

    def obter_sindicato(self, sindicato_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém um sindicato específico pelo ID
        
        Args:
            sindicato_id: ID do sindicato
            
        Returns:
            Dados do sindicato ou None se não encontrado
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            response = (
                self.client
                .from_("Sindicatos")
                .select("*")
                .eq("id", sindicato_id)
                .execute()
            )
            
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Erro ao obter sindicato {sindicato_id}: {str(e)}")
            raise

    def atualizar_sindicato(self, sindicato_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza um sindicato existente
        
        Args:
            sindicato_id: ID do sindicato
            dados: Novos dados do sindicato
            
        Returns:
            Dados do sindicato atualizado
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            response = (
                self.client
                .from_("Sindicatos")
                .update(dados)
                .eq("id", sindicato_id)
                .execute()
            )
            
            logger.info(f"Sindicato {sindicato_id} atualizado com sucesso")
            return response.data[0] if response.data else {}
            
        except Exception as e:
            logger.error(f"Erro ao atualizar sindicato {sindicato_id}: {str(e)}")
            raise

    # Métodos para Convenções Coletivas
    def criar_convencao_coletiva(self, dados_cct: Dict[str, Any]) -> Dict[str, Any]:
        """
        Cria uma nova convenção coletiva
        
        Args:
            dados_cct: Dados da CCT (sindicato_id, vigencia_inicio, etc.)
            
        Returns:
            Dict com os dados da CCT criada
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            response = self.client.from_("ConvencoesColetivas").insert(dados_cct).execute()
            
            logger.info(f"CCT criada com sucesso: {dados_cct.get('numero_registro_mte')}")
            return response.data[0] if response.data else {}
            
        except Exception as e:
            logger.error(f"Erro ao criar CCT: {str(e)}")
            raise

    def listar_convencoes_coletivas(
        self, 
        sindicato_id: Optional[int] = None,
        limit: int = 100, 
        offset: int = 0
    ) -> List[Dict[str, Any]]:
        """
        Lista as convenções coletivas
        
        Args:
            sindicato_id: ID do sindicato para filtrar (opcional)
            limit: Limite de registos por página
            offset: Offset para paginação
            
        Returns:
            Lista de CCTs
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            query = self.client.from_("ConvencoesColetivas").select("*, Sindicatos(*)")
            
            if sindicato_id:
                query = query.eq("sindicato_id", sindicato_id)
                
            response = query.range(offset, offset + limit - 1).execute()
            
            return response.data or []
            
        except Exception as e:
            logger.error(f"Erro ao listar CCTs: {str(e)}")
            raise

    def obter_convencao_coletiva(self, cct_id: int) -> Optional[Dict[str, Any]]:
        """
        Obtém uma CCT específica pelo ID
        
        Args:
            cct_id: ID da CCT
            
        Returns:
            Dados da CCT ou None se não encontrada
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            response = (
                self.client
                .from_("ConvencoesColetivas")
                .select("*, Sindicatos(*)")
                .eq("id", cct_id)
                .execute()
            )
            
            return response.data[0] if response.data else None
            
        except Exception as e:
            logger.error(f"Erro ao obter CCT {cct_id}: {str(e)}")
            raise

    def atualizar_convencao_coletiva(self, cct_id: int, dados: Dict[str, Any]) -> Dict[str, Any]:
        """
        Atualiza uma CCT existente
        
        Args:
            cct_id: ID da CCT
            dados: Novos dados da CCT
            
        Returns:
            Dados da CCT atualizada
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            response = (
                self.client
                .from_("ConvencoesColetivas")
                .update(dados)
                .eq("id", cct_id)
                .execute()
            )
            
            logger.info(f"CCT {cct_id} atualizada com sucesso")
            return response.data[0] if response.data else {}
            
        except Exception as e:
            logger.error(f"Erro ao atualizar CCT {cct_id}: {str(e)}")
            raise

    # Métodos auxiliares
    def associar_empresa_sindicato(self, empresa_id: int, sindicato_id: int) -> Dict[str, Any]:
        """
        Associa uma empresa a um sindicato
        
        Args:
            empresa_id: ID da empresa
            sindicato_id: ID do sindicato
            
        Returns:
            Dados da empresa atualizada
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            response = (
                self.client
                .from_("Empresas")
                .update({"sindicato_id": sindicato_id})
                .eq("id", empresa_id)
                .execute()
            )
            
            logger.info(f"Empresa {empresa_id} associada ao sindicato {sindicato_id}")
            return response.data[0] if response.data else {}
            
        except Exception as e:
            logger.error(f"Erro ao associar empresa {empresa_id} ao sindicato {sindicato_id}: {str(e)}")
            raise

    def listar_empresas_por_sindicato(self, sindicato_id: int) -> List[Dict[str, Any]]:
        """
        Lista empresas associadas a um sindicato específico
        
        Args:
            sindicato_id: ID do sindicato
            
        Returns:
            Lista de empresas associadas ao sindicato
        """
        if not self.client:
            raise RuntimeError("Supabase client not available")

        try:
            response = (
                self.client
                .from_("Empresas")
                .select("*")
                .eq("sindicato_id", sindicato_id)
                .execute()
            )
            
            return response.data or []
            
        except Exception as e:
            logger.error(f"Erro ao listar empresas do sindicato {sindicato_id}: {str(e)}")
            raise