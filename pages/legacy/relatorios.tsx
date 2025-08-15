import React, { useState, useEffect } from "react";
import Head from 'next/head';
import { useRouter } from 'next/router';
import {
  Container,
  Typography,
  Box,
  Paper,
  Card,
  CardContent,
  Button,
  Chip,
  IconButton,
  Select,
  MenuItem,
  FormControl,
  InputLabel,
} from "@mui/material";
import {
  Assessment,
  Download,
  Visibility,
  Share,
  DateRange,
} from "@mui/icons-material";
import { authHelpers } from '../../lib/supabaseClient';

interface Report {
  id: number;
  title: string;
  description: string;
  type: 'Mensal' | 'Trimestral' | 'Anual' | 'Personalizado';
  status: 'Disponível' | 'Processando' | 'Erro';
  generated_date: string;
  size: string;
}

export default function RelatoriosPage() {
  const [user, setUser] = useState(null);
  const [reports, setReports] = useState<Report[]>([]);
  const [filteredReports, setFilteredReports] = useState<Report[]>([]);
  const [typeFilter, setTypeFilter] = useState('');
  const [loading, setLoading] = useState(true);
  const router = useRouter();

  useEffect(() => {
    const checkUser = async () => {
      try {
        const currentUser = await authHelpers.getCurrentUser();
        if (!currentUser) {
          router.push('/login');
          return;
        }
        setUser(currentUser);
        
        // Mock data for now
        const mockReports: Report[] = [
          {
            id: 1,
            title: "Relatório Mensal de Auditoria - Janeiro 2024",
            description: "Relatório completo das atividades de auditoria realizadas no mês de janeiro",
            type: 'Mensal',
            status: 'Disponível',
            generated_date: '2024-01-31',
            size: '2.3 MB'
          },
          {
            id: 2,
            title: "Análise Trimestral de Compliance",
            description: "Análise detalhada do compliance trabalhista no último trimestre",
            type: 'Trimestral',
            status: 'Disponível',
            generated_date: '2024-01-30',
            size: '4.7 MB'
          },
          {
            id: 3,
            title: "Relatório Anual de Desempenho",
            description: "Relatório consolidado do desempenho da empresa em 2023",
            type: 'Anual',
            status: 'Processando',
            generated_date: '2024-01-29',
            size: '0 MB'
          },
          {
            id: 4,
            title: "Dashboard Executivo - Personalizado",
            description: "Relatório personalizado com métricas específicas solicitadas",
            type: 'Personalizado',
            status: 'Disponível',
            generated_date: '2024-01-28',
            size: '1.8 MB'
          }
        ];
        setReports(mockReports);
        setFilteredReports(mockReports);
      } catch (error) {
        console.error('Error checking user:', error);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkUser();
  }, [router]);

  const handleTypeFilter = (type: string) => {
    setTypeFilter(type);
    if (type === '') {
      setFilteredReports(reports);
    } else {
      setFilteredReports(reports.filter(report => report.type === type));
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Disponível': return 'success';
      case 'Processando': return 'warning';
      case 'Erro': return 'error';
      default: return 'default';
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'Mensal': return 'primary';
      case 'Trimestral': return 'secondary';
      case 'Anual': return 'info';
      case 'Personalizado': return 'warning';
      default: return 'default';
    }
  };

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography>Carregando...</Typography>
      </Container>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <>
      <Head>
        <title>Relatórios - AUDITORIA360</title>
        <meta name="description" content="Relatórios e análises do AUDITORIA360" />
        <meta name="robots" content="noindex" />
      </Head>
      
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Relatórios
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Acesse relatórios de auditoria, compliance e desempenho da sua empresa.
          </Typography>
        </Box>

        {/* Quick Stats */}
        <Box sx={{ display: 'grid', gap: 3, gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', mb: 4 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="primary">
                Total de Relatórios
              </Typography>
              <Typography variant="h3" color="text.primary">
                {reports.length}
              </Typography>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" color="success.main">
                Disponíveis
              </Typography>
              <Typography variant="h3" color="text.primary">
                {reports.filter(r => r.status === 'Disponível').length}
              </Typography>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" color="warning.main">
                Processando
              </Typography>
              <Typography variant="h3" color="text.primary">
                {reports.filter(r => r.status === 'Processando').length}
              </Typography>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" color="info.main">
                Este Mês
              </Typography>
              <Typography variant="h3" color="text.primary">
                {reports.filter(r => r.generated_date.includes('2024-01')).length}
              </Typography>
            </CardContent>
          </Card>
        </Box>

        {/* Filter and Actions */}
        <Paper sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', gap: 2, alignItems: 'center', flexWrap: 'wrap' }}>
            <FormControl size="small" sx={{ minWidth: 150 }}>
              <InputLabel>Tipo de Relatório</InputLabel>
              <Select
                value={typeFilter}
                onChange={(e) => handleTypeFilter(e.target.value)}
                label="Tipo de Relatório"
              >
                <MenuItem value="">Todos</MenuItem>
                <MenuItem value="Mensal">Mensal</MenuItem>
                <MenuItem value="Trimestral">Trimestral</MenuItem>
                <MenuItem value="Anual">Anual</MenuItem>
                <MenuItem value="Personalizado">Personalizado</MenuItem>
              </Select>
            </FormControl>
            
            <Button
              variant="contained"
              startIcon={<Assessment />}
              color="primary"
            >
              Gerar Novo Relatório
            </Button>
            
            <Button
              variant="outlined"
              startIcon={<DateRange />}
              color="primary"
            >
              Relatório Personalizado
            </Button>
          </Box>
        </Paper>

        {/* Reports Grid */}
        <Box sx={{ display: 'grid', gap: 3, gridTemplateColumns: 'repeat(auto-fill, minmax(350px, 1fr))' }}>
          {filteredReports.map((report) => (
            <Card key={report.id} sx={{ position: 'relative' }}>
              <CardContent>
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', mb: 2 }}>
                  <Typography variant="h6" component="h3" sx={{ flex: 1 }}>
                    {report.title}
                  </Typography>
                  <Box sx={{ display: 'flex', gap: 1 }}>
                    <Chip
                      label={report.type}
                      color={getTypeColor(report.type) as any}
                      size="small"
                    />
                    <Chip
                      label={report.status}
                      color={getStatusColor(report.status) as any}
                      size="small"
                    />
                  </Box>
                </Box>
                
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  {report.description}
                </Typography>
                
                <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
                  <Typography variant="caption" color="text.secondary">
                    Gerado em: {report.generated_date}
                  </Typography>
                  <Typography variant="caption" color="text.secondary">
                    Tamanho: {report.size}
                  </Typography>
                </Box>
                
                <Box sx={{ display: 'flex', gap: 1 }}>
                  <IconButton
                    size="small"
                    color="primary"
                    disabled={report.status !== 'Disponível'}
                    title="Visualizar"
                  >
                    <Visibility />
                  </IconButton>
                  <IconButton
                    size="small"
                    color="primary"
                    disabled={report.status !== 'Disponível'}
                    title="Download"
                  >
                    <Download />
                  </IconButton>
                  <IconButton
                    size="small"
                    color="primary"
                    disabled={report.status !== 'Disponível'}
                    title="Compartilhar"
                  >
                    <Share />
                  </IconButton>
                </Box>
              </CardContent>
            </Card>
          ))}
        </Box>
      </Container>
    </>
  );
}