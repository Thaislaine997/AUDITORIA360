import React, { useState } from "react";
import Head from "next/head";
import Link from "next/link";
import { motion } from "framer-motion";

interface Integracao {
  id: number;
  nome: string;
  descricao: string;
  tipo: string;
  status: 'ATIVA' | 'INATIVA' | 'ERRO';
  ativa: boolean;
  ultima_sincronizacao?: string;
  icon: string;
}

const IntegracoesPage: React.FC = () => {
  const [integracoes, setIntegracoes] = useState<Integracao[]>([
    {
      id: 1,
      nome: "Supabase",
      descricao: "Banco de dados e autenticação em tempo real",
      tipo: "DATABASE",
      status: "ATIVA",
      ativa: true,
      ultima_sincronizacao: "2024-01-18T10:30:00",
      icon: "🗄️"
    },
    {
      id: 2,
      nome: "Google Gemini",
      descricao: "API de Inteligência Artificial para análise",
      tipo: "AI",
      status: "ATIVA",
      ativa: true,
      ultima_sincronizacao: "2024-01-18T09:45:00",
      icon: "🤖"
    },
    {
      id: 3,
      nome: "Stripe",
      descricao: "Processamento de pagamentos seguro",
      tipo: "PAYMENT",
      status: "INATIVA",
      ativa: false,
      icon: "💳"
    },
    {
      id: 4,
      nome: "SendGrid",
      descricao: "Serviço de envio de emails transacionais",
      tipo: "EMAIL",
      status: "ATIVA",
      ativa: true,
      ultima_sincronizacao: "2024-01-18T11:15:00",
      icon: "📧"
    },
    {
      id: 5,
      nome: "WhatsApp Business API",
      descricao: "Comunicação direta com clientes via WhatsApp",
      tipo: "MESSAGING",
      status: "ERRO",
      ativa: false,
      icon: "📱"
    },
    {
      id: 6,
      nome: "Google Drive",
      descricao: "Armazenamento e backup de documentos",
      tipo: "STORAGE",
      status: "ATIVA",
      ativa: true,
      ultima_sincronizacao: "2024-01-18T12:00:00",
      icon: "☁️"
    }
  ]);

  const toggleIntegracao = (id: number) => {
    setIntegracoes(prev => 
      prev.map(integracao => 
        integracao.id === id 
          ? { ...integracao, ativa: !integracao.ativa, status: !integracao.ativa ? 'ATIVA' : 'INATIVA' }
          : integracao
      )
    );
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ATIVA': return 'bg-green-100 text-green-800 border-green-200';
      case 'INATIVA': return 'bg-gray-100 text-gray-800 border-gray-200';
      case 'ERRO': return 'bg-red-100 text-red-800 border-red-200';
      default: return 'bg-gray-100 text-gray-800 border-gray-200';
    }
  };

  const getTipoColor = (tipo: string) => {
    switch (tipo) {
      case 'DATABASE': return 'bg-blue-100 text-blue-800';
      case 'AI': return 'bg-purple-100 text-purple-800';
      case 'PAYMENT': return 'bg-green-100 text-green-800';
      case 'EMAIL': return 'bg-orange-100 text-orange-800';
      case 'MESSAGING': return 'bg-pink-100 text-pink-800';
      case 'STORAGE': return 'bg-cyan-100 text-cyan-800';
      default: return 'bg-gray-100 text-gray-800';
    }
  };

  const formatUltimaSincronizacao = (data?: string) => {
    if (!data) return 'Nunca sincronizado';
    const date = new Date(data);
    return date.toLocaleString('pt-BR');
  };

  return (
    <>
      <Head>
        <title>Integrações - Portal AUDITORIA360</title>
        <meta name="description" content="Gerencie todas as integrações do Portal AUDITORIA360" />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
        <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&display=swap" rel="stylesheet" />
      </Head>

      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 font-sans">
        {/* Header */}
        <header className="bg-white shadow-sm border-b border-gray-200">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between items-center py-4">
              <motion.div 
                className="flex items-center space-x-4"
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
              >
                <Link href="/dashboard">
                  <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent cursor-pointer">
                    AUDITORIA360
                  </div>
                </Link>
                <div className="h-6 w-px bg-gray-300"></div>
                <div className="text-sm text-gray-600">Integrações</div>
              </motion.div>
              
              <motion.div
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
              >
                <Link href="/dashboard">
                  <button className="bg-gray-100 hover:bg-gray-200 text-gray-700 px-4 py-2 rounded-lg transition-colors font-medium">
                    ← Voltar ao Dashboard
                  </button>
                </Link>
              </motion.div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Page Header */}
          <motion.div 
            className="mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h1 className="text-3xl font-bold text-gray-900 mb-2">Integrações</h1>
            <p className="text-gray-600">
              Gerencie todas as integrações e conexões do Portal AUDITORIA360
            </p>
          </motion.div>

          {/* Stats Overview */}
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.3 }}
          >
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-gray-600">Total de Integrações</h3>
                <span className="text-2xl">🔗</span>
              </div>
              <p className="text-3xl font-bold text-gray-900">{integracoes.length}</p>
            </div>
            
            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-gray-600">Ativas</h3>
                <span className="text-2xl">✅</span>
              </div>
              <p className="text-3xl font-bold text-green-600">{integracoes.filter(i => i.status === 'ATIVA').length}</p>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-gray-600">Inativas</h3>
                <span className="text-2xl">⏸️</span>
              </div>
              <p className="text-3xl font-bold text-gray-600">{integracoes.filter(i => i.status === 'INATIVA').length}</p>
            </div>

            <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-sm font-medium text-gray-600">Com Erro</h3>
                <span className="text-2xl">⚠️</span>
              </div>
              <p className="text-3xl font-bold text-red-600">{integracoes.filter(i => i.status === 'ERRO').length}</p>
            </div>
          </motion.div>

          {/* Integrations Grid */}
          <div className="grid grid-cols-1 md:grid-cols-2 xl:grid-cols-3 gap-6">
            {integracoes.map((integracao, index) => (
              <motion.div
                key={integracao.id}
                className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6 hover:shadow-md transition-all duration-300"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.4 + index * 0.1 }}
                whileHover={{ y: -2 }}
              >
                {/* Header */}
                <div className="flex items-start justify-between mb-4">
                  <div className="flex items-center space-x-3">
                    <div className="text-3xl">{integracao.icon}</div>
                    <div>
                      <h3 className="text-lg font-semibold text-gray-900">{integracao.nome}</h3>
                      <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium ${getTipoColor(integracao.tipo)}`}>
                        {integracao.tipo}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center space-x-2">
                    <span className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${getStatusColor(integracao.status)}`}>
                      {integracao.status}
                    </span>
                  </div>
                </div>

                {/* Description */}
                <p className="text-gray-600 text-sm mb-4">{integracao.descricao}</p>

                {/* Last Sync */}
                {integracao.ultima_sincronizacao && (
                  <div className="mb-4 p-3 bg-gray-50 rounded-lg">
                    <div className="text-xs text-gray-500 mb-1">Última sincronização</div>
                    <div className="text-sm text-gray-700">{formatUltimaSincronizacao(integracao.ultima_sincronizacao)}</div>
                  </div>
                )}

                {/* Actions */}
                <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                  <label className="flex items-center cursor-pointer">
                    <input
                      type="checkbox"
                      checked={integracao.ativa}
                      onChange={() => toggleIntegracao(integracao.id)}
                      className="sr-only"
                    />
                    <div className={`relative inline-flex h-6 w-11 items-center rounded-full transition-colors ${
                      integracao.ativa ? 'bg-blue-600' : 'bg-gray-200'
                    }`}>
                      <span className={`inline-block h-4 w-4 transform rounded-full bg-white transition-transform ${
                        integracao.ativa ? 'translate-x-6' : 'translate-x-1'
                      }`} />
                    </div>
                    <span className="ml-2 text-sm text-gray-700">
                      {integracao.ativa ? 'Ativa' : 'Inativa'}
                    </span>
                  </label>

                  <div className="flex space-x-2">
                    {integracao.ativa && (
                      <button className="p-2 text-gray-400 hover:text-blue-600 transition-colors rounded-lg hover:bg-blue-50">
                        <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
                        </svg>
                      </button>
                    )}
                    <button className="p-2 text-gray-400 hover:text-gray-600 transition-colors rounded-lg hover:bg-gray-50">
                      <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M10.325 4.317c.426-1.756 2.924-1.756 3.35 0a1.724 1.724 0 002.573 1.066c1.543-.94 3.31.826 2.37 2.37a1.724 1.724 0 001.065 2.572c1.756.426 1.756 2.924 0 3.35a1.724 1.724 0 00-1.066 2.573c.94 1.543-.826 3.31-2.37 2.37a1.724 1.724 0 00-2.572 1.065c-.426 1.756-2.924 1.756-3.35 0a1.724 1.724 0 00-2.573-1.066c-1.543.94-3.31-.826-2.37-2.37a1.724 1.724 0 00-1.065-2.572c-1.756-.426-1.756-2.924 0-3.35a1.724 1.724 0 001.066-2.573c-.94-1.543.826-3.31 2.37-2.37.996.608 2.296.07 2.572-1.065z"/>
                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"/>
                      </svg>
                    </button>
                  </div>
                </div>
              </motion.div>
            ))}
          </div>

          {/* Add New Integration */}
          <motion.div 
            className="mt-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1 }}
          >
            <div className="flex items-center justify-between">
              <div>
                <h3 className="text-lg font-semibold mb-2">Adicionar Nova Integração</h3>
                <p className="text-blue-100">Conecte novos serviços ao Portal AUDITORIA360</p>
              </div>
              <button className="bg-white/20 backdrop-blur-sm rounded-xl p-4 hover:bg-white/30 transition-all">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 4v16m8-8H4"/>
                </svg>
              </button>
            </div>
          </motion.div>
        </main>
      </div>
    </>
  );
};

export default IntegracoesPage;