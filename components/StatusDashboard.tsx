import React, { useEffect, useState } from "react";
import { 
  CheckCircle, 
  XCircle, 
  AlertCircle, 
  Clock, 
  RefreshCw,
  Activity,
  TrendingUp,
  Server,
  Zap,
  Smartphone,
  Monitor,
  Globe,
  BarChart3
} from "lucide-react";
import AutomationDashboard from './AutomationDashboard';

// Status types and interfaces
interface ModuleStatus {
  name: string;
  status: string;
  response_time?: number;
  details?: string;
  last_check: string;
  critical?: boolean;
}

interface SystemHealth {
  system_status: string;
  total_modules: number;
  healthy_modules: number;
  health_percentage: number;
  modules: ModuleStatus[];
  timestamp: string;
  total_response_time: number;
}

// Module configuration for frontend display
const MODULES = [
  { name: "Dashboard Estratégico", url: "/api/health/dashboard", category: "admin" },
  { name: "Controle Mensal", url: "/api/health/controle_mensal", category: "client" },
  { name: "Disparo de Auditoria", url: "/api/health/disparo_auditoria", category: "client" },
  { name: "Análise Forense", url: "/api/health/forense", category: "client" },
  { name: "Gestão de Regras", url: "/api/health/regras", category: "client" },
  { name: "Simulador de Impactos", url: "/api/health/simulador", category: "client" },
  { name: "Geração de Relatórios", url: "/api/health/relatorios", category: "client" },
  { name: "Integração com IA", url: "/api/health/ia", category: "core" },
  { name: "Login/Admin", url: "/api/health/login_admin", category: "admin" },
  { name: "LOGOPERACOES", url: "/api/health/logoperacoes", category: "admin" },
  { name: "Personificação", url: "/api/health/personificacao", category: "admin" },
  { name: "Login/Onboarding", url: "/api/health/login_onboarding", category: "client" },
  { name: "Logs e Auditoria", url: "/api/health/logs_auditoria", category: "core" },
  { name: "Onboarding Escritório", url: "/api/health/onboarding_escritorio", category: "client" },
  { name: "Gerenciamento de Usuários", url: "/api/health/gerenciamento_usuarios", category: "core" },
];

// Status styling and icons
const getStatusConfig = (status: string) => {
  switch (status) {
    case "ok":
    case "funcionando":
      return {
        color: "text-green-600",
        bgColor: "bg-green-100",
        icon: CheckCircle,
        label: "FUNCIONANDO",
        badgeColor: "bg-green-500"
      };
    case "em_desenvolvimento":
      return {
        color: "text-yellow-600", 
        bgColor: "bg-yellow-100",
        icon: Clock,
        label: "EM DESENVOLVIMENTO",
        badgeColor: "bg-yellow-500"
      };
    case "em_teste":
      return {
        color: "text-blue-600",
        bgColor: "bg-blue-100", 
        icon: Activity,
        label: "EM TESTE",
        badgeColor: "bg-blue-500"
      };
    case "error":
    case "erro":
      return {
        color: "text-red-600",
        bgColor: "bg-red-100",
        icon: XCircle,
        label: "ERRO",
        badgeColor: "bg-red-500"
      };
    case "degraded":
      return {
        color: "text-orange-600",
        bgColor: "bg-orange-100",
        icon: AlertCircle,
        label: "DEGRADADO",
        badgeColor: "bg-orange-500"
      };
    default:
      return {
        color: "text-gray-600",
        bgColor: "bg-gray-100",
        icon: AlertCircle,
        label: "DESCONHECIDO",
        badgeColor: "bg-gray-500"
      };
  }
};

const StatusDashboard: React.FC = () => {
  const [systemHealth, setSystemHealth] = useState<SystemHealth | null>(null);
  const [loading, setLoading] = useState(true);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [autoRefresh, setAutoRefresh] = useState(true);
  const [isMobile, setIsMobile] = useState(false);
  const [viewMode, setViewMode] = useState<'overview' | 'detailed' | 'categories'>('overview');

  // Detect mobile viewport
  useEffect(() => {
    const checkMobile = () => {
      setIsMobile(window.innerWidth < 768);
    };
    
    checkMobile();
    window.addEventListener('resize', checkMobile);
    return () => window.removeEventListener('resize', checkMobile);
  }, []);

  // Fetch system health data
  const fetchSystemHealth = async () => {
    try {
      setLoading(true);
      const response = await fetch('/api/health/status');
      const data: SystemHealth = await response.json();
      
      setSystemHealth(data);
      setLastUpdate(new Date());
    } catch (error) {
      console.error('Error fetching system health:', error);
    } finally {
      setLoading(false);
    }
  };

  // Auto-refresh effect
  useEffect(() => {
    fetchSystemHealth();
    
    let interval: NodeJS.Timeout;
    if (autoRefresh) {
      interval = setInterval(fetchSystemHealth, 30000); // Refresh every 30 seconds
    }
    
    return () => {
      if (interval) clearInterval(interval);
    };
  }, [autoRefresh]);

  const handleRefresh = () => {
    fetchSystemHealth();
  };

  const formatResponseTime = (time?: number) => {
    if (!time) return "N/A";
    return time < 1 ? `${(time * 1000).toFixed(0)}ms` : `${time.toFixed(2)}s`;
  };

  const getSystemHealthColor = (status: string) => {
    switch (status) {
      case "healthy": return "text-green-600";
      case "degraded": return "text-yellow-600";
      case "critical": return "text-red-600";
      default: return "text-gray-600";
    }
  };

  const getSystemHealthIcon = (status: string) => {
    switch (status) {
      case "healthy": return CheckCircle;
      case "degraded": return AlertCircle;
      case "critical": return XCircle;
      default: return Server;
    }
  };

  // Group modules by category
  const modulesByCategory = systemHealth?.modules.reduce((acc, module) => {
    const moduleConfig = MODULES.find(m => m.name === module.name);
    const category = moduleConfig?.category || 'other';
    
    if (!acc[category]) acc[category] = [];
    acc[category].push(module);
    return acc;
  }, {} as Record<string, ModuleStatus[]>) || {};


  const categoryLabels: Record<string, string> = {
    admin: 'Administração',
    client: 'Cliente',
    core: 'Sistema Central',
    other: 'Outros'
  };

  if (loading && !systemHealth) {
    return (
      <div className="min-h-screen bg-gray-50 p-4">
        <div className="max-w-7xl mx-auto">
          <div className="animate-pulse">
            <div className="h-8 bg-gray-300 rounded mb-6"></div>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
              {[1, 2, 3].map((i) => (
                <div key={i} className="h-32 bg-gray-300 rounded-lg"></div>
              ))}
            </div>
            <div className="h-96 bg-gray-300 rounded-lg"></div>
          </div>
        </div>
      </div>
    );
  }

  const SystemHealthIcon = systemHealth ? getSystemHealthIcon(systemHealth.system_status) : Server;

  return (
    <>
      <AutomationDashboard />
      <div className="min-h-screen bg-gray-50 p-4 md:p-6">
        <div className="max-w-7xl mx-auto">
          {/* Header */}
          <div className="mb-6 md:mb-8">
            <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-4 space-y-4 md:space-y-0">
              <div>
                <h1 className="text-2xl md:text-3xl font-bold text-gray-900">Status Operacional - AUDITORIA360</h1>
                <p className="text-gray-600 mt-1">
                  Monitoramento em tempo real dos módulos do sistema
                </p>
              </div>
              
              <div className="flex flex-col sm:flex-row items-start sm:items-center space-y-2 sm:space-y-0 sm:space-x-4 w-full md:w-auto">
                {/* View Mode Toggle */}
                {!isMobile && (
                  <div className="flex bg-gray-200 rounded-lg p-1">
                    <button
                      onClick={() => setViewMode('overview')}
                      className={`px-3 py-1 rounded text-sm font-medium ${
                        viewMode === 'overview' ? 'bg-white shadow' : 'text-gray-600'
                      }`}
                    >
                      <BarChart3 className="h-4 w-4 inline mr-1" />
                      Geral
                    </button>
                    <button
                      onClick={() => setViewMode('categories')}
                      className={`px-3 py-1 rounded text-sm font-medium ${
                        viewMode === 'categories' ? 'bg-white shadow' : 'text-gray-600'
                      }`}
                    >
                      <Globe className="h-4 w-4 inline mr-1" />
                      Por Categoria
                    </button>
                    <button
                      onClick={() => setViewMode('detailed')}
                      className={`px-3 py-1 rounded text-sm font-medium ${
                        viewMode === 'detailed' ? 'bg-white shadow' : 'text-gray-600'
                      }`}
                    >
                      <Monitor className="h-4 w-4 inline mr-1" />
                      Detalhado
                    </button>
                  </div>
                )}
                
                <div className="flex items-center space-x-2">
                  <span className="text-sm text-gray-500">Auto-refresh:</span>
                  <button
                    onClick={() => setAutoRefresh(!autoRefresh)}
                    className={`px-3 py-1 rounded text-sm font-medium ${
                      autoRefresh 
                        ? 'bg-green-100 text-green-700 border border-green-300'
                        : 'bg-gray-100 text-gray-700 border border-gray-300'
                    }`}
                  >
                    {autoRefresh ? "Ativo" : "Inativo"}
                  </button>
                </div>
                
                <button
                  onClick={handleRefresh}
                  disabled={loading}
                  className="flex items-center space-x-2 px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 w-full sm:w-auto justify-center"
                >
                  <RefreshCw className={`h-4 w-4 ${loading ? 'animate-spin' : ''}`} />
                  <span>Atualizar</span>
                </button>
              </div>
            </div>
            
            <div className="text-sm text-gray-500">
              Última atualização: {lastUpdate.toLocaleTimeString('pt-BR')}
            </div>
          </div>

          {/* System Overview Cards */}
          {systemHealth && (
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 md:gap-6 mb-6 md:mb-8">
              <div className="bg-white p-4 md:p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm md:text-lg font-semibold text-gray-900">Status Geral</h3>
                    <div className={`flex items-center space-x-2 mt-2 ${getSystemHealthColor(systemHealth.system_status)}`}>
                      <SystemHealthIcon className="h-4 w-4 md:h-5 md:w-5" />
                      <span className="font-medium text-sm md:text-base">
                        {systemHealth.system_status === "healthy" ? "SAUDÁVEL" : 
                         systemHealth.system_status === "degraded" ? "DEGRADADO" : "CRÍTICO"}
                      </span>
                    </div>
                  </div>
                  <div className="p-3 bg-blue-100 rounded-full">
                    <Server className="h-6 w-6 md:h-8 md:w-8 text-blue-600" />
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 md:p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm md:text-lg font-semibold text-gray-900">Módulos OK</h3>
                    <div className="flex items-center space-x-2 mt-2">
                      <span className="text-xl md:text-2xl font-bold text-green-600">
                        {systemHealth.healthy_modules}/{systemHealth.total_modules}
                      </span>
                      <span className="text-xs md:text-sm text-gray-500">
                        ({systemHealth.health_percentage.toFixed(1)}%)
                      </span>
                    </div>
                  </div>
                  <div className="p-3 bg-green-100 rounded-full">
                    <TrendingUp className="h-6 w-6 md:h-8 md:w-8 text-green-600" />
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 md:p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm md:text-lg font-semibold text-gray-900">Tempo Resposta</h3>
                    <div className="flex items-center space-x-2 mt-2">
                      <span className="text-xl md:text-2xl font-bold text-blue-600">
                        {formatResponseTime(systemHealth.total_response_time)}
                      </span>
                      <span className="text-xs md:text-sm text-gray-500">médio</span>
                    </div>
                  </div>
                  <div className="p-3 bg-blue-100 rounded-full">
                    <Zap className="h-6 w-6 md:h-8 md:w-8 text-blue-600" />
                  </div>
                </div>
              </div>

              <div className="bg-white p-4 md:p-6 rounded-lg shadow-md">
                <div className="flex items-center justify-between">
                  <div>
                    <h3 className="text-sm md:text-lg font-semibold text-gray-900">Plataforma</h3>
                    <div className="flex items-center space-x-2 mt-2">
                      {isMobile ? (
                        <Smartphone className="h-4 w-4 md:h-5 md:w-5 text-purple-600" />
                      ) : (
                        <Monitor className="h-4 w-4 md:h-5 md:w-5 text-purple-600" />
                      )}
                      <span className="font-medium text-sm md:text-base text-purple-600">
                        {isMobile ? "Mobile" : "Desktop"}
                      </span>
                    </div>
                  </div>
                  <div className="p-3 bg-purple-100 rounded-full">
                    <Globe className="h-6 w-6 md:h-8 md:w-8 text-purple-600" />
                  </div>
                </div>
              </div>
            </div>
          )}

          {/* Modules Status - Different views based on mode and screen size */}
          <div className="bg-white rounded-lg shadow-md overflow-hidden">
            <div className="px-4 md:px-6 py-4 border-b border-gray-200">
              <h2 className="text-lg md:text-xl font-semibold text-gray-900">Status dos Módulos</h2>
            </div>
            
            {/* Mobile View or Categories View */}
            {(isMobile || viewMode === 'categories') && systemHealth && (
              <div className="p-4 md:p-6 space-y-4">
                {Object.entries(modulesByCategory).map(([category, modules]) => (
                  <div key={category} className="border rounded-lg">
                    <div className="bg-gray-50 px-4 py-2 border-b">
                      <h3 className="font-medium text-gray-900">{categoryLabels[category] || category}</h3>
                      <span className="text-sm text-gray-500">
                        {modules.filter(m => getStatusConfig(m.status).label === 'FUNCIONANDO').length}/{modules.length} funcionando
                      </span>
                    </div>
                    <div className="divide-y">
                      {modules.map((module, index) => {
                        const statusConfig = getStatusConfig(module.status);
                        const StatusIcon = statusConfig.icon;
                        
                        return (
                          <div key={index} className="p-4">
                            <div className="flex items-center justify-between mb-2">
                              <span className="font-medium text-gray-900 text-sm md:text-base">
                                {module.name}
                              </span>
                              <div className={`flex items-center space-x-2 ${statusConfig.color}`}>
                                <StatusIcon className="h-4 w-4" />
                                <span className="text-xs md:text-sm font-medium">{statusConfig.label}</span>
                              </div>
                            </div>
                            <div className="text-xs md:text-sm text-gray-500">
                              <div>{module.details || "-"}</div>
                              <div className="flex justify-between mt-1">
                                <span>Resposta: {formatResponseTime(module.response_time)}</span>
                                <span>Atualizado: {new Date(module.last_check).toLocaleTimeString('pt-BR')}</span>
                              </div>
                            </div>
                          </div>
                        );
                      })}
                    </div>
                  </div>
                ))}
              </div>
            )}

            {/* Desktop Table View */}
            {!isMobile && viewMode === 'detailed' && (
              <div className="overflow-x-auto">
                <table className="w-full">
                  <thead className="bg-gray-50">
                    <tr>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Módulo
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Status
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Tempo Resposta
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Detalhes
                      </th>
                      <th className="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                        Última Verificação
                      </th>
                    </tr>
                  </thead>
                  <tbody className="bg-white divide-y divide-gray-200">
                    {systemHealth?.modules.map((module, index) => {
                      const statusConfig = getStatusConfig(module.status);
                      const StatusIcon = statusConfig.icon;
                      
                      return (
                        <tr key={index} className="hover:bg-gray-50">
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className="flex items-center">
                              <span className="text-sm font-medium text-gray-900">
                                {module.name}
                              </span>
                              {module.critical && (
                                <span className="ml-2 px-2 py-1 text-xs bg-red-100 text-red-800 rounded-full">
                                  CRÍTICO
                                </span>
                              )}
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap">
                            <div className={`flex items-center space-x-2 ${statusConfig.color}`}>
                              <StatusIcon className="h-4 w-4" />
                              <span className="text-sm font-medium">{statusConfig.label}</span>
                            </div>
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                            {formatResponseTime(module.response_time)}
                          </td>
                          <td className="px-6 py-4 text-sm text-gray-900 max-w-xs truncate">
                            {module.details || "-"}
                          </td>
                          <td className="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                            {new Date(module.last_check).toLocaleTimeString('pt-BR')}
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}

            {/* Overview Grid View */}
            {!isMobile && viewMode === 'overview' && systemHealth && (
              <div className="p-6">
                <div className="grid grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-4">
                  {systemHealth.modules.map((module, index) => {
                    const statusConfig = getStatusConfig(module.status);
                    const StatusIcon = statusConfig.icon;
                    
                    return (
                      <div key={index} className={`border rounded-lg p-4 ${statusConfig.bgColor} border-l-4`} style={{borderLeftColor: statusConfig.color.replace('text-', '').replace('-600', '')}}>
                        <div className="flex items-center justify-between mb-2">
                          <StatusIcon className={`h-5 w-5 ${statusConfig.color}`} />
                          <span className="text-xs text-gray-600">{formatResponseTime(module.response_time)}</span>
                        </div>
                        <h3 className="font-medium text-gray-900 text-sm mb-1">{module.name}</h3>
                        <p className="text-xs text-gray-600 truncate">{module.details}</p>
                        <div className={`mt-2 inline-block px-2 py-1 rounded text-xs font-medium ${statusConfig.bgColor} ${statusConfig.color}`}>
                          {statusConfig.label}
                        </div>
                      </div>
                    );
                  })}
                </div>
              </div>
            )}
          </div>

          {/* System Information Footer */}
          <div className="mt-6 md:mt-8 bg-white rounded-lg shadow-md p-4 md:p-6">
            <h3 className="text-lg font-semibold text-gray-900 mb-4">Informações do Sistema</h3>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 text-sm">
              <div>
                <span className="font-medium text-gray-700">Versão:</span>
                <span className="ml-2 text-gray-600">1.0.0</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Ambiente:</span>
                <span className="ml-2 text-gray-600">Produção</span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Última Verificação:</span>
                <span className="ml-2 text-gray-600">
                  {systemHealth?.timestamp ? 
                    new Date(systemHealth.timestamp).toLocaleString('pt-BR') : 
                    'N/A'}
                </span>
              </div>
              <div>
                <span className="font-medium text-gray-700">Próxima Atualização:</span>
                <span className="ml-2 text-gray-600">
                  {autoRefresh ? "30 segundos" : "Manual"}
                </span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </>
  );
};

export default StatusDashboard;