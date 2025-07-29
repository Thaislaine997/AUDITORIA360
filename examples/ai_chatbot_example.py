"""
Exemplo prático de uso da API de IA e Chatbot do AUDITORIA360.

Este exemplo demonstra:
- Interação com chatbot especializado
- Busca na base de conhecimento
- Geração de recomendações
- Análise de documentos com IA
- Treinamento do chatbot

Requer: requests, openai, python-dotenv
"""

import json
import requests
from typing import Dict, List, Optional


class ChatbotAPI:
    """Cliente para interagir com a API de IA e Chatbot."""
    
    def __init__(self, base_url: str = "http://localhost:8000", token: str = None):
        self.base_url = base_url
        self.token = token
        self.headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}" if token else ""
        }
    
    def chat(self, message: str, context: Optional[Dict] = None) -> Dict:
        """
        Conversa com o chatbot.
        
        Args:
            message: Mensagem do usuário
            context: Contexto adicional (usuário, sessão, etc.)
            
        Returns:
            dict: Resposta do chatbot
        """
        url = f"{self.base_url}/api/v1/ai/chat"
        
        data = {
            "message": message,
            "context": context or {},
            "use_knowledge_base": True,
            "include_sources": True
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"🤖 Chatbot respondeu:")
            print(f"Resposta: {result.get('response', 'N/A')}")
            
            if result.get('confidence'):
                print(f"Confiança: {result['confidence']:.2f}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro no chat: {e}")
            return {"error": str(e)}
    
    def search_knowledge_base(self, query: str, limit: int = 5) -> List[Dict]:
        """
        Busca na base de conhecimento.
        
        Args:
            query: Termo de busca
            limit: Número máximo de resultados
            
        Returns:
            list: Resultados da busca
        """
        url = f"{self.base_url}/api/v1/ai/knowledge-base/search"
        params = {"q": query, "limit": limit}
        
        try:
            response = requests.get(url, params=params, headers=self.headers)
            response.raise_for_status()
            
            results = response.json()
            print(f"🔍 Busca na base de conhecimento:")
            print(f"Encontrados: {len(results)} resultados")
            
            return results
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na busca: {e}")
            return []
    
    def get_recommendations(self, context: Dict) -> List[Dict]:
        """
        Obtém recomendações personalizadas.
        
        Args:
            context: Contexto do usuário/situação
            
        Returns:
            list: Lista de recomendações
        """
        url = f"{self.base_url}/api/v1/ai/recommendations"
        
        try:
            response = requests.post(url, json=context, headers=self.headers)
            response.raise_for_status()
            
            recommendations = response.json()
            print(f"💡 Recomendações obtidas: {len(recommendations)}")
            
            return recommendations
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao obter recomendações: {e}")
            return []
    
    def analyze_document(self, document_id: int, analysis_type: str = "general") -> Dict:
        """
        Analisa documento com IA.
        
        Args:
            document_id: ID do documento
            analysis_type: Tipo de análise (general, compliance, payroll, etc.)
            
        Returns:
            dict: Resultado da análise
        """
        url = f"{self.base_url}/api/v1/ai/analyze-document"
        
        data = {
            "document_id": document_id,
            "analysis_type": analysis_type,
            "include_suggestions": True
        }
        
        try:
            response = requests.post(url, json=data, headers=self.headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"📄 Análise de documento concluída:")
            print(f"Tipo: {analysis_type}")
            print(f"Confiança: {result.get('confidence', 0):.2f}")
            
            return result
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro na análise: {e}")
            return {"error": str(e)}


def example_basic_chat():
    """Exemplo básico de conversa com chatbot."""
    print("\n💬 === EXEMPLO DE CHAT BÁSICO ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = ChatbotAPI(token=token)
    
    # Conversas de exemplo
    conversations = [
        "Como calcular o INSS sobre o salário?",
        "Qual é o prazo para entregar a DIRF?",
        "Quais são as principais mudanças na CLT em 2024?",
        "Como funciona o cálculo de férias?",
        "O que é necessário para demitir um funcionário?"
    ]
    
    chat_session = {
        "session_id": "demo_session_001",
        "user_id": "user_123",
        "user_role": "hr_manager"
    }
    
    for i, message in enumerate(conversations, 1):
        print(f"\n--- Pergunta {i} ---")
        print(f"👤 Usuário: {message}")
        
        response = api.chat(message, context=chat_session)
        
        if "response" in response:
            # Mostrar resposta
            bot_response = response["response"]
            if len(bot_response) > 200:
                bot_response = bot_response[:200] + "..."
            
            print(f"🤖 Bot: {bot_response}")
            
            # Mostrar fontes se disponíveis
            if response.get("sources"):
                print(f"📚 Fontes consultadas:")
                for source in response["sources"][:2]:
                    print(f"- {source.get('title', 'N/A')}")
            
            # Mostrar sugestões de perguntas relacionadas
            if response.get("related_questions"):
                print(f"❓ Perguntas relacionadas:")
                for question in response["related_questions"][:2]:
                    print(f"- {question}")


def example_knowledge_base_search():
    """Exemplo de busca na base de conhecimento."""
    print("\n🔍 === EXEMPLO DE BUSCA NA BASE DE CONHECIMENTO ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = ChatbotAPI(token=token)
    
    # Diferentes tipos de busca
    search_queries = [
        "cálculo de impostos folha de pagamento",
        "convenção coletiva reajuste salarial",
        "procedimentos admissão funcionário",
        "obrigações fiscais empresa",
        "direitos trabalhistas férias"
    ]
    
    for query in search_queries:
        print(f"\n🔎 Buscando: '{query}'")
        
        results = api.search_knowledge_base(query, limit=3)
        
        for i, result in enumerate(results, 1):
            print(f"\n{i}. {result.get('title', 'N/A')}")
            print(f"   Categoria: {result.get('category', 'N/A')}")
            print(f"   Relevância: {result.get('relevance_score', 0):.2f}")
            
            # Mostrar snippet do conteúdo
            content = result.get('content', '')
            if content and len(content) > 150:
                content = content[:150] + "..."
            print(f"   Conteúdo: {content}")


def example_personalized_recommendations():
    """Exemplo de recomendações personalizadas."""
    print("\n💡 === EXEMPLO DE RECOMENDAÇÕES PERSONALIZADAS ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = ChatbotAPI(token=token)
    
    # Diferentes contextos de usuário
    user_contexts = [
        {
            "user_role": "hr_manager",
            "company_size": "medium",
            "industry": "technology",
            "current_issues": ["high_turnover", "payroll_errors"],
            "priority": "compliance"
        },
        {
            "user_role": "accountant",
            "company_size": "small",
            "industry": "retail",
            "current_issues": ["tax_deadlines", "cost_reduction"],
            "priority": "automation"
        },
        {
            "user_role": "ceo",
            "company_size": "large",
            "industry": "manufacturing",
            "current_issues": ["digital_transformation", "audit_preparation"],
            "priority": "strategic"
        }
    ]
    
    for i, context in enumerate(user_contexts, 1):
        print(f"\n--- Recomendações para Usuário {i} ---")
        print(f"Perfil: {context['user_role']} - {context['industry']}")
        print(f"Problemas atuais: {', '.join(context['current_issues'])}")
        
        recommendations = api.get_recommendations(context)
        
        for j, rec in enumerate(recommendations[:3], 1):
            print(f"\n{j}. {rec.get('title', 'N/A')}")
            print(f"   Prioridade: {rec.get('priority', 'N/A')}")
            print(f"   Impacto estimado: {rec.get('impact_score', 0):.1f}/10")
            print(f"   Esforço: {rec.get('effort_level', 'N/A')}")
            
            description = rec.get('description', '')
            if len(description) > 100:
                description = description[:100] + "..."
            print(f"   Descrição: {description}")


def example_document_analysis():
    """Exemplo de análise de documentos com IA."""
    print("\n📄 === EXEMPLO DE ANÁLISE DE DOCUMENTOS ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = ChatbotAPI(token=token)
    
    # Diferentes tipos de análise
    analysis_scenarios = [
        {
            "document_id": 1,
            "analysis_type": "payroll_compliance",
            "description": "Análise de conformidade em demonstrativo de pagamento"
        },
        {
            "document_id": 2,
            "analysis_type": "contract_review",
            "description": "Revisão de contrato de trabalho"
        },
        {
            "document_id": 3,
            "analysis_type": "cct_comparison",
            "description": "Comparação de convenção coletiva"
        }
    ]
    
    for scenario in analysis_scenarios:
        print(f"\n📋 {scenario['description']}")
        
        result = api.analyze_document(
            document_id=scenario["document_id"],
            analysis_type=scenario["analysis_type"]
        )
        
        if "analysis_result" in result:
            analysis = result["analysis_result"]
            
            print(f"✅ Status: {analysis.get('status', 'N/A')}")
            print(f"📊 Score de conformidade: {analysis.get('compliance_score', 0):.1f}/10")
            
            # Mostrar achados principais
            if analysis.get("findings"):
                print(f"\n🔍 Principais achados:")
                for finding in analysis["findings"][:3]:
                    severity = finding.get("severity", "info").upper()
                    print(f"- [{severity}] {finding.get('description', 'N/A')}")
            
            # Mostrar sugestões
            if analysis.get("suggestions"):
                print(f"\n💡 Sugestões de melhoria:")
                for suggestion in analysis["suggestions"][:2]:
                    print(f"- {suggestion.get('action', 'N/A')}")
                    print(f"  Impacto: {suggestion.get('impact', 'N/A')}")


def example_chatbot_training():
    """Exemplo de treinamento e feedback do chatbot."""
    print("\n🎓 === EXEMPLO DE TREINAMENTO DO CHATBOT ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = ChatbotAPI(token=token)
    
    # Adicionar feedback para melhorar respostas
    feedback_data = [
        {
            "conversation_id": "conv_001",
            "user_question": "Como calcular férias?",
            "bot_response": "Para calcular férias...",
            "user_rating": 5,
            "user_feedback": "Resposta muito clara e completa",
            "suggested_improvement": None
        },
        {
            "conversation_id": "conv_002",
            "user_question": "Prazo para DIRF",
            "bot_response": "A DIRF deve ser entregue...",
            "user_rating": 3,
            "user_feedback": "Faltou mencionar as multas por atraso",
            "suggested_improvement": "Incluir informações sobre penalidades"
        }
    ]
    
    feedback_url = f"{api.base_url}/api/v1/ai/feedback"
    
    for feedback in feedback_data:
        print(f"\n📝 Enviando feedback para: {feedback['user_question']}")
        
        try:
            response = requests.post(feedback_url, json=feedback, headers=api.headers)
            response.raise_for_status()
            
            result = response.json()
            print(f"✅ Feedback registrado: ID {result.get('feedback_id', 'N/A')}")
            
            if result.get("training_triggered"):
                print(f"🎯 Treinamento do modelo agendado")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ Erro ao enviar feedback: {e}")
    
    # Adicionar novo conhecimento à base
    new_knowledge = {
        "title": "Cálculo de Adicional Noturno 2024",
        "content": """
        O adicional noturno é de no mínimo 20% sobre a hora diurna.
        
        Horário noturno:
        - Urbano: 22h às 5h (hora reduzida de 52min30s)
        - Rural: 21h às 5h (agricultura) ou 20h às 4h (pecuária)
        
        Cálculo:
        Valor da hora normal × 1,20 × número de horas noturnas
        """,
        "category": "payroll_calculations",
        "tags": ["adicional_noturno", "calculo_folha", "legislacao_2024"],
        "source": "CLT Art. 73",
        "last_updated": "2024-01-15"
    }
    
    knowledge_url = f"{api.base_url}/api/v1/ai/knowledge-base"
    
    try:
        response = requests.post(knowledge_url, json=new_knowledge, headers=api.headers)
        response.raise_for_status()
        
        result = response.json()
        print(f"\n📚 Conhecimento adicionado à base:")
        print(f"ID: {result.get('knowledge_id', 'N/A')}")
        print(f"Categoria: {new_knowledge['category']}")
        print(f"Tags: {', '.join(new_knowledge['tags'])}")
        
    except requests.exceptions.RequestException as e:
        print(f"❌ Erro ao adicionar conhecimento: {e}")


def example_advanced_chat_features():
    """Exemplo de recursos avançados do chatbot."""
    print("\n🚀 === RECURSOS AVANÇADOS DO CHATBOT ===")
    
    token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."
    api = ChatbotAPI(token=token)
    
    # Chat com análise de sentimento e intenção
    advanced_context = {
        "session_id": "advanced_demo",
        "user_id": "power_user",
        "enable_sentiment_analysis": True,
        "enable_intent_detection": True,
        "preferred_response_style": "detailed",
        "user_expertise_level": "intermediate"
    }
    
    complex_questions = [
        "Estou preocupado com uma possível auditoria fiscal, o que devo verificar na folha de pagamento?",
        "Nossa empresa está crescendo rápido, que controles internos você recomenda para RH?",
        "Preciso urgentemente calcular rescisão de um funcionário com 5 anos de empresa",
    ]
    
    for question in complex_questions:
        print(f"\n💭 Pergunta complexa:")
        print(f"'{question}'")
        
        response = api.chat(question, context=advanced_context)
        
        if "response" in response:
            print(f"\n🤖 Resposta:")
            bot_response = response["response"]
            if len(bot_response) > 300:
                bot_response = bot_response[:300] + "..."
            print(bot_response)
            
            # Análise de sentimento
            if response.get("sentiment_analysis"):
                sentiment = response["sentiment_analysis"]
                print(f"\n😊 Sentimento detectado: {sentiment.get('emotion', 'N/A')}")
                print(f"Urgência: {sentiment.get('urgency_level', 'N/A')}")
            
            # Intenção detectada
            if response.get("intent_analysis"):
                intent = response["intent_analysis"]
                print(f"🎯 Intenção: {intent.get('primary_intent', 'N/A')}")
                print(f"Confiança: {intent.get('confidence', 0):.2f}")
            
            # Ações sugeridas
            if response.get("suggested_actions"):
                print(f"\n✅ Ações sugeridas:")
                for action in response["suggested_actions"][:2]:
                    print(f"- {action.get('description', 'N/A')}")
                    print(f"  Prioridade: {action.get('priority', 'N/A')}")


def main():
    """Função principal com todos os exemplos."""
    print("🤖 EXEMPLOS DE USO - API DE IA E CHATBOT AUDITORIA360")
    print("=" * 65)
    
    try:
        example_basic_chat()
        example_knowledge_base_search()
        example_personalized_recommendations()
        example_document_analysis()
        example_chatbot_training()
        example_advanced_chat_features()
        
        print("\n✅ Todos os exemplos executados com sucesso!")
        print("\n📚 Para mais informações, consulte:")
        print("- Documentação da API: http://localhost:8000/docs")
        print("- Manual de IA: docs/tecnico/ai-chatbot-guide.md")
        print("- Base de conhecimento: docs/knowledge-base/")
        
    except Exception as e:
        print(f"\n❌ Erro durante execução: {e}")
        print("Verifique se a API está rodando e o token é válido")


if __name__ == "__main__":
    main()