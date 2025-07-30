import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  CardActions,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Chip,
  Avatar,
  Divider,
  Alert,
  Skeleton,
} from '@mui/material';
import {
  Business,
  TrendingUp,
  Assessment,
  Security,
  Speed,
  AttachMoney,
  People,
  CheckCircle,
  Warning,
  Error,
  Info,
} from '@mui/icons-material';
import { useAuthStore } from '../../stores/authStore';

interface DashboardTemplate {
  id: string;
  name: string;
  description: string;
  segment: string;
  icon: React.ReactNode;
  color: string;
  widgets: DashboardWidget[];
  isRecommended?: boolean;
}

interface DashboardWidget {
  id: string;
  title: string;
  type: 'metric' | 'chart' | 'list' | 'alert';
  size: 'small' | 'medium' | 'large';
  position: { x: number; y: number };
  data?: any;
  config?: any;
}

interface SegmentDashboardProps {
  onTemplateSelect?: (template: DashboardTemplate) => void;
}

const SegmentDashboard: React.FC<SegmentDashboardProps> = ({ onTemplateSelect }) => {
  const { user } = useAuthStore();
  const [selectedSegment, setSelectedSegment] = useState<string>('');
  const [selectedTemplate, setSelectedTemplate] = useState<DashboardTemplate | null>(null);
  const [previewDialogOpen, setPreviewDialogOpen] = useState(false);
  const [loading, setLoading] = useState(false);

  const dashboardTemplates: DashboardTemplate[] = [
    {
      id: 'startups',
      name: 'Dashboard para Startups',
      description: 'Métricas essenciais para startups e empresas de tecnologia em crescimento rápido',
      segment: 'Startups',
      icon: <TrendingUp />,
      color: '#4CAF50',
      isRecommended: user?.preferred_segment === 'Startups',
      widgets: [
        {
          id: 'burn_rate',
          title: 'Burn Rate Mensal',
          type: 'metric',
          size: 'medium',
          position: { x: 0, y: 0 },
          data: { value: 'R$ 45.000', trend: '+12%', status: 'warning' }
        },
        {
          id: 'runway',
          title: 'Runway (meses)',
          type: 'metric', 
          size: 'medium',
          position: { x: 1, y: 0 },
          data: { value: '18', trend: '-2', status: 'info' }
        },
        {
          id: 'team_growth',
          title: 'Crescimento da Equipe',
          type: 'chart',
          size: 'large',
          position: { x: 0, y: 1 },
          data: { type: 'line', labels: ['Jan', 'Fev', 'Mar', 'Abr'], values: [5, 8, 12, 15] }
        },
        {
          id: 'compliance_score',
          title: 'Score de Compliance',
          type: 'metric',
          size: 'small',
          position: { x: 2, y: 0 },
          data: { value: '92%', status: 'success' }
        },
        {
          id: 'tax_optimization',
          title: 'Otimização Tributária',
          type: 'alert',
          size: 'medium',
          position: { x: 0, y: 2 },
          data: { 
            message: 'Empresa elegível para incentivos fiscais de inovação',
            severity: 'info',
            actionText: 'Saiba mais'
          }
        }
      ]
    },
    {
      id: 'varejo',
      name: 'Dashboard para Varejo',
      description: 'Indicadores de performance para empresas do setor varejista',
      segment: 'Varejo',
      icon: <Business />,
      color: '#2196F3',
      isRecommended: user?.preferred_segment === 'Varejo',
      widgets: [
        {
          id: 'sales_revenue',
          title: 'Faturamento Mensal',
          type: 'metric',
          size: 'large',
          position: { x: 0, y: 0 },
          data: { value: 'R$ 2.450.000', trend: '+8.5%', status: 'success' }
        },
        {
          id: 'inventory_turnover',
          title: 'Giro de Estoque',
          type: 'metric',
          size: 'medium',
          position: { x: 1, y: 0 },
          data: { value: '4.2x', trend: '+0.3', status: 'success' }
        },
        {
          id: 'profit_margin',
          title: 'Margem de Lucro',
          type: 'metric',
          size: 'medium',
          position: { x: 2, y: 0 },
          data: { value: '15.8%', trend: '-1.2%', status: 'warning' }
        },
        {
          id: 'tax_burden',
          title: 'Carga Tributária',
          type: 'chart',
          size: 'medium',
          position: { x: 0, y: 1 },
          data: { type: 'donut', labels: ['ICMS', 'PIS/COFINS', 'Outros'], values: [45, 30, 25] }
        },
        {
          id: 'seasonal_performance',
          title: 'Performance Sazonal',
          type: 'chart',
          size: 'large',
          position: { x: 1, y: 1 },
          data: { type: 'bar', labels: ['Q1', 'Q2', 'Q3', 'Q4'], values: [85, 120, 95, 150] }
        }
      ]
    },
    {
      id: 'saude',
      name: 'Dashboard para Serviços de Saúde',
      description: 'Métricas especializadas para clínicas, hospitais e operadoras de saúde',
      segment: 'Serviços de Saúde',
      icon: <Security />,
      color: '#FF5722',
      isRecommended: user?.preferred_segment === 'Serviços de Saúde',
      widgets: [
        {
          id: 'patient_volume',
          title: 'Volume de Pacientes',
          type: 'metric',
          size: 'medium',
          position: { x: 0, y: 0 },
          data: { value: '1.250', trend: '+5.2%', status: 'success' }
        },
        {
          id: 'ans_compliance',
          title: 'Compliance ANS',
          type: 'metric',
          size: 'medium',
          position: { x: 1, y: 0 },
          data: { value: '98.5%', trend: '+0.3%', status: 'success' }
        },
        {
          id: 'regulatory_alerts',
          title: 'Alertas Regulatórios',
          type: 'list',
          size: 'large',
          position: { x: 0, y: 1 },
          data: {
            items: [
              { title: 'Renovação ANVISA', status: 'pending', dueDate: '15/02/2024' },
              { title: 'Auditoria CRM', status: 'completed', completedDate: '10/01/2024' },
              { title: 'Certificação ISO', status: 'in_progress', progress: 75 }
            ]
          }
        },
        {
          id: 'financial_health',
          title: 'Saúde Financeira',
          type: 'metric',
          size: 'small',
          position: { x: 2, y: 0 },
          data: { value: 'Boa', status: 'success' }
        },
        {
          id: 'quality_metrics',
          title: 'Indicadores de Qualidade',
          type: 'chart',
          size: 'medium',
          position: { x: 2, y: 1 },
          data: { type: 'radar', metrics: ['Satisfação', 'Tempo Espera', 'Precisão', 'Segurança'], values: [90, 85, 95, 98] }
        }
      ]
    },
    {
      id: 'industrial',
      name: 'Dashboard Industrial',
      description: 'Indicadores para empresas do setor industrial e manufatura',
      segment: 'Industrial',
      icon: <Speed />,
      color: '#9C27B0',
      widgets: [
        {
          id: 'production_efficiency',
          title: 'Eficiência Produtiva',
          type: 'metric',
          size: 'large',
          position: { x: 0, y: 0 },
          data: { value: '87.3%', trend: '+2.1%', status: 'success' }
        },
        {
          id: 'waste_reduction',
          title: 'Redução de Desperdício',
          type: 'metric',
          size: 'medium',
          position: { x: 1, y: 0 },
          data: { value: '12.5%', trend: '-3.2%', status: 'success' }
        },
        {
          id: 'environmental_compliance',
          title: 'Compliance Ambiental',
          type: 'metric',
          size: 'medium',
          position: { x: 2, y: 0 },
          data: { value: '95%', status: 'success' }
        },
        {
          id: 'cost_breakdown',
          title: 'Breakdown de Custos',
          type: 'chart',
          size: 'large',
          position: { x: 0, y: 1 },
          data: { type: 'waterfall', categories: ['Material', 'Mão de obra', 'Energia', 'Overhead'], values: [40, 30, 15, 15] }
        }
      ]
    },
    {
      id: 'servicos',
      name: 'Dashboard para Serviços',
      description: 'Métricas para empresas de consultoria e prestação de serviços',
      segment: 'Serviços',
      icon: <People />,
      color: '#FF9800',
      widgets: [
        {
          id: 'billable_hours',
          title: 'Horas Faturáveis',
          type: 'metric',
          size: 'medium',
          position: { x: 0, y: 0 },
          data: { value: '1.840h', trend: '+120h', status: 'success' }
        },
        {
          id: 'client_satisfaction',
          title: 'Satisfação do Cliente',
          type: 'metric',
          size: 'medium',
          position: { x: 1, y: 0 },
          data: { value: '4.8/5', trend: '+0.2', status: 'success' }
        },
        {
          id: 'utilization_rate',
          title: 'Taxa de Utilização',
          type: 'metric',
          size: 'medium',
          position: { x: 2, y: 0 },
          data: { value: '78%', trend: '+5%', status: 'info' }
        },
        {
          id: 'project_profitability',
          title: 'Rentabilidade por Projeto',
          type: 'chart',
          size: 'large',
          position: { x: 0, y: 1 },
          data: { type: 'bubble', projects: [
            { name: 'Projeto A', margin: 25, hours: 200, revenue: 50000 },
            { name: 'Projeto B', margin: 18, hours: 150, revenue: 35000 },
            { name: 'Projeto C', margin: 32, hours: 300, revenue: 80000 }
          ]}
        }
      ]
    }
  ];

  const handleSegmentSelect = (segment: string) => {
    setSelectedSegment(segment);
  };

  const handleTemplatePreview = (template: DashboardTemplate) => {
    setSelectedTemplate(template);
    setPreviewDialogOpen(true);
  };

  const handleTemplateSelect = (template: DashboardTemplate) => {
    setLoading(true);
    
    // Simulate API call to apply template
    setTimeout(() => {
      setLoading(false);
      setPreviewDialogOpen(false);
      
      // Update user preferences
      // await userService.updateDashboardPreferences({
      //   preferred_segment: template.segment,
      //   dashboard_template: template.id
      // });
      
      if (onTemplateSelect) {
        onTemplateSelect(template);
      }
      
      // Show success message
      alert(`Dashboard ${template.name} aplicado com sucesso!`);
    }, 2000);
  };

  const getFilteredTemplates = () => {
    if (!selectedSegment) return dashboardTemplates;
    return dashboardTemplates.filter(template => template.segment === selectedSegment);
  };

  const renderWidget = (widget: DashboardWidget) => {
    switch (widget.type) {
      case 'metric':
        return (
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" color="text.secondary" gutterBottom>
                {widget.title}
              </Typography>
              <Typography variant="h4" component="div">
                {widget.data?.value}
              </Typography>
              {widget.data?.trend && (
                <Typography variant="body2" color={widget.data.status === 'success' ? 'success.main' : widget.data.status === 'warning' ? 'warning.main' : 'info.main'}>
                  {widget.data.trend}
                </Typography>
              )}
            </CardContent>
          </Card>
        );
      
      case 'chart':
        return (
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {widget.title}
              </Typography>
              <Box sx={{ height: 120, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: 'grey.100', borderRadius: 1 }}>
                <Typography variant="body2" color="text.secondary">
                  Gráfico: {widget.data?.type}
                </Typography>
              </Box>
            </CardContent>
          </Card>
        );
      
      case 'list':
        return (
          <Card variant="outlined" sx={{ height: '100%' }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                {widget.title}
              </Typography>
              {widget.data?.items?.map((item: any, index: number) => (
                <Box key={index} sx={{ display: 'flex', justifyContent: 'space-between', py: 0.5 }}>
                  <Typography variant="body2">{item.title}</Typography>
                  <Chip size="small" label={item.status} color={item.status === 'completed' ? 'success' : item.status === 'pending' ? 'warning' : 'info'} />
                </Box>
              ))}
            </CardContent>
          </Card>
        );
      
      case 'alert':
        return (
          <Alert severity={widget.data?.severity || 'info'} action={
            widget.data?.actionText && (
              <Button size="small" color="inherit">
                {widget.data.actionText}
              </Button>
            )
          }>
            {widget.data?.message}
          </Alert>
        );
      
      default:
        return <Box sx={{ height: '100%', bgcolor: 'grey.100', borderRadius: 1 }} />;
    }
  };

  return (
    <Box>
      {/* Header */}
      <Box sx={{ mb: 4 }}>
        <Typography variant="h4" component="h1" gutterBottom>
          Templates de Dashboard por Segmento
        </Typography>
        <Typography variant="body1" color="text.secondary" paragraph>
          Escolha um template otimizado para o seu segmento de negócio. Cada template contém 
          KPIs e métricas mais relevantes para sua área de atuação.
        </Typography>
        
        {user?.preferred_segment && (
          <Alert severity="info" sx={{ mt: 2 }}>
            Baseado no seu perfil, recomendamos o template para <strong>{user.preferred_segment}</strong>
          </Alert>
        )}
      </Box>

      {/* Segment Filter */}
      <Box sx={{ mb: 4 }}>
        <FormControl sx={{ minWidth: 250 }}>
          <InputLabel>Filtrar por segmento</InputLabel>
          <Select
            value={selectedSegment}
            label="Filtrar por segmento"
            onChange={(e) => handleSegmentSelect(e.target.value)}
          >
            <MenuItem value="">Todos os segmentos</MenuItem>
            <MenuItem value="Startups">Startups</MenuItem>
            <MenuItem value="Varejo">Varejo</MenuItem>
            <MenuItem value="Serviços de Saúde">Serviços de Saúde</MenuItem>
            <MenuItem value="Industrial">Industrial</MenuItem>
            <MenuItem value="Serviços">Serviços</MenuItem>
          </Select>
        </FormControl>
      </Box>

      {/* Templates Grid */}
      <Grid container spacing={3}>
        {getFilteredTemplates().map((template) => (
          <Grid item xs={12} md={6} lg={4} key={template.id}>
            <Card 
              sx={{ 
                height: '100%', 
                position: 'relative',
                border: template.isRecommended ? 2 : 1,
                borderColor: template.isRecommended ? 'primary.main' : 'divider',
              }}
            >
              {template.isRecommended && (
                <Chip
                  label="Recomendado"
                  color="primary"
                  size="small"
                  sx={{ position: 'absolute', top: 8, right: 8, zIndex: 1 }}
                />
              )}
              
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                  <Avatar sx={{ bgcolor: template.color, mr: 2 }}>
                    {template.icon}
                  </Avatar>
                  <Box>
                    <Typography variant="h6">
                      {template.name}
                    </Typography>
                    <Typography variant="body2" color="text.secondary">
                      {template.segment}
                    </Typography>
                  </Box>
                </Box>
                
                <Typography variant="body2" paragraph>
                  {template.description}
                </Typography>
                
                <Box sx={{ mb: 2 }}>
                  <Typography variant="subtitle2" gutterBottom>
                    Widgets inclusos:
                  </Typography>
                  <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                    {template.widgets.slice(0, 3).map((widget) => (
                      <Chip
                        key={widget.id}
                        label={widget.title}
                        size="small"
                        variant="outlined"
                      />
                    ))}
                    {template.widgets.length > 3 && (
                      <Chip
                        label={`+${template.widgets.length - 3} mais`}
                        size="small"
                        color="primary"
                        variant="outlined"
                      />
                    )}
                  </Box>
                </Box>
              </CardContent>
              
              <CardActions>
                <Button 
                  size="small" 
                  onClick={() => handleTemplatePreview(template)}
                >
                  Visualizar
                </Button>
                <Button 
                  size="small" 
                  variant="contained" 
                  onClick={() => handleTemplateSelect(template)}
                  disabled={loading}
                >
                  Aplicar Template
                </Button>
              </CardActions>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Preview Dialog */}
      <Dialog
        open={previewDialogOpen}
        onClose={() => setPreviewDialogOpen(false)}
        maxWidth="lg"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Avatar sx={{ bgcolor: selectedTemplate?.color, mr: 2 }}>
              {selectedTemplate?.icon}
            </Avatar>
            <Box>
              <Typography variant="h6">
                {selectedTemplate?.name}
              </Typography>
              <Typography variant="body2" color="text.secondary">
                Preview do template
              </Typography>
            </Box>
          </Box>
        </DialogTitle>
        
        <DialogContent>
          {selectedTemplate && (
            <Box>
              <Typography variant="body1" paragraph>
                {selectedTemplate.description}
              </Typography>
              
              <Divider sx={{ my: 3 }} />
              
              <Typography variant="h6" gutterBottom>
                Widgets do Dashboard:
              </Typography>
              
              <Grid container spacing={2}>
                {selectedTemplate.widgets.map((widget) => (
                  <Grid 
                    item 
                    xs={widget.size === 'small' ? 4 : widget.size === 'medium' ? 6 : 12} 
                    key={widget.id}
                  >
                    {loading ? (
                      <Skeleton variant="rectangular" height={150} />
                    ) : (
                      renderWidget(widget)
                    )}
                  </Grid>
                ))}
              </Grid>
            </Box>
          )}
        </DialogContent>
        
        <DialogActions>
          <Button onClick={() => setPreviewDialogOpen(false)}>
            Cancelar
          </Button>
          <Button 
            variant="contained" 
            onClick={() => selectedTemplate && handleTemplateSelect(selectedTemplate)}
            disabled={loading}
          >
            {loading ? 'Aplicando...' : 'Aplicar Este Template'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default SegmentDashboard;