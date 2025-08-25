import { NextPage } from "next";
import Head from "next/head";
import { useRouter } from "next/router";
import { useEffect, useState } from "react";
import { motion } from "framer-motion";
import { authHelpers } from "../lib/supabaseClient";
import Link from "next/link";

interface User {
  id: string;
  email?: string;
  user_metadata?: {
    full_name?: string;
  };
}

const DashboardPage: NextPage = () => {
  const router = useRouter();
  const [user, setUser] = useState<User | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    checkUser();
  }, []);

  const checkUser = async () => {
    try {
      const currentUser = await authHelpers.getCurrentUser();
      if (!currentUser) {
        router.push("/login");
        return;
      }
      setUser(currentUser);
    } catch (error) {
      console.error("Error checking user:", error);
      router.push("/login");
    } finally {
      setLoading(false);
    }
  };

  const handleSignOut = async () => {
    try {
      await authHelpers.signOut();
      router.push("/");
    } catch (error) {
      console.error("Error signing out:", error);
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50 flex items-center justify-center">
        <div className="text-center">
          <motion.div 
            className="w-16 h-16 border-4 border-blue-200 border-t-blue-600 rounded-full mx-auto mb-4"
            animate={{ rotate: 360 }}
            transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
          />
          <p className="text-gray-600 font-medium">Carregando Portal AUDITORIA360...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return null; // Will redirect to login
  }

  return (
    <>
      <Head>
        <title>Dashboard - Portal AUDITORIA360</title>
        <meta name="description" content="Dashboard do Portal AUDITORIA360 - Gestão completa da folha de pagamento e auditoria inteligente." />
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
                <div className="text-2xl font-bold bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
                  AUDITORIA360
                </div>
                <div className="h-6 w-px bg-gray-300"></div>
                <div className="text-sm text-gray-600">Dashboard</div>
              </motion.div>
              
              <motion.div 
                className="flex items-center space-x-4"
                initial={{ opacity: 0, x: 20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ duration: 0.6 }}
              >
                <div className="text-sm text-gray-600">
                  Bem-vindo, <span className="font-medium">{user.user_metadata?.full_name || user.email}</span>
                </div>
                <button
                  onClick={handleSignOut}
                  className="bg-gradient-to-r from-red-500 to-red-600 hover:from-red-600 hover:to-red-700 text-white px-4 py-2 rounded-lg transition-all duration-300 font-medium transform hover:scale-105"
                >
                  Sair
                </button>
              </motion.div>
            </div>
          </div>
        </header>

        {/* Main Content */}
        <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
          {/* Welcome Section */}
          <motion.div 
            className="mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.2 }}
          >
            <h2 className="text-3xl font-bold text-gray-900 mb-2">
              Bem-vindo ao Portal AUDITORIA360
            </h2>
            <p className="text-gray-600">
              Sua central de controle para gestão da folha de pagamento e auditoria inteligente.
            </p>
          </motion.div>

          {/* Stats Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            {[
              { title: "Folhas Processadas", value: "127", subtitle: "Este mês", color: "blue", icon: "📊" },
              { title: "Auditorias Ativas", value: "34", subtitle: "Em andamento", color: "green", icon: "✅" },
              { title: "Demandas Abertas", value: "12", subtitle: "Aguardando análise", color: "yellow", icon: "🎫" },
              { title: "Compliance", value: "98.5%", subtitle: "Taxa de conformidade", color: "purple", icon: "🔒" }
            ].map((stat, index) => (
              <motion.div
                key={stat.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.3 + index * 0.1 }}
              >
                <StatsCard {...stat} />
              </motion.div>
            ))}
          </div>

          {/* Dashboard Modules */}
          <motion.div 
            className="grid grid-cols-1 lg:grid-cols-2 xl:grid-cols-3 gap-6 mb-8"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 0.7 }}
          >
            {[
              { title: "Controle da Folha Mensal", description: "Resumo, status, valores e gráficos da folha de pagamento", icon: "📊", href: "/folha" },
              { title: "Portal de Demandas", description: "Gestão de tickets: abertos, em andamento, finalizados", icon: "🎫", href: "/demandas" },
              { title: "Portal de Auditoria", description: "Upload de resumos e análise automática integrada", icon: "🔍", href: "/auditoria" },
              { title: "Tabelas Oficiais", description: "INSS, FGTS, IRRF, salário família e mínimo atualizados", icon: "📋", href: "/tabelas" },
              { title: "Portal CCT", description: "Convenções coletivas: importar, status e buscas online", icon: "📄", href: "/cct" },
              { title: "Gestão e Relatórios", description: "Relatórios integrados com todas as funcionalidades", icon: "📈", href: "/relatorios" }
            ].map((module, index) => (
              <motion.div
                key={module.title}
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: 0.8 + index * 0.1 }}
              >
                <DashboardModule {...module} />
              </motion.div>
            ))}
          </motion.div>

          {/* Recent Activity */}
          <motion.div 
            className="bg-white rounded-2xl shadow-sm border border-gray-200 p-6"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.2 }}
          >
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Atividade Recente</h3>
            <div className="space-y-4">
              <ActivityItem
                title="Folha processada com sucesso"
                description="Empresa XYZ Ltda - Novembro/2024"
                time="2 horas atrás"
                status="success"
              />
              <ActivityItem
                title="Nova demanda recebida"
                description="Solicitação de recálculo de férias - Ticket #1234"
                time="4 horas atrás"
                status="info"
              />
              <ActivityItem
                title="Auditoria finalizada"
                description="Análise de conformidade - Empresa ABC S.A."
                time="1 dia atrás"
                status="success"
              />
            </div>
          </motion.div>

          {/* Quick Actions */}
          <motion.div 
            className="mt-8 bg-gradient-to-r from-blue-600 to-purple-600 rounded-2xl p-6 text-white"
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.6, delay: 1.4 }}
          >
            <h3 className="text-lg font-semibold mb-4">Ações Rápidas</h3>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <Link href="/folha/controle-mensal">
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 hover:bg-white/20 transition-all cursor-pointer">
                  <div className="text-2xl mb-2">🚀</div>
                  <div className="font-medium">Processar Folha</div>
                  <div className="text-blue-100 text-sm">Iniciar processamento mensal</div>
                </div>
              </Link>
              <Link href="/ia/validacao">
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 hover:bg-white/20 transition-all cursor-pointer">
                  <div className="text-2xl mb-2">🤖</div>
                  <div className="font-medium">Validação IA</div>
                  <div className="text-blue-100 text-sm">Análise inteligente automática</div>
                </div>
              </Link>
              <Link href="/relatorios/templates">
                <div className="bg-white/10 backdrop-blur-sm rounded-xl p-4 hover:bg-white/20 transition-all cursor-pointer">
                  <div className="text-2xl mb-2">📋</div>
                  <div className="font-medium">Gerar Relatório</div>
                  <div className="text-blue-100 text-sm">Relatórios personalizados</div>
                </div>
              </Link>
            </div>
          </motion.div>
        </main>
      </div>
    </>
  );
};

// Enhanced StatsCard with animations and modern design
function StatsCard({
  title,
  value,
  subtitle,
  color,
  icon,
}: {
  title: string;
  value: string;
  subtitle: string;
  color: "blue" | "green" | "yellow" | "purple";
  icon: string;
}) {
  const colorClasses = {
    blue: "border-blue-200 hover:shadow-blue-100",
    green: "border-green-200 hover:shadow-green-100",
    yellow: "border-yellow-200 hover:shadow-yellow-100",
    purple: "border-purple-200 hover:shadow-purple-100",
  };

  return (
    <div className={`bg-white p-6 rounded-2xl border-l-4 ${colorClasses[color]} shadow-sm hover:shadow-lg transition-all duration-300 hover:-translate-y-1`}>
      <div className="flex items-center justify-between mb-4">
        <h3 className="text-sm font-medium text-gray-600">{title}</h3>
        <span className="text-2xl">{icon}</span>
      </div>
      <p className="text-3xl font-bold text-gray-900 mb-1">{value}</p>
      <p className="text-sm text-gray-500">{subtitle}</p>
    </div>
  );
}

// Enhanced DashboardModule with hover effects
function DashboardModule({
  title,
  description,
  icon,
  href,
}: {
  title: string;
  description: string;
  icon: string;
  href: string;
}) {
  return (
    <Link href={href}>
      <div className="bg-white p-6 rounded-2xl shadow-sm border border-gray-200 hover:shadow-lg transition-all duration-300 cursor-pointer hover:-translate-y-1 group">
        <div className="flex items-start">
          <div className="text-3xl mr-4 group-hover:scale-110 transition-transform duration-300">{icon}</div>
          <div className="flex-1">
            <h3 className="text-lg font-semibold text-gray-900 mb-2 group-hover:text-blue-600 transition-colors">{title}</h3>
            <p className="text-gray-600 text-sm">{description}</p>
          </div>
          <div className="text-gray-400 group-hover:text-blue-500 transition-colors">
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M9 5l7 7-7 7"/>
            </svg>
          </div>
        </div>
      </div>
    </Link>
  );
}

// Enhanced ActivityItem with status indicators
function ActivityItem({
  title,
  description,
  time,
  status,
}: {
  title: string;
  description: string;
  time: string;
  status: "success" | "info" | "warning";
}) {
  const statusConfig = {
    success: { color: "bg-green-500", icon: "✓" },
    info: { color: "bg-blue-500", icon: "ℹ" },
    warning: { color: "bg-yellow-500", icon: "⚠" },
  };

  const config = statusConfig[status];

  return (
    <div className="flex items-start space-x-3 py-3 hover:bg-gray-50 rounded-lg px-2 transition-colors">
      <div className={`w-8 h-8 ${config.color} rounded-full flex items-center justify-center text-white text-sm font-bold`}>
        {config.icon}
      </div>
      <div className="flex-1">
        <p className="text-sm font-medium text-gray-900">{title}</p>
        <p className="text-sm text-gray-600">{description}</p>
        <p className="text-xs text-gray-400 mt-1">{time}</p>
      </div>
    </div>
  );
}

export default DashboardPage;