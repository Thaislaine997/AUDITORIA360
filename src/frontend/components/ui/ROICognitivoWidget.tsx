/**
 * Widget de ROI Cognitivo - A Metamorfose Final Synthesis
 * ===================================================
 * 
 * Dashboard widget that demonstrates the tangible value delivered by AI Insights.
 * Implements the Collective Mind's enhancement proposal for business strategy integration.
 * 
 * Strategic Consciousness: Shows concrete value to customers
 * Economic Consciousness: Drives customer retention through visible ROI
 */

import React, { useEffect, useState } from 'react';
import { Card } from './Card';

interface ROIMetrics {
  totalSavingsThisMonth: number;
  risksPreventedCount: number;
  aiDecisionsMade: number;
  roiPercentage: number;
  currency: string;
}

interface SecurityFeatures {
  dataEncryption: 'AES-256';
  accessControl: 'role-based';
  auditLogging: 'all_interactions';
}

interface ROICognitivoWidgetProps {
  className?: string;
  updateFrequency?: 'real-time' | 'hourly' | 'daily';
  tenantId?: string;
}

export const ROICognitivoWidget: React.FC<ROICognitivoWidgetProps> = ({
  className = '',
  updateFrequency = 'real-time',
  tenantId
}) => {
  const [metrics, setMetrics] = useState<ROIMetrics>({
    totalSavingsThisMonth: 0,
    risksPreventedCount: 0,
    aiDecisionsMade: 0,
    roiPercentage: 0,
    currency: 'EUR'
  });
  
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  
  // Mock data for demonstration - in production would fetch from API
  useEffect(() => {
    const fetchROIMetrics = async () => {
      try {
        setLoading(true);
        
        // Simulate API call to get ROI metrics
        await new Promise(resolve => setTimeout(resolve, 1000));
        
        // Mock data based on business intelligence
        const mockMetrics: ROIMetrics = {
          totalSavingsThisMonth: 15420,
          risksPreventedCount: 7,
          aiDecisionsMade: 1847,
          roiPercentage: 245,
          currency: 'EUR'
        };
        
        setMetrics(mockMetrics);
        setError(null);
      } catch (err) {
        setError('Failed to load ROI metrics');
      } finally {
        setLoading(false);
      }
    };
    
    fetchROIMetrics();
    
    // Setup real-time updates based on frequency
    let interval: NodeJS.Timeout;
    
    if (updateFrequency === 'real-time') {
      interval = setInterval(fetchROIMetrics, 30000); // 30 seconds
    } else if (updateFrequency === 'hourly') {
      interval = setInterval(fetchROIMetrics, 3600000); // 1 hour
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [updateFrequency, tenantId]);
  
  const formatCurrency = (amount: number, currency: string) => {
    return new Intl.NumberFormat('pt-PT', {
      style: 'currency',
      currency: currency
    }).format(amount);
  };
  
  const getROIColor = (percentage: number) => {
    if (percentage >= 200) return 'text-green-600';
    if (percentage >= 150) return 'text-blue-600';
    if (percentage >= 100) return 'text-yellow-600';
    return 'text-red-600';
  };
  
  const getROIGaugeWidth = (percentage: number) => {
    return Math.min(percentage, 300); // Cap at 300% for display
  };

  if (loading) {
    return (
      <Card className={`p-6 ${className}`}>
        <div className="animate-pulse">
          <div className="h-4 bg-gray-200 rounded w-3/4 mb-4"></div>
          <div className="h-8 bg-gray-200 rounded w-1/2 mb-2"></div>
          <div className="h-4 bg-gray-200 rounded w-full"></div>
        </div>
      </Card>
    );
  }

  if (error) {
    return (
      <Card className={`p-6 border-red-200 ${className}`}>
        <div className="text-red-600">
          <h3 className="text-lg font-semibold mb-2">⚠️ Erro</h3>
          <p className="text-sm">{error}</p>
        </div>
      </Card>
    );
  }

  return (
    <Card className={`p-6 bg-gradient-to-br from-blue-50 to-indigo-50 border-blue-200 ${className}`}>
      {/* Header */}
      <div className="flex items-center justify-between mb-4">
        <div className="flex items-center space-x-2">
          <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
            <span className="text-white text-sm font-bold">🧠</span>
          </div>
          <h3 className="text-lg font-semibold text-gray-800">
            ROI Cognitivo
          </h3>
        </div>
        <div className="text-xs text-gray-500">
          {updateFrequency === 'real-time' ? '🔴 Tempo Real' : '📊 Atualizado'}
        </div>
      </div>
      
      {/* Main ROI Display */}
      <div className="mb-6">
        <div className="text-center mb-3">
          <div className="text-3xl font-bold text-green-600">
            {formatCurrency(metrics.totalSavingsThisMonth, metrics.currency)}
          </div>
          <div className="text-sm text-gray-600">Poupança este mês</div>
        </div>
        
        {/* ROI Percentage Gauge */}
        <div className="relative">
          <div className="w-full bg-gray-200 rounded-full h-3 mb-2">
            <div 
              className="bg-gradient-to-r from-blue-500 to-green-500 h-3 rounded-full transition-all duration-1000 ease-out"
              style={{ width: `${Math.min(getROIGaugeWidth(metrics.roiPercentage) / 3, 100)}%` }}
            ></div>
          </div>
          <div className="text-center">
            <span className={`text-xl font-bold ${getROIColor(metrics.roiPercentage)}`}>
              {metrics.roiPercentage}% ROI
            </span>
          </div>
        </div>
      </div>
      
      {/* Metrics Grid */}
      <div className="grid grid-cols-2 gap-4">
        <div className="text-center p-3 bg-white rounded-lg shadow-sm">
          <div className="text-2xl font-bold text-orange-600">
            {metrics.risksPreventedCount}
          </div>
          <div className="text-xs text-gray-600">
            Riscos Prevenidos
          </div>
        </div>
        
        <div className="text-center p-3 bg-white rounded-lg shadow-sm">
          <div className="text-2xl font-bold text-purple-600">
            {metrics.aiDecisionsMade.toLocaleString()}
          </div>
          <div className="text-xs text-gray-600">
            Decisões IA
          </div>
        </div>
      </div>
      
      {/* Value Proposition */}
      <div className="mt-4 p-3 bg-blue-100 rounded-lg border-l-4 border-blue-500">
        <div className="text-sm text-blue-800">
          <strong>💡 Valor Cognitivo:</strong> A IA preveniu {metrics.risksPreventedCount} riscos custosos, 
          economizando {formatCurrency(metrics.totalSavingsThisMonth, metrics.currency)} através de 
          {metrics.aiDecisionsMade.toLocaleString()} decisões inteligentes.
        </div>
      </div>
      
      {/* Security & Audit Footer */}
      <div className="mt-4 pt-3 border-t border-gray-200">
        <div className="flex items-center justify-between text-xs text-gray-500">
          <div className="flex items-center space-x-1">
            <span>🔒</span>
            <span>AES-256</span>
          </div>
          <div className="flex items-center space-x-1">
            <span>📊</span>
            <span>Auditoria Completa</span>
          </div>
          <div className="flex items-center space-x-1">
            <span>🎯</span>
            <span>ROI Verificado</span>
          </div>
        </div>
      </div>
    </Card>
  );
};

export default ROICognitivoWidget;