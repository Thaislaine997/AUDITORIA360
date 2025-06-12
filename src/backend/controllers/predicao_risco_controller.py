from typing import Optional, List, Dict, Any
from datetime import date, datetime
import json
import uuid # Para gerar UUIDs, se necessário

# Supondo que google.cloud.bigquery será instalada e configurada
from google.cloud import bigquery

from src.schemas.predicao_risco_schemas import (
    PredicaoRiscoDashboardResponse,
    RiscoPrevistoDetalheSchema,
    DetalhePredicaoRiscoResponse,
    FatorContribuinteTecnicoSchema,
    DadosSuporteVisualizacaoSchema
)

# --- Mock BQUtils e Gemini Utils --- #
# Em um cenário real, estas seriam classes/funções importadas de src.utils
class MockBQUtilsPredicao:
    def __init__(self, client_config: Optional[Dict[str, Any]] = None):
        self.project_id = client_config.get("gcp_project_id", "mock_project") if client_config else "mock_project"
        self.dataset_id = client_config.get("auditoria_folha_dataset", "mock_dataset") if client_config else "mock_dataset"
        print(f"MockBQUtilsPredicao inicializado para {self.project_id}.{self.dataset_id}")

    def executar_query_para_objeto_unico(self, query: str, params: Optional[list] = None) -> Optional[Dict[str, Any]]:
        print(f"MOCK BQ Executando Query (objeto único): {query} com params {params}")
        id_folha_param = None
        if params:
            for p_obj in params: # params é uma lista de objetos ScalarQueryParameter
                if hasattr(p_obj, 'name') and p_obj.name == "id_folha":
                    id_folha_param = p_obj.value
                    break
        
        if id_folha_param == "folha_com_predicao_existente":
            return {
                "score_saude_folha_calculado": 85.0,
                "classe_risco_predita": "MEDIO",
                "detalhamento_riscos_previstos_json": json.dumps([
                    {"id_risco_detalhe": "uuid_risk1", "tipo_risco": "ERRO_CALCULO_INSS", "nome_amigavel_risco": "Risco de Cálculo INSS", "probabilidade": 0.70, "severidade_estimada": "ALTA", "principais_fatores": ["Alta variação salarial", "Muitas rubricas manuais"], "explicacao_explainable_ai": {"feature_comissao_var": 0.6, "feature_num_rubricas_manuais": 0.25}},
                    {"id_risco_detalhe": "uuid_risk2", "tipo_risco": "PARAM_IRRF_DESATUALIZADO", "nome_amigavel_risco": "Parâmetro IRRF Desatualizado", "probabilidade": 0.55, "severidade_estimada": "MEDIA", "principais_fatores": ["Tabela IRRF não atualizada há 60 dias"], "explicacao_explainable_ai": {"feature_dias_ult_att_irrf": 0.7}},
                    {"id_risco_detalhe": "uuid_risk3", "tipo_risco": "FALHA_MAPEAMENTO_RUBRICA_FGTS", "nome_amigavel_risco": "Mapeamento Incorreto Rubrica FGTS", "probabilidade": 0.40, "severidade_estimada": "MEDIA", "principais_fatores": ["Nova rubrica de comissão sem flag FGTS"], "explicacao_explainable_ai": {"feature_nova_rubrica_sem_fgts": 0.5}}
                ]),
                "explicacao_geral_predicao_ia": "A folha apresenta um risco geral MEDIO, principalmente devido a potenciais issues no cálculo de INSS para funcionários comissionados e uma possível desatualização da tabela de IRRF.",
                "features_utilizadas_json": json.dumps({"feature_comissao_var": 1500.0, "feature_num_rubricas_manuais": 5, "feature_dias_ult_att_irrf": 62, "feature_nova_rubrica_sem_fgts": 1}),
                "periodo_referencia": date(2024, 1, 1) 
            }
        return None

class MockGeminiUtilsPredicao:
    def gerar_explicacao_detalhada(self, prompt: str) -> str:
        print(f"MOCK Gemini - Gerando explicação para prompt: {prompt[:200]}...")
        if "Score de Saúde Geral" in prompt:
            return "MOCK GEMINI: O score de saúde geral reflete uma combinação de fatores. As principais áreas de atenção são X e Y. Recomendações: 1. Revisar Z, 2. Validar W."
        elif "risco específico" in prompt:
            return "MOCK GEMINI: Este risco específico é influenciado por A e B. Para mitigar, sugerimos: 1. Fazer C, 2. Analisar D."
        return "MOCK GEMINI: Explicação padrão detalhada."

bq_utils_pred = MockBQUtilsPredicao() # Instância global do mock BQ
gemini_utils_pred = MockGeminiUtilsPredicao() # Instância global do mock Gemini

# --- Controller --- #

class PredicaoRiscoController:
    async def obter_dados_predicao_para_dashboard(
        self,
        id_folha_processada: str,
        id_cliente: str
        # client_config: Dict[str, Any] # Passar a configuração do cliente real
    ) -> Optional[PredicaoRiscoDashboardResponse]:
        """
        Busca os dados de predição mais recentes para uma folha e os formata para o dashboard.
        """
        # Em um cenário real: 
        # client_config_real = get_client_config(id_cliente) # Obter config do cliente
        # bq_utils_real = BQUtils(client_config_real) # Usar a instância real
        
        query = f"""
            SELECT
                score_saude_folha_calculado,
                classe_risco_predita,
                detalhamento_riscos_previstos_json,
                explicacao_geral_predicao_ia,
                periodo_referencia
            FROM `{bq_utils_pred.project_id}.{bq_utils_pred.dataset_id}.PredicoesRiscoFolha`
            WHERE id_folha_processada_fk = @id_folha AND id_cliente = @id_cliente
            ORDER BY timestamp_predicao DESC
            LIMIT 1
        """
        params = [
            bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha_processada),
            bigquery.ScalarQueryParameter("id_cliente", "STRING", id_cliente),
        ]
        
        predicao_raw = bq_utils_pred.executar_query_para_objeto_unico(query, params) # Usando mock

        if not predicao_raw:
            return None

        principais_riscos: List[RiscoPrevistoDetalheSchema] = []
        if predicao_raw.get("detalhamento_riscos_previstos_json"):
            try:
                lista_riscos_detalhados = json.loads(predicao_raw["detalhamento_riscos_previstos_json"])
                for risco_detalhe_dict in lista_riscos_detalhados[:3]: # Pegar os Top 3
                    # Adicionar campos faltantes no mock para o schema RiscoPrevistoDetalheSchema
                    risco_detalhe_dict.setdefault("id_risco_detalhe", str(uuid.uuid4()))
                    risco_detalhe_dict.setdefault("descricao_risco", risco_detalhe_dict.get("nome_amigavel_risco", "Risco não especificado"))
                    risco_detalhe_dict.setdefault("fator_principal", risco_detalhe_dict.get("principais_fatores")[0] if risco_detalhe_dict.get("principais_fatores") else "Não especificado")
                    principais_riscos.append(RiscoPrevistoDetalheSchema(**risco_detalhe_dict))
            except json.JSONDecodeError:
                print(f"Erro ao decodificar detalhamento_riscos_previstos_json para folha {id_folha_processada}")
            except Exception as e:
                print(f"Erro ao processar detalhamento_riscos_previstos_json: {e}")
                
        score_saude_raw = predicao_raw.get("score_saude_folha_calculado")
        score_saude_final = None
        if score_saude_raw is not None:
            try:
                score_saude_final = float(score_saude_raw)
            except ValueError:
                print(f"Não foi possível converter score_saude_folha_calculado '{score_saude_raw}' para float.")

        return PredicaoRiscoDashboardResponse(
            score_saude_folha=score_saude_final,
            classe_risco_geral=predicao_raw.get("classe_risco_predita"),
            principais_riscos_previstos=principais_riscos,
            explicacao_geral_ia=predicao_raw.get("explicacao_geral_predicao_ia"),
            id_folha_processada=id_folha_processada,
            periodo_referencia=predicao_raw.get("periodo_referencia", date.today())
        )

    async def obter_detalhes_aprofundados_predicao(
        self,
        id_folha_processada: str,
        id_cliente: str,
        tipo_detalhe: str,
        id_risco_detalhe: Optional[str] = None
        # client_config: Dict[str, Any] # Passar config real
    ) -> Optional[DetalhePredicaoRiscoResponse]:
        
        # Em um cenário real:
        # client_config_real = get_client_config(id_cliente)
        # bq_utils_real = BQUtils(client_config_real)
        # gemini_utils_real = GeminiUtils(client_config_real) # ou similar
        
        query_pred_completa = f"""
            SELECT *
            FROM `{bq_utils_pred.project_id}.{bq_utils_pred.dataset_id}.PredicoesRiscoFolha`
            WHERE id_folha_processada_fk = @id_folha AND id_cliente = @id_cliente
            ORDER BY timestamp_predicao DESC LIMIT 1
        """
        params_pred = [
           bigquery.ScalarQueryParameter("id_folha", "STRING", id_folha_processada),
           bigquery.ScalarQueryParameter("id_cliente", "STRING", id_cliente)
        ]
        predicao_completa_raw = bq_utils_pred.executar_query_para_objeto_unico(query_pred_completa, params_pred)

        if not predicao_completa_raw:
            return None

        fatores_tecnicos: List[FatorContribuinteTecnicoSchema] = []
        explicacao_foco_ia = ""
        risco_foco_obj: Optional[RiscoPrevistoDetalheSchema] = None
        dados_para_grafico: List[DadosSuporteVisualizacaoSchema] = []
        recomendacoes: List[str] = []

        features_usadas = {}
        if predicao_completa_raw.get("features_utilizadas_json"):
            try: features_usadas = json.loads(predicao_completa_raw["features_utilizadas_json"])
            except json.JSONDecodeError: pass
        
        riscos_detalhados_lista_raw = []
        if predicao_completa_raw.get("detalhamento_riscos_previstos_json"):
            try: riscos_detalhados_lista_raw = json.loads(predicao_completa_raw["detalhamento_riscos_previstos_json"])
            except json.JSONDecodeError: pass

        prompt_contexto_base_gemini = f"""
            Contexto da Folha (ID: {id_folha_processada}, Cliente: {id_cliente}, Período: {predicao_completa_raw.get('periodo_referencia')}):
            Score de Saúde Calculado: {predicao_completa_raw.get('score_saude_folha_calculado')}
            Classe de Risco Geral Predita: {predicao_completa_raw.get('classe_risco_predita')}
            Explicação Geral da IA (anterior): {predicao_completa_raw.get('explicacao_geral_predicao_ia')}
            Features da folha que foram enviadas ao modelo de risco: {json.dumps(features_usadas, indent=2)}
        """

        if tipo_detalhe == "score_geral":
            # Para o score geral, os fatores podem ser uma agregação ou os fatores dos top N riscos
            for risco_obj_raw in riscos_detalhados_lista_raw[:2]: # Exemplo: fatores dos top 2 riscos
                if risco_obj_raw.get("explicacao_explainable_ai"):
                    for feature, impacto in risco_obj_raw.get("explicacao_explainable_ai", {}).items():
                        fatores_tecnicos.append(FatorContribuinteTecnicoSchema(
                            feature=feature, 
                            valor=features_usadas.get(feature, "N/D"), 
                            atribuicao_impacto=impacto
                        ))
            prompt_gemini_detalhe = f"""
                {prompt_contexto_base_gemini}
                O usuário pediu detalhes sobre o Score de Saúde Geral ({predicao_completa_raw.get('score_saude_folha_calculado')}).
                Com base em todos os riscos previstos (resumidos abaixo) e nos fatores técnicos,
                gere uma explicação detalhada em linguagem natural sobre o que compõe este score e quais são as principais áreas de atenção.
                Forneça 2-3 recomendações gerais acionáveis.
                Riscos Detalhados: {json.dumps(riscos_detalhados_lista_raw, indent=2)}
            """
            explicacao_foco_ia = gemini_utils_pred.gerar_explicacao_detalhada(prompt_gemini_detalhe) # Usando mock
            recomendacoes = ["Revisar parametrizações críticas do sistema.", "Realizar treinamentos periódicos com a equipe de RH."]

        elif tipo_detalhe == "risco_especifico" and id_risco_detalhe:
            risco_especifico_raw = next((r for r in riscos_detalhados_lista_raw if r.get("id_risco_detalhe") == id_risco_detalhe), None)
            if risco_especifico_raw:
                # Garantir que todos os campos necessários para RiscoPrevistoDetalheSchema estão presentes
                risco_especifico_raw.setdefault("descricao_risco", risco_especifico_raw.get("nome_amigavel_risco", "Risco não especificado"))
                risco_especifico_raw.setdefault("fator_principal", risco_especifico_raw.get("principais_fatores")[0] if risco_especifico_raw.get("principais_fatores") else "Não especificado")
                risco_foco_obj = RiscoPrevistoDetalheSchema(**risco_especifico_raw)
                
                if risco_especifico_raw.get("explicacao_explainable_ai"):
                     for feature, impacto in risco_especifico_raw.get("explicacao_explainable_ai", {}).items():
                        fatores_tecnicos.append(FatorContribuinteTecnicoSchema(
                            feature=feature, 
                            valor=features_usadas.get(feature, "N/D"), 
                            atribuicao_impacto=impacto
                        ))
                
                prompt_gemini_detalhe = f"""
                    {prompt_contexto_base_gemini}
                    O usuário pediu detalhes sobre o seguinte risco específico:
                    - ID Risco: {risco_foco_obj.id_risco_detalhe}
                    - Descrição: {risco_foco_obj.descricao_risco}
                    - Probabilidade Estimada: {risco_foco_obj.probabilidade_estimada}
                    - Severidade Estimada: {risco_foco_obj.severidade_estimada}
                    - Fator Principal (manual): {risco_foco_obj.fator_principal}
                    - Fatores Técnicos (do Explainable AI, se disponíveis): {json.dumps(risco_especifico_raw.get("explicacao_explainable_ai"), indent=2)}
                    
                    Explique este risco em linguagem natural para um usuário de RH, detalhando por que ele pode ocorrer com base nos fatores técnicos e nas features da folha.
                    Forneça 2-3 recomendações específicas e acionáveis para mitigar este risco.
                """
                explicacao_foco_ia = gemini_utils_pred.gerar_explicacao_detalhada(prompt_gemini_detalhe) # Usando mock
                recomendacoes = [
                    f"Para o risco '{risco_foco_obj.descricao_risco}', verifique o fator: {risco_foco_obj.fator_principal}.", 
                    "Analise as rubricas relacionadas e os parâmetros do sistema."
                ]

                # Exemplo de como adicionar dados para visualização contextual
                if risco_foco_obj.descricao_risco and "comissao" in risco_foco_obj.descricao_risco.lower() and "feature_comissao_var" in features_usadas:
                    dados_para_grafico.append(DadosSuporteVisualizacaoSchema(
                        tipo_grafico="VALOR_SIMPLES", 
                        titulo_grafico="Variação da Comissão (Feature Usada no Modelo)",
                        dados={"label": "Variação de Comissão", "valor": features_usadas["feature_comissao_var"]}
                    ))
            else:
                return None # Risco específico não encontrado
        else:
             return None # Tipo de detalhe inválido ou id_risco_detalhe faltando

        score_saude_final_detalhe = None
        score_saude_raw_detalhe = predicao_completa_raw.get("score_saude_folha_calculado")
        if score_saude_raw_detalhe is not None:
            try: score_saude_final_detalhe = float(score_saude_raw_detalhe)
            except ValueError: pass

        return DetalhePredicaoRiscoResponse(
            id_folha_processada=id_folha_processada,
            risco_selecionado=risco_foco_obj,
            score_saude_folha=score_saude_final_detalhe,
            classe_risco_geral=predicao_completa_raw.get("classe_risco_predita"),
            fatores_contribuintes_tecnicos=fatores_tecnicos,
            explicacao_detalhada_ia=explicacao_foco_ia,
            dados_suporte_visualizacao=dados_para_grafico if dados_para_grafico else None,
            recomendacoes_ia=recomendacoes if recomendacoes else None
        )

# Instância do controller para ser usada nas rotas
predicao_risco_controller = PredicaoRiscoController()
