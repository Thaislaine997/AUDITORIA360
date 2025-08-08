"""
OpenAI Integration Service for AUDITORIA360
Provides secure and configurable access to OpenAI GPT models
"""

import json
import logging
import os
from typing import Any, Dict, List, Optional

from dotenv import load_dotenv
from openai import AsyncOpenAI

# Load environment variables
load_dotenv()

logger = logging.getLogger(__name__)


class OpenAIService:
    """Service class for OpenAI GPT integration"""

    def __init__(self):
        """Initialize OpenAI service with configuration from environment"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
        self.max_tokens = int(os.getenv("OPENAI_MAX_TOKENS", "2000"))
        self.temperature = float(os.getenv("OPENAI_TEMPERATURE", "0.7"))

        if not self.api_key:
            logger.error("OPENAI_API_KEY not found in environment variables")
            raise ValueError("OpenAI API key is required")

        # Initialize OpenAI client
        self.client = AsyncOpenAI(api_key=self.api_key)

        logger.info(f"OpenAI service initialized with model: {self.model}")

    async def chat_completion(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None,
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Generate chat completion using OpenAI GPT

        Args:
            messages: List of message dictionaries with 'role' and 'content'
            system_prompt: Optional system prompt to set context
            temperature: Override default temperature
            max_tokens: Override default max tokens

        Returns:
            Dict with response, usage info, and metadata
        """
        try:
            # Prepare messages
            chat_messages = []

            # Add system prompt if provided
            if system_prompt:
                chat_messages.append({"role": "system", "content": system_prompt})

            # Add user messages
            chat_messages.extend(messages)

            # Make API call
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=chat_messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens,
            )

            # Extract response
            content = response.choices[0].message.content

            return {
                "response": content,
                "model": response.model,
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens,
                    "completion_tokens": response.usage.completion_tokens,
                    "total_tokens": response.usage.total_tokens,
                },
                "finish_reason": response.choices[0].finish_reason,
                "success": True,
            }

        except Exception as e:
            logger.error(f"Error in OpenAI chat completion: {e}")
            return {"success": False, "error": str(e), "response": None}

    async def get_auditoria_response(
        self, user_message: str, context: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Get specialized response for AUDITORIA360 queries

        Args:
            user_message: User's question or request
            context: Additional context about user/session

        Returns:
            Structured response with answer and metadata
        """
        system_prompt = """Você é um assistente especializado em auditoria, folha de pagamento e direito trabalhista brasileiro.
        
Sua expertise inclui:
- Cálculos de folha de pagamento (INSS, IRRF, FGTS, etc.)
- Convenções coletivas de trabalho (CCTs)
- Legislação trabalhista (CLT, Portarias, etc.)
- Procedimentos de auditoria
- Compliance trabalhista
- Obrigações fiscais e previdenciárias

Responda de forma clara, precisa e baseada na legislação atual. Sempre cite as fontes legais quando aplicável.
Se não souber uma informação específica, seja honesto sobre isso e sugira onde o usuário pode encontrar a resposta."""

        messages = [{"role": "user", "content": user_message}]

        # Add context if provided
        if context:
            context_info = (
                f"Contexto adicional: {json.dumps(context, ensure_ascii=False)}"
            )
            messages.insert(0, {"role": "user", "content": context_info})

        result = await self.chat_completion(
            messages=messages, system_prompt=system_prompt
        )

        if result["success"]:
            # Add AUDITORIA360 specific metadata
            result.update(
                {
                    "source": "OpenAI GPT",
                    "domain": "auditoria_trabalhista",
                    "confidence": 0.85,  # Could be calculated based on response characteristics
                    "suggestions": self._generate_follow_up_suggestions(user_message),
                }
            )

        return result

    def _generate_follow_up_suggestions(self, user_message: str) -> List[str]:
        """Generate follow-up question suggestions based on user message"""
        message_lower = user_message.lower()

        suggestions = []

        if "cálculo" in message_lower or "calcular" in message_lower:
            suggestions.extend(
                [
                    "Como é feito o cálculo do INSS?",
                    "Qual a alíquota do FGTS?",
                    "Como calcular horas extras?",
                ]
            )

        if "cct" in message_lower or "convenção" in message_lower:
            suggestions.extend(
                [
                    "Como comparar diferentes CCTs?",
                    "Quais são os prazos das convenções?",
                    "Como aplicar reajustes da CCT?",
                ]
            )

        if "auditoria" in message_lower:
            suggestions.extend(
                [
                    "Quais documentos são necessários para auditoria?",
                    "Como preparar para fiscalização trabalhista?",
                    "Principais pontos de atenção em auditoria?",
                ]
            )

        # Default suggestions if no specific topic detected
        if not suggestions:
            suggestions = [
                "Como calcular rescisão trabalhista?",
                "Quais são as obrigações mensais do RH?",
                "Como fazer cálculo de férias?",
            ]

        return suggestions[:3]  # Return max 3 suggestions

    async def analyze_document_content(
        self, document_content: str, document_type: str = "general"
    ) -> Dict[str, Any]:
        """
        Analyze document content using OpenAI

        Args:
            document_content: Text content of document
            document_type: Type of document (cct, payroll, contract, etc.)

        Returns:
            Analysis results with insights and recommendations
        """
        analysis_prompts = {
            "cct": "Analise esta convenção coletiva de trabalho. Identifique as principais cláusulas, direitos dos trabalhadores, obrigações do empregador e pontos de atenção para implementação.",
            "payroll": "Analise este demonstrativo de pagamento. Verifique se os cálculos estão corretos, identifique possíveis inconsistências e sugira melhorias.",
            "contract": "Analise este contrato de trabalho. Verifique conformidade com a CLT, identifique cláusulas que podem gerar problemas e sugira adequações.",
            "general": "Analise este documento relacionado à área trabalhista. Identifique pontos importantes, possíveis riscos e recomendações.",
        }

        prompt = analysis_prompts.get(document_type, analysis_prompts["general"])

        messages = [
            {
                "role": "user",
                "content": f"{prompt}\n\nConteúdo do documento:\n{document_content}",
            }
        ]

        result = await self.chat_completion(
            messages=messages,
            system_prompt="Você é um especialista em análise de documentos trabalhistas. Forneça análises detalhadas, identificando pontos críticos e sugerindo ações.",
        )

        if result["success"]:
            result.update(
                {
                    "document_type": document_type,
                    "analysis_type": "openai_gpt",
                    "recommendations_included": True,
                }
            )

        return result

    async def get_recommendations(self, user_context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate personalized recommendations based on user context

        Args:
            user_context: Information about user, company, current issues

        Returns:
            List of personalized recommendations
        """
        context_summary = json.dumps(user_context, ensure_ascii=False, indent=2)

        prompt = f"""Com base no contexto fornecido, gere recomendações práticas e específicas para melhorar os processos de RH e compliance trabalhista.

Contexto:
{context_summary}

Forneça 3-5 recomendações priorizadas, cada uma com:
1. Título da recomendação
2. Descrição detalhada
3. Prioridade (Alta/Média/Baixa)
4. Impacto esperado
5. Recursos necessários"""

        messages = [{"role": "user", "content": prompt}]

        result = await self.chat_completion(
            messages=messages,
            system_prompt="Você é um consultor especialista em RH e compliance trabalhista. Gere recomendações práticas e implementáveis.",
        )

        return result


# Global instance
_openai_service: Optional[OpenAIService] = None


def get_openai_service() -> OpenAIService:
    """Get or create global OpenAI service instance"""
    global _openai_service
    if _openai_service is None:
        _openai_service = OpenAIService()
    return _openai_service


# Test function
async def test_openai_integration():
    """Test OpenAI integration"""
    try:
        service = get_openai_service()

        # Test basic chat
        result = await service.get_auditoria_response(
            "Como calcular o INSS sobre o salário?",
            {"user_role": "hr_manager", "company_size": "medium"},
        )

        print("OpenAI Integration Test:")
        print(f"Success: {result['success']}")
        if result["success"]:
            print(f"Response: {result['response'][:200]}...")
            print(f"Usage: {result['usage']}")
        else:
            print(f"Error: {result['error']}")

    except Exception as e:
        print(f"Test failed: {e}")


if __name__ == "__main__":
    import asyncio

    asyncio.run(test_openai_integration())
