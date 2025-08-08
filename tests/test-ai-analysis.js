// Basic test for the AI text analysis functionality
// This file can be run with: node test-ai-analysis.js

// Mock data for testing
const mockDocument = {
  id: 1,
  nome: "test-document.pdf",
  texto_extraido: `
    PORTARIA Nº 123/2024
    
    Art. 1º Fica estabelecido o valor do salário mínimo nacional em R$ 1.550,00 (um mil, quinhentos e cinquenta reais), 
    vigente a partir de 1º de janeiro de 2024.
    
    Art. 2º As alíquotas de contribuição para o INSS ficam estabelecidas da seguinte forma:
    I - 7,5% (sete vírgula cinco por cento) para salários de até R$ 1.412,00;
    II - 9% (nove por cento) para salários de R$ 1.412,01 até R$ 2.666,68;
    III - 12% (doze por cento) para salários de R$ 2.666,69 até R$ 4.000,03;
    IV - 14% (quatorze por cento) para salários acima de R$ 4.000,03.
    
    Art. 3º O valor do salário família fica estabelecido em R$ 59,82 (cinquenta e nove reais e oitenta e dois centavos) 
    para dependentes de segurados com remuneração mensal de até R$ 1.819,26.
  `,
  status: 'CONCLUIDO',
  criado_em: new Date().toISOString()
};

// Function to test AI analysis locally
async function testAIAnalysis() {
  console.log('🧪 Testing AI Analysis Function');
  console.log('================================');
  
  const SUPABASE_FUNCTION_URL = process.env.SUPABASE_URL 
    ? `${process.env.SUPABASE_URL}/functions/v1/analisar-texto-com-ia`
    : 'https://your-project.supabase.co/functions/v1/analisar-texto-com-ia';
  
  console.log(`📡 Calling function: ${SUPABASE_FUNCTION_URL}`);
  console.log(`📄 Document: ${mockDocument.nome}`);
  
  try {
    const response = await fetch(SUPABASE_FUNCTION_URL, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${process.env.SUPABASE_ANON_KEY || 'your-anon-key'}`
      },
      body: JSON.stringify({
        record: mockDocument
      })
    });
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const result = await response.json();
    console.log('✅ Function response:', result);
    
    if (result.parametros && result.parametros.length > 0) {
      console.log(`🎯 Extracted ${result.parametros.length} parameters`);
    }
    
  } catch (error) {
    console.error('❌ Test failed:', error.message);
    console.log('💡 Make sure to:');
    console.log('   1. Set SUPABASE_URL and SUPABASE_ANON_KEY environment variables');
    console.log('   2. Deploy the functions with: ./scripts/deploy-functions.sh');
    console.log('   3. Set the GEMINI_API_KEY secret in Supabase');
  }
}

// Run test if this file is executed directly
if (require.main === module) {
  testAIAnalysis();
}

module.exports = { testAIAnalysis, mockDocument };