#!/usr/bin/env python3
"""
Demo script for AI Development Assistant
Shows the assistant functionality with mock responses
"""

import asyncio
import json
from typing import Dict, Any
import time

class MockAIBrain:
    """Mock AI brain for demonstration purposes"""
    
    def __init__(self):
        print("🧠 Inicializando Demo do Cérebro da IA de Desenvolvimento...")
        self.knowledge_base = {
            "auth": "O sistema de autenticação está em src/api/routers/auth.py usando JWT tokens",
            "routers": "A API usa FastAPI com routers modulares em src/api/routers/. Cada funcionalidade tem seu próprio router.",
            "frontend": "Frontend em React com TypeScript, usando Material-UI para componentes",
            "database": "Sistema usa SQLAlchemy para ORM, com suporte a PostgreSQL e SQLite",
            "structure": "Arquitetura modular: api/ para backend, src/frontend/ para React, ia_desenvolvimento/ para IA"
        }
    
    def fazer_pergunta(self, pergunta: str) -> Dict[str, Any]:
        """Simulate AI response based on keywords"""
        pergunta_lower = pergunta.lower()
        
        # Find relevant knowledge
        resposta = "Com base na análise do código do AUDITORIA360:\n\n"
        sources = []
        
        if any(word in pergunta_lower for word in ["auth", "autenticação", "login", "jwt"]):
            resposta += self.knowledge_base["auth"]
            sources.append({"file": "src/api/routers/auth.py", "type": ".py"})
            
        elif any(word in pergunta_lower for word in ["router", "api", "endpoint"]):
            resposta += self.knowledge_base["routers"]
            sources.append({"file": "api/index.py", "type": ".py"})
            sources.append({"file": "src/api/routers/", "type": "directory"})
            
        elif any(word in pergunta_lower for word in ["frontend", "react", "tsx", "componente"]):
            resposta += self.knowledge_base["frontend"]
            sources.append({"file": "src/frontend/src/pages/", "type": "directory"})
            
        elif any(word in pergunta_lower for word in ["database", "banco", "sql", "orm"]):
            resposta += self.knowledge_base["database"]
            sources.append({"file": "src/models.py", "type": ".py"})
            
        elif any(word in pergunta_lower for word in ["estrutura", "arquitetura", "organização"]):
            resposta += self.knowledge_base["structure"]
            sources.append({"file": "src/", "type": "directory"})
            sources.append({"file": "api/", "type": "directory"})
            
        else:
            resposta += f"""Analisando sua pergunta: "{pergunta}"

O projeto AUDITORIA360 é um sistema completo de auditoria e compliance com:

🏗️ **Arquitetura:**
- Backend: FastAPI com Python
- Frontend: React + TypeScript + Material-UI  
- Base de dados: SQLAlchemy (PostgreSQL/SQLite)
- IA: Assistentes integrados para automação

📁 **Estrutura principal:**
- `api/` - Aplicação FastAPI principal
- `src/` - Código fonte modular
- `src/frontend/` - Aplicação React
- `ia_desenvolvimento/` - Este assistente de IA

Para perguntas específicas, tente mencionar: auth, routers, frontend, database, ou estrutura.
"""
            sources.append({"file": "README.md", "type": ".md"})
        
        return {
            "resposta": resposta,
            "status": "success",
            "timestamp": time.time(),
            "sources": sources
        }
    
    def get_status(self) -> Dict[str, Any]:
        """Get mock status"""
        return {
            "database_exists": True,
            "retrieval_ready": True,
            "files_processed": 127,
            "last_training": time.time() - 3600,  # 1 hour ago
            "message": "✅ Assistente ativo (DEMO MODE)"
        }


async def demo_conversation():
    """Demo conversation with the AI assistant"""
    brain = MockAIBrain()
    
    print("\n" + "="*80)
    print("🎯 DEMONSTRAÇÃO - ASSISTENTE DE DESENVOLVIMENTO AUDITORIA360")
    print("="*80)
    
    # Show status
    status = brain.get_status()
    print(f"\n📊 STATUS: {status['message']}")
    print(f"📁 Arquivos processados: {status['files_processed']}")
    
    # Demo questions
    questions = [
        "Como funciona a estrutura de routers da API?",
        "Explique o sistema de autenticação",
        "Como está organizado o frontend React?",
        "Que tipo de banco de dados é usado?",
        "Me fale sobre a arquitetura geral do projeto"
    ]
    
    for i, question in enumerate(questions, 1):
        print(f"\n🤔 PERGUNTA {i}: {question}")
        print("-" * 50)
        
        # Simulate thinking time
        print("🧠 Analisando código...")
        await asyncio.sleep(0.5)
        
        # Get response
        response = brain.fazer_pergunta(question)
        
        print(f"💬 RESPOSTA:\n{response['resposta']}")
        
        if response['sources']:
            print(f"\n📚 FONTES CONSULTADAS:")
            for source in response['sources']:
                print(f"  • {source['file']} ({source['type']})")
        
        print()
        await asyncio.sleep(1)
    
    print("\n" + "="*80)
    print("✅ DEMONSTRAÇÃO CONCLUÍDA")
    print("="*80)
    print("""
🎉 O Assistente de Desenvolvimento está funcionando!

📋 PRÓXIMOS PASSOS:
1. Configure OPENAI_API_KEY para funcionalidade completa
2. Acesse http://localhost:8000/api/v1/dev-assistant/status
3. Use a interface web em DevAssistantPage.tsx
4. Faça perguntas específicas sobre o código

🔧 ENDPOINTS DISPONÍVEIS:
- GET /api/v1/dev-assistant/status - Status do sistema
- POST /api/v1/dev-assistant/query - Fazer perguntas
- POST /api/v1/dev-assistant/retrain - Retreinar IA
- GET /api/v1/dev-assistant/health - Health check

🧠 Este é seu "meta-cérebro" - uma IA treinada no seu próprio código!
""")


if __name__ == "__main__":
    asyncio.run(demo_conversation())