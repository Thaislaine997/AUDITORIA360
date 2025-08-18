// src/frontend/src/components/TemplateManager.tsx

import React, { useState, useEffect } from 'react';
import api from '../services/api';

interface Template {
  id: number;
  nome_template: string;
  descricao?: string;
  criado_em: string;
  tarefas: string[];
}

interface TemplateManagerProps {
  onTemplateApplied?: () => void;
}

export const TemplateManager: React.FC<TemplateManagerProps> = ({ onTemplateApplied }) => {
  const [templates, setTemplates] = useState<Template[]>([]);
  const [loading, setLoading] = useState(true);
  const [showCreateForm, setShowCreateForm] = useState(false);
  const [newTemplate, setNewTemplate] = useState({
    nome_template: '',
    descricao: '',
    tarefas: ['']
  });

  useEffect(() => {
    fetchTemplates();
  }, []);

  const fetchTemplates = async () => {
    try {
      setLoading(true);
      const response = await api.get('/v1/templates');
      setTemplates(response.data);
    } catch (error) {
      console.error('Erro ao carregar templates:', error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTemplate = async (e: React.FormEvent) => {
    e.preventDefault();
    
    try {
      const validTarefas = newTemplate.tarefas.filter(t => t.trim().length > 0);
      
      if (validTarefas.length === 0) {
        alert('Adicione pelo menos uma tarefa');
        return;
      }

      await api.post('/v1/templates', {
        ...newTemplate,
        tarefas: validTarefas
      });

      await fetchTemplates();
      setShowCreateForm(false);
      setNewTemplate({ nome_template: '', descricao: '', tarefas: [''] });
    } catch (error: any) {
      console.error('Erro ao criar template:', error);
      const errorMsg = error.response?.data?.detail || 'Erro ao criar template';
      alert(`Erro ao criar template: ${errorMsg}`);
    }
  };

  const handleApplyTemplate = async (templateId: number) => {
    const currentDate = new Date();
    const mes = currentDate.getMonth() + 1;
    const ano = currentDate.getFullYear();

    try {
      const response = await api.post('/v1/controles/aplicar-template', {
        template_id: templateId,
        mes,
        ano,
        empresas_ids: null // Apply to all companies
      });

      alert(response.data.message);
      if (onTemplateApplied) {
        onTemplateApplied();
      }
    } catch (error: any) {
      console.error('Erro ao aplicar template:', error);
      const errorMsg = error.response?.data?.detail || 'Erro ao aplicar template';
      alert(`Erro ao aplicar template: ${errorMsg}`);
    }
  };

  const addTarefaField = () => {
    setNewTemplate(prev => ({
      ...prev,
      tarefas: [...prev.tarefas, '']
    }));
  };

  const updateTarefa = (index: number, value: string) => {
    setNewTemplate(prev => ({
      ...prev,
      tarefas: prev.tarefas.map((tarefa, i) => i === index ? value : tarefa)
    }));
  };

  const removeTarefa = (index: number) => {
    if (newTemplate.tarefas.length > 1) {
      setNewTemplate(prev => ({
        ...prev,
        tarefas: prev.tarefas.filter((_, i) => i !== index)
      }));
    }
  };

  if (loading) {
    return (
      <div className="flex justify-center items-center py-8">
        <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600"></div>
        <span className="ml-2 text-gray-600">A carregar templates...</span>
      </div>
    );
  }

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-900 flex items-center">
          📋 Gestão de Templates
        </h2>
        <button
          onClick={() => setShowCreateForm(true)}
          className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 flex items-center"
        >
          ➕ Novo Template
        </button>
      </div>

      {showCreateForm && (
        <div className="border border-gray-200 rounded-lg p-4 mb-4 bg-gray-50">
          <h3 className="font-medium text-gray-900 mb-3">Criar Novo Template</h3>
          <form onSubmit={handleCreateTemplate}>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Nome do Template *
                </label>
                <input
                  type="text"
                  required
                  value={newTemplate.nome_template}
                  onChange={(e) => setNewTemplate(prev => ({ ...prev, nome_template: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="ex: Simples Nacional - Padrão"
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Descrição
                </label>
                <input
                  type="text"
                  value={newTemplate.descricao}
                  onChange={(e) => setNewTemplate(prev => ({ ...prev, descricao: e.target.value }))}
                  className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                  placeholder="Descrição opcional"
                />
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Tarefas do Template *
              </label>
              {newTemplate.tarefas.map((tarefa, index) => (
                <div key={index} className="flex items-center mb-2">
                  <input
                    type="text"
                    value={tarefa}
                    onChange={(e) => updateTarefa(index, e.target.value)}
                    className="flex-1 px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-blue-500 focus:border-blue-500"
                    placeholder={`Tarefa ${index + 1}`}
                  />
                  {newTemplate.tarefas.length > 1 && (
                    <button
                      type="button"
                      onClick={() => removeTarefa(index)}
                      className="ml-2 text-red-600 hover:text-red-800"
                    >
                      ❌
                    </button>
                  )}
                </div>
              ))}
              <button
                type="button"
                onClick={addTarefaField}
                className="text-blue-600 hover:text-blue-800 text-sm"
              >
                + Adicionar Tarefa
              </button>
            </div>

            <div className="flex justify-end space-x-2">
              <button
                type="button"
                onClick={() => setShowCreateForm(false)}
                className="px-4 py-2 text-gray-600 border border-gray-300 rounded-md hover:bg-gray-50"
              >
                Cancelar
              </button>
              <button
                type="submit"
                className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
              >
                Criar Template
              </button>
            </div>
          </form>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {templates.map((template) => (
          <div key={template.id} className="border border-gray-200 rounded-lg p-4">
            <div className="flex justify-between items-start mb-2">
              <h3 className="font-medium text-gray-900 text-sm">{template.nome_template}</h3>
              <span className="text-xs text-gray-500">
                {template.tarefas.length} tarefas
              </span>
            </div>
            
            {template.descricao && (
              <p className="text-sm text-gray-600 mb-3">{template.descricao}</p>
            )}
            
            <div className="mb-3">
              <p className="text-xs text-gray-500 mb-1">Tarefas:</p>
              <ul className="text-xs text-gray-600 space-y-1">
                {template.tarefas.slice(0, 3).map((tarefa, index) => (
                  <li key={index} className="truncate">• {tarefa}</li>
                ))}
                {template.tarefas.length > 3 && (
                  <li className="text-gray-400">... e mais {template.tarefas.length - 3}</li>
                )}
              </ul>
            </div>
            
              <button
                onClick={() => handleApplyTemplate(template.id)}
                className="w-full bg-green-600 text-white px-3 py-2 rounded-md hover:bg-green-700 flex items-center justify-center text-sm"
              >
                ▶️ Aplicar Template
              </button>
          </div>
        ))}
      </div>

      {templates.length === 0 && (
        <div className="text-center py-8 text-gray-500">
          <div className="text-4xl mb-4">📋</div>
          <p>Nenhum template encontrado.</p>
          <p className="text-sm">Crie seu primeiro template para facilitar a criação de controles mensais.</p>
        </div>
      )}
    </div>
  );
};