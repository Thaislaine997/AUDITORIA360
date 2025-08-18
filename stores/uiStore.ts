import { create } from 'zustand';

type LayoutMode = 'comfortable' | 'compact';

// Fluxo Design System: Contextual Workspaces
type WorkspaceType = 
  | 'dashboard'      // Main overview workspace
  | 'payroll'        // Payroll management workspace  
  | 'audit'          // Auditing and compliance workspace
  | 'reports'        // Reports and analytics workspace
  | 'ai_consultant'  // AI consultant and risk analysis workspace
  | 'documents'      // Document management workspace
  | 'admin'          // Administration workspace
  | 'developer';     // Developer portal workspace

interface WorkspaceConfig {
  id: WorkspaceType;
  name: string;
  icon: string;
  color: string;
  shortcuts: Array<{
    label: string;
    action: string;
    icon: string;
    hotkey?: string;
  }>;
  tools: Array<{
    label: string;
    component: string;
    icon: string;
    description: string;
  }>;
}

interface UIState {
  sidebarOpen: boolean;
  currentPage: string;
  layoutMode: LayoutMode; // Fluxo Layout Mode
  
  // Contextual Workspaces - Grande Síntese Initiative II
  currentWorkspace: WorkspaceType;
  workspaceConfigs: Record<WorkspaceType, WorkspaceConfig>;
  
  notifications: Array<{
    id: string;
    message: string;
    type: 'info' | 'success' | 'warning' | 'error';
    timestamp: Date;
  }>;
  
  // Actions
  toggleSidebar: () => void;
  setSidebarOpen: (open: boolean) => void;
  setCurrentPage: (page: string) => void;
  setLayoutMode: (mode: LayoutMode) => void; // Fluxo Layout Mode setter
  toggleLayoutMode: () => void; // Fluxo Layout Mode toggle
  
  // Contextual Workspaces actions
  setCurrentWorkspace: (workspace: WorkspaceType) => void;
  getWorkspaceTools: (workspace: WorkspaceType) => WorkspaceConfig['tools'];
  getWorkspaceShortcuts: (workspace: WorkspaceType) => WorkspaceConfig['shortcuts'];
  
  addNotification: (notification: Omit<UIState['notifications'][0], 'id' | 'timestamp'>) => void;
  removeNotification: (id: string) => void;
  clearNotifications: () => void;
}

export const useUIStore = create<UIState>((set, get) => ({
  sidebarOpen: true,
  currentPage: '/dashboard',
  layoutMode: 'comfortable', // Fluxo default layout mode
  currentWorkspace: 'dashboard',
  notifications: [],

  // Contextual Workspaces Configuration - Fluxo Design System
  workspaceConfigs: {
    dashboard: {
      id: 'dashboard',
      name: 'Visão Geral',
      icon: '🏠',
      color: '#0077FF',
      shortcuts: [
        { label: 'Relatório Rápido', action: 'quick_report', icon: '📊', hotkey: 'Ctrl+R' },
        { label: 'Nova Auditoria', action: 'new_audit', icon: '🔍', hotkey: 'Ctrl+N' },
        { label: 'Consultor IA', action: 'ai_consultant', icon: '🧠' }
      ],
      tools: [
        { label: 'Métricas ao Vivo', component: 'LiveMetrics', icon: '📈', description: 'Indicadores em tempo real' },
        { label: 'Atividade Recente', component: 'RecentActivity', icon: '⏱️', description: 'Últimas ações do sistema' }
      ]
    },
    payroll: {
      id: 'payroll',
      name: 'Folha de Pagamento',
      icon: '💰',
      color: '#10B981',
      shortcuts: [
        { label: 'Processar Folha', action: 'process_payroll', icon: '⚙️', hotkey: 'Ctrl+P' },
        { label: 'Relatório Folha', action: 'payroll_report', icon: '📋' },
        { label: 'Validar Dados', action: 'validate_data', icon: '✓' }
      ],
      tools: [
        { label: 'Calculadora Folha', component: 'PayrollCalculator', icon: '🧮', description: 'Cálculos automáticos' },
        { label: 'Histórico Folhas', component: 'PayrollHistory', icon: '📚', description: 'Histórico de processamento' }
      ]
    },
    audit: {
      id: 'audit',
      name: 'Auditoria',
      icon: '🔍',
      color: '#F59E0B',
      shortcuts: [
        { label: 'Nova Auditoria', action: 'new_audit', icon: '📝', hotkey: 'Ctrl+A' },
        { label: 'Consultor Riscos', action: 'risk_consultant', icon: '⚠️' },
        { label: 'Template Auditoria', action: 'audit_template', icon: '📄' }
      ],
      tools: [
        { label: 'Analisador Riscos', component: 'RiskAnalyzer', icon: '🎯', description: 'Análise de riscos automatizada' },
        { label: 'Trilha Auditoria', component: 'AuditTrail', icon: '👣', description: 'Rastros de alterações' }
      ]
    },
    reports: {
      id: 'reports',
      name: 'Relatórios',
      icon: '📊',
      color: '#8B5CF6',
      shortcuts: [
        { label: 'Relatório Personalizado', action: 'custom_report', icon: '🎨', hotkey: 'Ctrl+Shift+R' },
        { label: 'Exportar PDF', action: 'export_pdf', icon: '📄' },
        { label: 'Agendar Relatório', action: 'schedule_report', icon: '⏰' }
      ],
      tools: [
        { label: 'Builder Relatórios', component: 'ReportBuilder', icon: '🏗️', description: 'Construtor visual de relatórios' },
        { label: 'Analytics', component: 'Analytics', icon: '📈', description: 'Análises avançadas' }
      ]
    },
    ai_consultant: {
      id: 'ai_consultant',
      name: 'Consultor IA',
      icon: '🧠',
      color: '#EC4899',
      shortcuts: [
        { label: 'Nova Consulta', action: 'new_consultation', icon: '💬', hotkey: 'Ctrl+I' },
        { label: 'Histórico IA', action: 'ai_history', icon: '📜' },
        { label: 'Feedback IA', action: 'ai_feedback', icon: '⭐' }
      ],
      tools: [
        { label: 'Chat IA', component: 'AIChat', icon: '💭', description: 'Conversação com IA' },
        { label: 'Análise Preditiva', component: 'PredictiveAnalysis', icon: '🔮', description: 'Previsões inteligentes' }
      ]
    },
    documents: {
      id: 'documents',
      name: 'Documentos',
      icon: '📁',
      color: '#14B8A6',
      shortcuts: [
        { label: 'Upload Documento', action: 'upload_doc', icon: '⬆️', hotkey: 'Ctrl+U' },
        { label: 'Buscar Documento', action: 'search_doc', icon: '🔍' },
        { label: 'OCR Documento', action: 'ocr_doc', icon: '👁️' }
      ],
      tools: [
        { label: 'Gerenciador Arquivos', component: 'FileManager', icon: '🗃️', description: 'Organização de documentos' },
        { label: 'OCR Engine', component: 'OCREngine', icon: '📖', description: 'Extração de texto' }
      ]
    },
    admin: {
      id: 'admin',
      name: 'Administração',
      icon: '⚙️',
      color: '#6366F1',
      shortcuts: [
        { label: 'Gerenciar Usuários', action: 'manage_users', icon: '👥', hotkey: 'Ctrl+Shift+U' },
        { label: 'Configurações', action: 'settings', icon: '⚙️' },
        { label: 'Logs Sistema', action: 'system_logs', icon: '📋' }
      ],
      tools: [
        { label: 'User Manager', component: 'UserManager', icon: '👤', description: 'Gestão de utilizadores' },
        { label: 'System Monitor', component: 'SystemMonitor', icon: '📊', description: 'Monitorização do sistema' }
      ]
    },
    developer: {
      id: 'developer',
      name: 'Desenvolvedor',
      icon: '👨‍💻',
      color: '#EF4444',
      shortcuts: [
        { label: 'API Keys', action: 'api_keys', icon: '🔑', hotkey: 'Ctrl+K' },
        { label: 'Documentação API', action: 'api_docs', icon: '📖' },
        { label: 'Teste Endpoints', action: 'test_endpoints', icon: '🧪' }
      ],
      tools: [
        { label: 'API Explorer', component: 'APIExplorer', icon: '🗺️', description: 'Explorador de APIs' },
        { label: 'Webhook Manager', component: 'WebhookManager', icon: '🪝', description: 'Gestão de webhooks' }
      ]
    }
  },

  toggleSidebar: () => {
    const { sidebarOpen } = get();
    set({ sidebarOpen: !sidebarOpen });
  },

  setSidebarOpen: (open) => {
    set({ sidebarOpen: open });
  },

  setCurrentPage: (page) => {
    set({ currentPage: page });
    
    // Auto-detect workspace based on current page
    const state = get();
    let detectedWorkspace: WorkspaceType = 'dashboard';
    
    if (page.includes('/payroll')) detectedWorkspace = 'payroll';
    else if (page.includes('/audit')) detectedWorkspace = 'audit';
    else if (page.includes('/reports')) detectedWorkspace = 'reports';
    else if (page.includes('/consultor') || page.includes('/ai')) detectedWorkspace = 'ai_consultant';
    else if (page.includes('/documents')) detectedWorkspace = 'documents';
    else if (page.includes('/admin')) detectedWorkspace = 'admin';
    else if (page.includes('/developer')) detectedWorkspace = 'developer';
    
    if (state.currentWorkspace !== detectedWorkspace) {
      state.setCurrentWorkspace(detectedWorkspace);
    }
  },

  // Fluxo Layout Mode management
  setLayoutMode: (mode) => {
    set({ layoutMode: mode });
    // Apply layout mode class to body for global CSS effects
    document.body.className = document.body.className.replace(/fluxo-layout-\w+/g, '');
    document.body.classList.add(`fluxo-layout-${mode}`);
  },

  toggleLayoutMode: () => {
    const { layoutMode, setLayoutMode } = get();
    const newMode = layoutMode === 'comfortable' ? 'compact' : 'comfortable';
    setLayoutMode(newMode);
  },

  // Contextual Workspaces actions
  setCurrentWorkspace: (workspace) => {
    set({ currentWorkspace: workspace });
    
    // Apply workspace-specific CSS class
    document.body.className = document.body.className.replace(/fluxo-workspace-\w+/g, '');
    document.body.classList.add(`fluxo-workspace-${workspace}`);
    
    // Emit custom event for ACR tracking
    if (typeof window !== 'undefined') {
      window.dispatchEvent(new CustomEvent('fluxo:workspace:change', {
        detail: { workspace, timestamp: new Date().toISOString() }
      }));
    }
  },

  getWorkspaceTools: (workspace) => {
    const { workspaceConfigs } = get();
    return workspaceConfigs[workspace]?.tools || [];
  },

  getWorkspaceShortcuts: (workspace) => {
    const { workspaceConfigs } = get();
    return workspaceConfigs[workspace]?.shortcuts || [];
  },

  addNotification: (notification) => {
    const id = Math.random().toString(36).substr(2, 9);
    const newNotification = {
      ...notification,
      id,
      timestamp: new Date(),
    };
    
    set((state) => ({
      notifications: [...state.notifications, newNotification],
    }));
  },

  removeNotification: (id) => {
    set((state) => ({
      notifications: state.notifications.filter((n) => n.id !== id),
    }));
  },

  clearNotifications: () => {
    set({ notifications: [] });
  },
}));