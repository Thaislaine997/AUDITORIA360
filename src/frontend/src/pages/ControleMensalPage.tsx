// src/frontend/src/pages/ControleMensalPage.tsx

import React, { useState, useEffect } from 'react';
import { getControlesDoMes, ControleMensalDetalhado } from '../services/controleMensalService';
// Vamos criar este componente a seguir
import { ControleMensalTable } from '../components/ControleMensalTable';
import { TemplateManager } from '../components/TemplateManager';

export const ControleMensalPage: React.FC = () => {
  const [controles, setControles] = useState<ControleMensalDetalhado[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Lógica para selecionar o mês/ano
  const [date, setDate] = useState({ month: new Date().getMonth() + 1, year: new Date().getFullYear() });

  const fetchControles = async () => {
    try {
      setLoading(true);
      const data = await getControlesDoMes(date.year, date.month);
      setControles(data);
      setError(null);
    } catch (err) {
      setError('Falha ao carregar os dados de controle.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchControles();
  }, [date]);

  const handleTemplateApplied = () => {
    // Recarregar os dados após aplicar template
    fetchControles();
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-3xl font-bold text-gray-900 mb-6">Controle de Folha Mensal</h1>

      {/* Month and Year Selectors */}
      <div className="mb-6 flex gap-4 items-center">
        <div>
          <label htmlFor="month-select" className="block text-sm font-medium text-gray-700 mb-1">
            Mês
          </label>
          <select
            id="month-select"
            value={date.month}
            onChange={(e) => setDate(prev => ({ ...prev, month: parseInt(e.target.value) }))}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            {Array.from({ length: 12 }, (_, i) => (
              <option key={i + 1} value={i + 1}>
                {new Date(2024, i, 1).toLocaleDateString('pt-BR', { month: 'long' })}
              </option>
            ))}
          </select>
        </div>
        
        <div>
          <label htmlFor="year-select" className="block text-sm font-medium text-gray-700 mb-1">
            Ano
          </label>
          <select
            id="year-select"
            value={date.year}
            onChange={(e) => setDate(prev => ({ ...prev, year: parseInt(e.target.value) }))}
            className="block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:outline-none focus:ring-blue-500 focus:border-blue-500 sm:text-sm"
          >
            {Array.from({ length: 5 }, (_, i) => (
              <option key={2020 + i} value={2020 + i}>
                {2020 + i}
              </option>
            ))}
          </select>
        </div>
        
        <div className="text-sm text-gray-600 mt-6">
          Mostrando dados para <strong>{new Date(date.year, date.month - 1, 1).toLocaleDateString('pt-BR', { month: 'long', year: 'numeric' })}</strong>
        </div>
      </div>

      {/* Template Management Section */}
      <TemplateManager onTemplateApplied={handleTemplateApplied} />

      {loading && (
        <div className="flex justify-center items-center py-8">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
          <span className="ml-2 text-gray-600">A carregar...</span>
        </div>
      )}
      
      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-md mb-4">
          {error}
        </div>
      )}
      
      {!loading && !error && (
        <div>
          {controles.length > 0 ? (
            <ControleMensalTable data={controles} />
          ) : (
            <div className="text-center py-8 text-gray-500">
              Nenhum controle encontrado para o período selecionado.
            </div>
          )}
        </div>
      )}
    </div>
  );
};