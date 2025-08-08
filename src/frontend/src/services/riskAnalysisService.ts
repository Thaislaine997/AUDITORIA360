// Risk Analysis Service - Consultor de Riscos API integration
import api from './api';

// Types for Risk Analysis
export interface RiscoDetalhado {
  categoria: string;
  tipo_risco: string;
  descricao: string;
  evidencia: string;
  impacto_potencial: string;
  plano_acao: string;
  severidade: number;
}

export interface AnaliseRiscoResponse {
  empresa_id: number;
  empresa_nome: string;
  score_risco: number;
  nivel_risco: string;
  data_analise: string;
  progresso_analise: Record<string, string>;
  riscos_encontrados: RiscoDetalhado[];
  total_riscos: number;
  riscos_criticos: number;
  riscos_altos: number;
  riscos_medios: number;
  riscos_baixos: number;
  score_anterior?: number;
  variacao_score?: number;
}

export interface HistoricoAnaliseRisco {
  id: number;
  empresa_id: number;
  contabilidade_id: number;
  score_risco: number;
  data_analise: string;
  relatorio_resumo: {
    total_riscos: number;
    nivel_risco: string;
    categorias: Record<string, number>;
  };
}

export interface AnaliseRiscoRequest {
  empresa_id: number;
}

// Risk Analysis API Service Class
export class RiskAnalysisService {
  
  /**
   * Execute comprehensive risk analysis for a company
   * This triggers the "Oracle" - the predictive risk analysis engine
   */
  static async analisarRiscos(request: AnaliseRiscoRequest): Promise<AnaliseRiscoResponse> {
    try {
      console.log(`🔮 Triggering risk analysis for company ${request.empresa_id}...`);
      
      const response = await api.post<AnaliseRiscoResponse>('/riscos/analisar', request);
      
      console.log(`✅ Risk analysis completed: Score ${response.data.score_risco}/100`);
      return response.data;
    } catch (error: any) {
      console.error('❌ Risk analysis failed:', error);
      
      // Enhanced error handling
      if (error.response?.status === 404) {
        throw new Error('Empresa não encontrada. Verifique se o ID está correto.');
      } else if (error.response?.status === 500) {
        throw new Error(`Erro interno na análise: ${error.response.data?.detail || 'Erro desconhecido'}`);
      } else {
        throw new Error(`Falha na análise de riscos: ${error.message}`);
      }
    }
  }

  /**
   * Get risk analysis history for a company
   * Used for trending and evolution tracking
   */
  static async obterHistoricoRiscos(
    empresa_id: number, 
    limit: number = 10
  ): Promise<HistoricoAnaliseRisco[]> {
    try {
      console.log(`📊 Fetching risk history for company ${empresa_id}...`);
      
      const response = await api.get<HistoricoAnaliseRisco[]>(
        `/riscos/historico/${empresa_id}`,
        { params: { limit } }
      );
      
      console.log(`✅ Retrieved ${response.data.length} historical analyses`);
      return response.data;
    } catch (error: any) {
      console.error('❌ Failed to fetch risk history:', error);
      
      if (error.response?.status === 404) {
        throw new Error('Empresa não encontrada.');
      } else {
        throw new Error(`Erro ao buscar histórico: ${error.message}`);
      }
    }
  }

  /**
   * Convert risk severity number to user-friendly text
   */
  static getSeverityLabel(severidade: number): string {
    switch (severidade) {
      case 5: return 'CRÍTICO';
      case 4: return 'ALTO';
      case 3: return 'MÉDIO';
      case 2: return 'BAIXO';
      case 1: return 'INFORMATIVO';
      default: return 'DESCONHECIDO';
    }
  }

  /**
   * Get risk level color for UI display
   */
  static getRiskLevelColor(nivel_risco: string): string {
    switch (nivel_risco) {
      case 'CRÍTICO': return '#EF4444'; // Red
      case 'ALTO': return '#F59E0B'; // Orange
      case 'MÉDIO': return '#F59E0B'; // Yellow
      case 'BAIXO': return '#10B981'; // Green
      default: return '#6B7280'; // Gray
    }
  }

  /**
   * Get risk category icon
   */
  static getCategoryIcon(categoria: string): string {
    switch (categoria) {
      case 'TRABALHISTA': return '👷';
      case 'FISCAL': return '📋';
      case 'OPERACIONAL': return '⚙️';
      case 'CONFORMIDADE': return '✅';
      default: return '⚠️';
    }
  }

  /**
   * Format risk score with appropriate messaging
   */
  static formatScoreMessage(score: number, nivel_risco: string): string {
    if (score >= 90) {
      return `Excelente! Score ${score}/100 - Empresa com práticas exemplares de compliance.`;
    } else if (score >= 80) {
      return `Muito bom! Score ${score}/100 - Poucos riscos identificados.`;
    } else if (score >= 60) {
      return `Atenção! Score ${score}/100 - Alguns riscos requerem ação.`;
    } else if (score >= 40) {
      return `Alerta! Score ${score}/100 - Múltiplos riscos identificados.`;
    } else {
      return `Crítico! Score ${score}/100 - Ação imediata necessária.`;
    }
  }

  /**
   * Calculate risk evolution trend
   */
  static calculateTrend(score_atual: number, score_anterior?: number): {
    trend: 'up' | 'down' | 'stable';
    message: string;
    color: string;
  } {
    if (!score_anterior) {
      return {
        trend: 'stable',
        message: 'Primeira análise',
        color: '#6B7280'
      };
    }

    const diff = score_atual - score_anterior;
    
    if (diff > 5) {
      return {
        trend: 'up',
        message: `+${diff} pontos (melhoria)`,
        color: '#10B981'
      };
    } else if (diff < -5) {
      return {
        trend: 'down', 
        message: `${diff} pontos (deterioração)`,
        color: '#EF4444'
      };
    } else {
      return {
        trend: 'stable',
        message: 'Estável',
        color: '#6B7280'
      };
    }
  }
}

export default RiskAnalysisService;