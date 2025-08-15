import { create } from 'zustand';
import { persist } from 'zustand/middleware';

export interface Widget {
  id: string;
  type: 'kpi' | 'health-map' | 'activity-feed' | 'chart' | 'table' | 'custom';
  title: string;
  size: 'small' | 'medium' | 'large' | 'x-large';
  position: { x: number; y: number; w: number; h: number };
  config: Record<string, any>;
  visible: boolean;
  refreshInterval?: number; // in seconds
  lastRefresh?: Date;
  data?: any;
}

export interface DashboardLayout {
  id: string;
  name: string;
  widgets: Widget[];
  isDefault: boolean;
}

interface DashboardState {
  layouts: DashboardLayout[];
  currentLayoutId: string;
  editMode: boolean;
  
  // Actions
  createLayout: (name: string) => string;
  deleteLayout: (layoutId: string) => void;
  setCurrentLayout: (layoutId: string) => void;
  setEditMode: (editMode: boolean) => void;
  
  // Widget actions
  addWidget: (widget: Omit<Widget, 'id'>) => void;
  updateWidget: (widgetId: string, updates: Partial<Widget>) => void;
  removeWidget: (widgetId: string) => void;
  updateWidgetPosition: (widgetId: string, position: Widget['position']) => void;
  refreshWidget: (widgetId: string, data: any) => void;
  
  // Getters
  getCurrentLayout: () => DashboardLayout | undefined;
  getWidget: (widgetId: string) => Widget | undefined;
}

const defaultWidgets: Widget[] = [
  {
    id: 'kpi_overview',
    type: 'kpi',
    title: 'Visão Geral KPIs',
    size: 'large',
    position: { x: 0, y: 0, w: 6, h: 3 },
    config: {
      metrics: ['total_clients', 'active_audits', 'pending_documents']
    },
    visible: true,
    refreshInterval: 300, // 5 minutes
  },
  {
    id: 'health_map',
    type: 'health-map',
    title: 'Mapa de Saúde',
    size: 'medium',
    position: { x: 6, y: 0, w: 6, h: 3 },
    config: {
      showLegend: true,
      groupBy: 'status'
    },
    visible: true,
    refreshInterval: 600, // 10 minutes
  },
  {
    id: 'activity_feed',
    type: 'activity-feed',
    title: 'Atividades Recentes',
    size: 'medium',
    position: { x: 0, y: 3, w: 12, h: 4 },
    config: {
      maxItems: 10,
      showTimestamps: true
    },
    visible: true,
    refreshInterval: 60, // 1 minute
  },
];

const defaultLayout: DashboardLayout = {
  id: 'default',
  name: 'Layout Padrão',
  widgets: defaultWidgets,
  isDefault: true,
};

export const useDashboardStore = create<DashboardState>()(
  persist(
    (set, get) => ({
      layouts: [defaultLayout],
      currentLayoutId: 'default',
      editMode: false,

      createLayout: (name) => {
        const id = `layout_${Date.now()}`;
        const newLayout: DashboardLayout = {
          id,
          name,
          widgets: [],
          isDefault: false,
        };

        set((state) => ({
          layouts: [...state.layouts, newLayout],
          currentLayoutId: id,
        }));

        return id;
      },

      deleteLayout: (layoutId) => {
        set((state) => {
          const layouts = state.layouts.filter(l => l.id !== layoutId && !l.isDefault);
          const currentLayoutId = state.currentLayoutId === layoutId 
            ? layouts.find(l => l.isDefault)?.id || layouts[0]?.id || 'default'
            : state.currentLayoutId;
          
          return { layouts, currentLayoutId };
        });
      },

      setCurrentLayout: (currentLayoutId) => {
        set({ currentLayoutId });
      },

      setEditMode: (editMode) => {
        set({ editMode });
      },

      addWidget: (widgetData) => {
        const widget: Widget = {
          ...widgetData,
          id: `widget_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`,
        };

        set((state) => ({
          layouts: state.layouts.map(layout =>
            layout.id === state.currentLayoutId
              ? { ...layout, widgets: [...layout.widgets, widget] }
              : layout
          ),
        }));
      },

      updateWidget: (widgetId, updates) => {
        set((state) => ({
          layouts: state.layouts.map(layout =>
            layout.id === state.currentLayoutId
              ? {
                  ...layout,
                  widgets: layout.widgets.map(widget =>
                    widget.id === widgetId ? { ...widget, ...updates } : widget
                  ),
                }
              : layout
          ),
        }));
      },

      removeWidget: (widgetId) => {
        set((state) => ({
          layouts: state.layouts.map(layout =>
            layout.id === state.currentLayoutId
              ? {
                  ...layout,
                  widgets: layout.widgets.filter(widget => widget.id !== widgetId),
                }
              : layout
          ),
        }));
      },

      updateWidgetPosition: (widgetId, position) => {
        get().updateWidget(widgetId, { position });
      },

      refreshWidget: (widgetId, data) => {
        get().updateWidget(widgetId, { data, lastRefresh: new Date() });
      },

      getCurrentLayout: () => {
        const { layouts, currentLayoutId } = get();
        return layouts.find(layout => layout.id === currentLayoutId);
      },

      getWidget: (widgetId) => {
        const currentLayout = get().getCurrentLayout();
        return currentLayout?.widgets.find(widget => widget.id === widgetId);
      },
    }),
    {
      name: 'dashboard-state',
    }
  )
);