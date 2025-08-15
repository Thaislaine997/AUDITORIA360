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
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import {
  Assignment,
  Add,
  Search,
  FilterList,
} from "@mui/icons-material";
import { authHelpers } from '../../lib/supabaseClient';

interface Demand {
  id: number;
  title: string;
  client: string;
  priority: 'Alta' | 'Média' | 'Baixa';
  status: 'Aberto' | 'Em Progresso' | 'Concluído';
  created_date: string;
  assigned_to: string;
}

export default function PortalDemandas() {
  const [user, setUser] = useState(null);
  const [demands, setDemands] = useState<Demand[]>([]);
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
        const mockDemands: Demand[] = [
          {
            id: 1,
            title: "Relatório de folha de pagamento - Empresa XYZ",
            client: "Empresa XYZ",
            priority: 'Alta',
            status: 'Em Progresso',
            created_date: '2024-01-15',
            assigned_to: 'João Silva'
          },
          {
            id: 2,
            title: "Auditoria fiscal trimestral - ABC Corp",
            client: "ABC Corp",
            priority: 'Média',
            status: 'Aberto',
            created_date: '2024-01-14',
            assigned_to: 'Maria Santos'
          },
          {
            id: 3,
            title: "Certificação ISO - Tech Solutions",
            client: "Tech Solutions",
            priority: 'Baixa',
            status: 'Concluído',
            created_date: '2024-01-10',
            assigned_to: 'Pedro Costa'
          }
        ];
        setDemands(mockDemands);
      } catch (error) {
        console.error('Error checking user:', error);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkUser();
  }, [router]);

  const getPriorityColor = (priority: string) => {
    switch (priority) {
      case 'Alta': return 'error';
      case 'Média': return 'warning';
      case 'Baixa': return 'info';
      default: return 'default';
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'Concluído': return 'success';
      case 'Em Progresso': return 'primary';
      case 'Aberto': return 'default';
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
        <title>Portal de Demandas - AUDITORIA360</title>
        <meta name="description" content="Gestão de demandas e tickets do AUDITORIA360" />
        <meta name="robots" content="noindex" />
      </Head>
      
      <Container maxWidth="xl" sx={{ py: 4 }}>
        <Box sx={{ mb: 4 }}>
          <Typography variant="h4" component="h1" gutterBottom>
            Portal de Demandas
          </Typography>
          <Typography variant="subtitle1" color="text.secondary">
            Gerencie solicitações, tickets e demandas dos clientes de forma centralizada e eficiente.
          </Typography>
        </Box>

        {/* Summary Cards */}
        <Box sx={{ display: 'grid', gap: 3, gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', mb: 4 }}>
          <Card>
            <CardContent>
              <Typography variant="h6" color="primary">
                Total de Demandas
              </Typography>
              <Typography variant="h3" color="text.primary">
                {demands.length}
              </Typography>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" color="warning.main">
                Em Progresso
              </Typography>
              <Typography variant="h3" color="text.primary">
                {demands.filter(d => d.status === 'Em Progresso').length}
              </Typography>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" color="success.main">
                Concluídas
              </Typography>
              <Typography variant="h3" color="text.primary">
                {demands.filter(d => d.status === 'Concluído').length}
              </Typography>
            </CardContent>
          </Card>
          
          <Card>
            <CardContent>
              <Typography variant="h6" color="error.main">
                Alta Prioridade
              </Typography>
              <Typography variant="h3" color="text.primary">
                {demands.filter(d => d.priority === 'Alta').length}
              </Typography>
            </CardContent>
          </Card>
        </Box>

        {/* Demands Table */}
        <Paper sx={{ p: 3 }}>
          <Box sx={{ display: "flex", justifyContent: "space-between", alignItems: "center", mb: 3 }}>
            <Typography variant="h6">
              Lista de Demandas
            </Typography>
            <Button
              variant="contained"
              startIcon={<Add />}
              color="primary"
            >
              Nova Demanda
            </Button>
          </Box>
          
          <Box sx={{ display: "flex", gap: 2, mb: 3 }}>
            <Button variant="outlined" startIcon={<Search />}>
              Buscar
            </Button>
            <Button variant="outlined" startIcon={<FilterList />}>
              Filtrar
            </Button>
          </Box>

          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>ID</TableCell>
                  <TableCell>Título</TableCell>
                  <TableCell>Cliente</TableCell>
                  <TableCell>Prioridade</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Data Criação</TableCell>
                  <TableCell>Responsável</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {demands.map((demand) => (
                  <TableRow key={demand.id}>
                    <TableCell>#{demand.id}</TableCell>
                    <TableCell>{demand.title}</TableCell>
                    <TableCell>{demand.client}</TableCell>
                    <TableCell>
                      <Chip
                        label={demand.priority}
                        color={getPriorityColor(demand.priority) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={demand.status}
                        color={getStatusColor(demand.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{demand.created_date}</TableCell>
                    <TableCell>{demand.assigned_to}</TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        variant="outlined"
                        startIcon={<Assignment />}
                        onClick={() => console.log('View demand:', demand.id)}
                      >
                        Ver
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Container>
    </>
  );
}