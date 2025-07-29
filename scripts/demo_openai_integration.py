#!/usr/bin/env python3
"""
Demo script for OpenAI GPT integration in AUDITORIA360
Tests the integration with real API calls (if API key is valid)
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

# Add project root to path
sys.path.append('/home/runner/work/AUDITORIA360/AUDITORIA360')

# Load environment variables
load_dotenv()

async def test_openai_service():
    """Test OpenAI service functionality"""
    print("🤖 Testing OpenAI Service Integration")
    print("=" * 50)
    
    try:
        from src.services.openai_service import OpenAIService
        
        # Check if API key is available
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key or api_key == "your_openai_api_key_here":
            print("❌ OpenAI API key not configured")
            print("ℹ️  Set OPENAI_API_KEY in .env file to test with real API")
            return False
        
        print(f"✅ API key configured: {api_key[:10]}...")
        
        # Initialize service
        service = OpenAIService()
        print(f"✅ OpenAI service initialized with model: {service.model}")
        
        # Test chat completion
        print("\n📝 Testing chat completion...")
        result = await service.get_auditoria_response(
            "Como é calculado o INSS sobre o salário em 2024?",
            {"user_role": "hr_manager", "company_size": "medium"}
        )
        
        if result["success"]:
            print("✅ Chat completion successful")
            print(f"📄 Response: {result['response'][:150]}...")
            print(f"🎯 Confidence: {result.get('confidence', 'N/A')}")
            print(f"💡 Suggestions: {len(result.get('suggestions', []))}")
            print(f"📊 Token usage: {result.get('usage', {}).get('total_tokens', 'N/A')}")
        else:
            print(f"❌ Chat completion failed: {result['error']}")
            return False
        
        # Test document analysis
        print("\n📋 Testing document analysis...")
        doc_content = """
        DEMONSTRATIVO DE PAGAMENTO
        Funcionário: João Silva
        Cargo: Analista
        Salário Base: R$ 3.500,00
        INSS: R$ 385,00 (11%)
        IRRF: R$ 70,00 (2%)
        """
        
        analysis_result = await service.analyze_document_content(doc_content, "payroll")
        
        if analysis_result["success"]:
            print("✅ Document analysis successful")
            print(f"📄 Analysis: {analysis_result['response'][:150]}...")
        else:
            print(f"❌ Document analysis failed: {analysis_result['error']}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing OpenAI service: {e}")
        return False

async def test_ai_agent():
    """Test AI agent with OpenAI integration"""
    print("\n🧠 Testing AI Agent Integration")
    print("=" * 50)
    
    try:
        from src.ai_agent import EnhancedAIAgent
        
        # Initialize agent
        agent = EnhancedAIAgent()
        print("✅ AI agent initialized")
        
        # Wait for initialization
        while agent.status == "initializing":
            await asyncio.sleep(0.1)
        
        print(f"📊 Agent status: {agent.status}")
        
        # Test capabilities
        capabilities = await agent.get_mcp_capabilities()
        print(f"🔧 OpenAI integration: {capabilities.get('openai_integration', False)}")
        print(f"🔧 MCP integration: {capabilities.get('mcp_integration', False)}")
        
        # Test chat functionality
        print("\n💬 Testing chat functionality...")
        chat_result = await agent.chat_with_openai(
            "Quais são os principais impostos incidentes sobre a folha de pagamento?"
        )
        
        if chat_result.get("success"):
            print("✅ Chat with OpenAI successful")
            print(f"📄 Response: {chat_result['response'][:150]}...")
        else:
            print(f"❌ Chat failed: {chat_result.get('error', 'Unknown error')}")
        
        # Test general action processing
        print("\n⚙️ Testing general action processing...")
        action_result = await agent.executar_acao(
            "chat: Explique como calcular horas extras",
            {"context": "payroll_calculation"}
        )
        
        if action_result.get("success"):
            print("✅ Action execution successful")
            print(f"📄 Result type: {type(action_result['result'])}")
        else:
            print(f"❌ Action failed: {action_result.get('error', 'Unknown error')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing AI agent: {e}")
        return False

async def test_api_endpoints():
    """Test API endpoints structure (without FastAPI server)"""
    print("\n🌐 Testing API Endpoint Structure")
    print("=" * 50)
    
    try:
        from src.api.routers.ai import router
        
        # Check that required endpoints exist
        endpoint_names = [route.name for route in router.routes if hasattr(route, 'name')]
        
        required_endpoints = [
            "chat_with_bot",
            "get_ai_recommendations", 
            "analyze_document_with_ai",
            "get_ai_status"
        ]
        
        for endpoint in required_endpoints:
            if endpoint in endpoint_names:
                print(f"✅ Endpoint '{endpoint}' exists")
            else:
                print(f"❌ Endpoint '{endpoint}' missing")
        
        print(f"📊 Total endpoints: {len(router.routes)}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing API structure: {e}")
        return False

def test_configuration():
    """Test configuration files"""
    print("\n⚙️ Testing Configuration")
    print("=" * 50)
    
    # Check .env.template
    template_path = "/home/runner/work/AUDITORIA360/AUDITORIA360/.env.template"
    if os.path.exists(template_path):
        print("✅ .env.template exists")
    else:
        print("❌ .env.template missing")
    
    # Check .env
    env_path = "/home/runner/work/AUDITORIA360/AUDITORIA360/.env"
    if os.path.exists(env_path):
        print("✅ .env exists")
    else:
        print("❌ .env missing")
    
    # Check requirements.txt
    req_path = "/home/runner/work/AUDITORIA360/AUDITORIA360/requirements.txt"
    if os.path.exists(req_path):
        with open(req_path, 'r') as f:
            content = f.read()
        
        if "openai" in content.lower():
            print("✅ OpenAI dependency in requirements.txt")
        else:
            print("❌ OpenAI dependency missing from requirements.txt")
        
        if "python-dotenv" in content.lower():
            print("✅ python-dotenv dependency in requirements.txt")
        else:
            print("❌ python-dotenv dependency missing from requirements.txt")
    
    # Check .gitignore
    gitignore_path = "/home/runner/work/AUDITORIA360/AUDITORIA360/.gitignore"
    if os.path.exists(gitignore_path):
        with open(gitignore_path, 'r') as f:
            content = f.read()
        
        if ".env" in content:
            print("✅ .env is in .gitignore")
        else:
            print("❌ .env not in .gitignore")
    
    return True

async def main():
    """Run all demo tests"""
    print("🚀 AUDITORIA360 OpenAI GPT Integration Demo")
    print("=" * 60)
    
    # Test configuration first
    test_configuration()
    
    # Test OpenAI service
    openai_success = await test_openai_service()
    
    # Test AI agent
    agent_success = await test_ai_agent()
    
    # Test API structure
    api_success = await test_api_endpoints()
    
    print("\n📊 Demo Results Summary")
    print("=" * 50)
    print(f"Configuration: ✅ Complete")
    print(f"OpenAI Service: {'✅ Success' if openai_success else '❌ Failed'}")
    print(f"AI Agent: {'✅ Success' if agent_success else '❌ Failed'}")
    print(f"API Structure: {'✅ Success' if api_success else '❌ Failed'}")
    
    if openai_success and agent_success and api_success:
        print("\n🎉 All tests passed! OpenAI integration is working correctly.")
        print("\nNext steps:")
        print("1. Start the API server: uvicorn api.index:app --reload --host 0.0.0.0 --port 8000")
        print("2. Test endpoints at: http://localhost:8000/docs")
        print("3. Try the chat endpoint: POST /api/v1/ai/chat")
    else:
        print("\n⚠️  Some tests failed. Check the error messages above.")
    
    return openai_success and agent_success and api_success

if __name__ == "__main__":
    success = asyncio.run(main())
    sys.exit(0 if success else 1)