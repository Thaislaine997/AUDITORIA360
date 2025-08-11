/**
 * ValidationIAPage.tsx - The Human Validation Interface
 * Implementation of the ValidationIA page mentioned in the Grand Tomo Architecture
 * 
 * This component represents the critical human-in-the-loop validation step
 * where experts review and correct AI extractions before they become business rules.
 */

import React, { useState, useEffect } from 'react';

interface AiExtraction {
  id: number;
  nome_parametro: string;
  valor_parametro: string;
  tipo_valor: string;
  contexto_original: string;
  ia_confidence_score: number;
  status_validacao: 'PENDENTE' | 'APROVADO' | 'REJEITADO';
}

interface ValidationIAPageProps {
  documentoId: number;
  contabilidadeId: number;
  userId: string;
}

const ValidationIAPage: React.FC<ValidationIAPageProps> = ({ 
  documentoId, 
  contabilidadeId, 
  userId 
}) => {
  const [extracoes, setExtracoes] = useState<AiExtraction[]>([]);
  const [validacoes, setValidacoes] = useState<Record<number, any>>({});
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    // Simulate loading AI extractions for validation
    const mockExtracoes: AiExtraction[] = [
      {
        id: 1,
        nome_parametro: "piso_salarial",
        valor_parametro: "1850.00",
        tipo_valor: "DECIMAL",
        contexto_original: "O piso salarial da categoria é de R$ 1.850,00 conforme estabelecido na cláusula 5ª.",
        ia_confidence_score: 0.95,
        status_validacao: "PENDENTE"
      },
      {
        id: 2, 
        nome_parametro: "vigencia_inicio",
        valor_parametro: "2024-01-01",
        tipo_valor: "DATE",
        contexto_original: "A presente convenção terá vigência a partir de 1º de janeiro de 2024.",
        ia_confidence_score: 0.98,
        status_validacao: "PENDENTE"
      },
      {
        id: 3,
        nome_parametro: "vale_refeicao",
        valor_parametro: "25.00",
        tipo_valor: "DECIMAL", 
        contexto_original: "Vale-refeição no valor de R$ 25,00 por dia trabalhado.",
        ia_confidence_score: 0.85,
        status_validacao: "PENDENTE"
      },
      {
        id: 4,
        nome_parametro: "adicional_noturno",
        valor_parametro: "25%",
        tipo_valor: "PERCENTAGE",
        contexto_original: "O adicional noturno será de 25% sobre a hora normal.",
        ia_confidence_score: 0.92,
        status_validacao: "PENDENTE"
      }
    ];

    // Simulate API delay
    setTimeout(() => {
      setExtracoes(mockExtracoes);
      setLoading(false);
    }, 1000);
  }, [documentoId]);

  const handleValidationChange = (extracaoId: number, newValue: any) => {
    setValidacoes(prev => ({
      ...prev,
      [extracaoId]: newValue
    }));
  };

  const handleSubmitValidations = async () => {
    setSubmitting(true);
    
    try {
      // Simulate API call to validate and publish rules
      const response = await fetch('/v1/conhecimento/validar-regras', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({
          documento_id: documentoId,
          user_id: userId,
          contabilidade_id: contabilidadeId,
          validacoes: validacoes
        })
      });

      if (response.ok) {
        alert('✅ Regras validadas e publicadas com sucesso! A base de conhecimento foi atualizada.');
        // Redirect to knowledge base or next step
      } else {
        alert('❌ Erro ao validar regras. Tente novamente.');
      }
    } catch (error) {
      console.error('Validation error:', error);
      alert('❌ Erro de comunicação. Verifique sua conexão.');
    } finally {
      setSubmitting(false);
    }
  };

  const getConfidenceColor = (score: number) => {
    if (score >= 0.9) return 'text-green-600';
    if (score >= 0.8) return 'text-yellow-600'; 
    return 'text-red-600';
  };

  const getConfidenceLabel = (score: number) => {
    if (score >= 0.9) return 'Alta Confiança';
    if (score >= 0.8) return 'Média Confiança';
    return 'Baixa Confiança';
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-screen bg-gray-50">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600 mx-auto mb-4"></div>
          <h2 className="text-xl font-semibold text-gray-700">🧠 Processando extrações da IA...</h2>
          <p className="text-gray-500 mt-2">Aguarde enquanto carregamos os dados para validação</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50 py-8">
      <div className="max-w-6xl mx-auto px-4">
        {/* Header */}
        <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold text-gray-900">
                🧠 Validação de IA - The Living Library
              </h1>
              <p className="text-gray-600 mt-2">
                Documento #{documentoId} • Validação Humana de Extrações da IA
              </p>
            </div>
            <div className="text-right">
              <div className="text-sm text-gray-500">
                {extracoes.length} extrações para validar
              </div>
              <div className="text-sm text-blue-600 font-medium">
                Fase 2: Validação Especialista
              </div>
            </div>
          </div>
        </div>

        {/* Instructions */}
        <div className="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
          <div className="flex items-start">
            <div className="text-blue-400 mr-3 mt-1">
              <svg className="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
                <path fillRule="evenodd" d="M18 10a8 8 0 11-16 0 8 8 0 0116 0zm-7-4a1 1 0 11-2 0 1 1 0 012 0zM9 9a1 1 0 000 2v3a1 1 0 001 1h1a1 1 0 100-2v-3a1 1 0 00-1-1H9z" clipRule="evenodd"/>
              </svg>
            </div>
            <div>
              <h3 className="font-medium text-blue-900">Instruções de Validação</h3>
              <p className="text-blue-700 text-sm mt-1">
                Revise cada extração da IA e corrija se necessário. Valores com alta confiança provavelmente estão corretos,
                mas sempre verifique o contexto original. Após validar, as regras serão publicadas na base de conhecimento.
              </p>
            </div>
          </div>
        </div>

        {/* Validation Cards */}
        <div className="space-y-4">
          {extracoes.map((extracao) => (
            <div key={extracao.id} className="bg-white rounded-lg shadow-sm border">
              <div className="p-6">
                <div className="flex items-start justify-between mb-4">
                  <div>
                    <h3 className="text-lg font-semibold text-gray-900">
                      📋 {extracao.nome_parametro.replace('_', ' ').toUpperCase()}
                    </h3>
                    <div className="flex items-center mt-2 space-x-4">
                      <span className="text-sm text-gray-500">ID: {extracao.id}</span>
                      <span className="text-sm text-gray-500">Tipo: {extracao.tipo_valor}</span>
                      <span className={`text-sm font-medium ${getConfidenceColor(extracao.ia_confidence_score)}`}>
                        🎯 {getConfidenceLabel(extracao.ia_confidence_score)} ({(extracao.ia_confidence_score * 100).toFixed(0)}%)
                      </span>
                    </div>
                  </div>
                </div>

                {/* Original Context */}
                <div className="bg-gray-50 rounded-lg p-4 mb-4">
                  <h4 className="font-medium text-gray-700 mb-2">📜 Contexto Original:</h4>
                  <p className="text-gray-600 italic">"{extracao.contexto_original}"</p>
                </div>

                {/* AI Extracted Value */}
                <div className="grid md:grid-cols-2 gap-4">
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      🤖 Valor Extraído pela IA:
                    </label>
                    <div className="bg-yellow-50 border border-yellow-200 rounded-md p-3">
                      <span className="font-mono text-lg">{extracao.valor_parametro}</span>
                    </div>
                  </div>

                  {/* Human Validation Input */}
                  <div>
                    <label className="block text-sm font-medium text-gray-700 mb-2">
                      ✍️ Valor Validado (corrija se necessário):
                    </label>
                    <input
                      type="text"
                      className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
                      placeholder={extracao.valor_parametro}
                      defaultValue={extracao.valor_parametro}
                      onChange={(e) => handleValidationChange(extracao.id, e.target.value)}
                    />
                    <p className="text-xs text-gray-500 mt-1">
                      Deixe em branco para usar o valor da IA
                    </p>
                  </div>
                </div>

                {/* Validation Actions */}
                <div className="flex items-center justify-between mt-4 pt-4 border-t">
                  <div className="flex space-x-2">
                    <button
                      onClick={() => handleValidationChange(extracao.id, extracao.valor_parametro)}
                      className="px-3 py-1 bg-green-100 text-green-700 rounded-full text-sm hover:bg-green-200 transition-colors"
                    >
                      ✅ Aprovar IA
                    </button>
                    <button
                      onClick={() => handleValidationChange(extracao.id, '')}
                      className="px-3 py-1 bg-red-100 text-red-700 rounded-full text-sm hover:bg-red-200 transition-colors"
                    >
                      ❌ Rejeitar
                    </button>
                  </div>
                  <div className="text-xs text-gray-400">
                    {validacoes[extracao.id] !== undefined ? (
                      <span className="text-green-600">✅ Validado</span>
                    ) : (
                      <span>⏳ Aguardando validação</span>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Submit Button */}
        <div className="mt-8 bg-white rounded-lg shadow-sm p-6">
          <div className="flex items-center justify-between">
            <div>
              <h3 className="text-lg font-semibold text-gray-900">Finalizar Validação</h3>
              <p className="text-gray-600 text-sm">
                Publicar regras validadas na base de conhecimento
              </p>
            </div>
            <button
              onClick={handleSubmitValidations}
              disabled={submitting}
              className={`px-6 py-3 rounded-lg font-medium transition-colors ${
                submitting
                  ? 'bg-gray-400 text-white cursor-not-allowed'
                  : 'bg-blue-600 text-white hover:bg-blue-700'
              }`}
            >
              {submitting ? (
                <span className="flex items-center">
                  <svg className="animate-spin -ml-1 mr-3 h-4 w-4 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                  Publicando...
                </span>
              ) : (
                '📚 Publicar Regras na Base de Conhecimento'
              )}
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};

export default ValidationIAPage;