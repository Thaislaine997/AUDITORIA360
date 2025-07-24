"""
Agente IA autônomo para monitoramento, sugestões de código, geração de relatórios e automação de ações.
"""


# Integração inicial com Gemini (Google Generative AI)
import google.generativeai as genai
from google.generativeai.generative_models import GenerativeModel

class IAAuditoriaAgent:
    """
    Agente IA para:
    - Analisar PRs e sugerir melhorias
    - Gerar tarefas/tickets estruturados
    - Elaborar comunicados via IA
    - Registrar logs e outputs
    """
    def __init__(self, gemini_api_key=None):
        self.gemini_api_key = gemini_api_key
        if gemini_api_key:
            genai.configure(api_key=gemini_api_key) if hasattr(genai, "configure") else None
            self.model = GenerativeModel("gemini-pro")
        else:
            self.model = None

    def analisar_pr(self, pr_data):
        """
        Analisa dados de Pull Request e sugere melhorias via IA Gemini.
        Args:
            pr_data (dict): Dados do PR (título, descrição, diffs, comentários)
        Returns:
            str: Sugestão de melhoria ou resumo IA
        """
        if not self.model:
            raise RuntimeError("Gemini API não configurada")
        prompt = f"""
        Analise o seguinte Pull Request e sugira melhorias, correções ou pontos de atenção:
        {pr_data}
        Responda de forma objetiva e técnica.
        """
        response = self.model.generate_content([prompt])
        return getattr(response, 'text', str(response))

    def gerar_tarefa(self, demanda):
        """
        Gera uma tarefa/ticket estruturado a partir de uma demanda via IA Gemini.
        Args:
            demanda (str): Descrição da demanda
        Returns:
            dict: Tarefa estruturada (título, descrição, prioridade, responsável)
        """
        if not self.model:
            raise RuntimeError("Gemini API não configurada")
        prompt = f"""
        Estruture a seguinte demanda em um ticket de tarefa para equipe de desenvolvimento:
        {demanda}
        Retorne em formato JSON com campos: titulo, descricao, prioridade, responsavel.
        """
        response = self.model.generate_content([prompt])
        import json
        try:
            return json.loads(getattr(response, 'text', str(response)))
        except Exception:
            return {"titulo": demanda, "descricao": demanda, "prioridade": "média", "responsavel": "a definir"}

    def gerar_comunicado(self, tipo, params):
        """
        Gera rascunho de comunicado via Gemini.
        Args:
            tipo (str): Tipo de comunicado
            params (dict): Parâmetros do comunicado
        Returns:
            str: Texto do comunicado
        """
        if not self.model:
            raise RuntimeError("Gemini API não configurada")
        prompt = f"""
        Gere um comunicado do tipo '{tipo}' com os seguintes parâmetros:
        {params}
        O texto deve ser formal, objetivo e pronto para envio ao RH.
        """
        response = self.model.generate_content([prompt])
        # Resposta pode estar em response.text, response.candidates ou response.parts
        if hasattr(response, 'text') and response.text:
            return response.text
        elif hasattr(response, 'candidates') and response.candidates:
            candidate = response.candidates[0]
            if hasattr(candidate, 'content') and hasattr(candidate.content, 'parts'):
                return candidate.content.parts[0].text
        elif hasattr(response, 'parts') and response.parts:
            return response.parts[0].text
        return str(response)

    def registrar_log(self, log_data):
        """
        Registra log de auditoria ou ação relevante via IA Gemini.
        Args:
            log_data (dict): Dados do log (ação, usuário, timestamp, detalhes)
        Returns:
            str: Confirmação ou resumo IA
        """
        if not self.model:
            raise RuntimeError("Gemini API não configurada")
        prompt = f"""
        Gere um registro de log para auditoria com os seguintes dados:
        {log_data}
        Responda com um texto resumido e formal.
        """
        response = self.model.generate_content([prompt])
        return getattr(response, 'text', str(response))
