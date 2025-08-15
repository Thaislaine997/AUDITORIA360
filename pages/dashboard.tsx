import React, { useState, useEffect } from "react";
import Head from 'next/head';
import { useRouter } from 'next/router';
import { Container, Typography, Paper, Box, Alert, Button } from "@mui/material";
import { authHelpers } from '../lib/supabaseClient';

interface User {
  id: string;
  email?: string;
  user_metadata?: {
    full_name?: string;
  };
}

export default function Dashboard() {
  const [user, setUser] = useState<User | null>(null);
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
        setUser(currentUser as User);
      } catch (error) {
        console.error('Error checking user:', error);
        router.push('/login');
      } finally {
        setLoading(false);
      }
    };

    checkUser();
  }, [router]);

  if (loading) {
    return (
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography>Loading...</Typography>
      </Container>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <>
      <Head>
        <title>Dashboard - AUDITORIA360</title>
        <meta name="description" content="Dashboard do AUDITORIA360" />
        <meta name="robots" content="noindex" />
      </Head>
      
      <Container maxWidth="lg" sx={{ py: 4 }}>
        <Typography variant="h3" component="h1" gutterBottom>
          Dashboard AUDITORIA360
        </Typography>
        
        <Alert severity="info" sx={{ mb: 4 }}>
          Bem-vindo(a), {user.user_metadata?.full_name || user.email}!
        </Alert>
        
        <Box sx={{ display: 'grid', gap: 3, gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))' }}>
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Documentos
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Gerencie documentos, certificações e uploads.
            </Typography>
            <Button variant="outlined" href="/legacy/documents" fullWidth>
              Acessar Documentos
            </Button>
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Portal de Demandas
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Gerencie tickets, solicitações e demandas dos clientes.
            </Typography>
            <Button variant="outlined" href="/legacy/portal-demandas" fullWidth>
              Acessar Portal
            </Button>
          </Paper>
          
          <Paper sx={{ p: 3 }}>
            <Typography variant="h6" gutterBottom>
              Relatórios
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
              Acesse relatórios de auditoria e análises detalhadas.
            </Typography>
            <Button variant="outlined" href="/legacy/relatorios" fullWidth>
              Ver Relatórios
            </Button>
          </Paper>
        </Box>
      </Container>
    </>
  );
}