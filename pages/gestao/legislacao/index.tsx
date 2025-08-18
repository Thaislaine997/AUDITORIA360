// Migrated from src/frontend/pages/gestao/GestaoLegislacaoPage.tsx
import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Chip,
  Button,
  IconButton,
} from "@mui/material";
import {
  Add as AddIcon,
  Edit as EditIcon,
  Visibility as ViewIcon,
} from "@mui/icons-material";

interface Legislacao {
  id: number;
  titulo: string;
  tipo: string;
  status: 'ATIVA' | 'REVOGADA' | 'PENDENTE';
  data_inicio: string;
  data_fim?: string;
}

const GestaoLegislacaoPage: React.FC = () => {
  const [legislacoes] = useState<Legislacao[]>([
    {
      id: 1,
      titulo: "CCT Comerciários 2024-2025",
      tipo: "Convenção Coletiva",
      status: "ATIVA",
      data_inicio: "2024-01-01",
      data_fim: "2024-12-31"
    },
    {
      id: 2,
      titulo: "Lei 13.467/2017 - Reforma Trabalhista",
      tipo: "Lei Federal",
      status: "ATIVA",
      data_inicio: "2017-11-11"
    },
    {
      id: 3,
      titulo: "CCT Comerciários 2023-2024",
      tipo: "Convenção Coletiva",
      status: "REVOGADA",
      data_inicio: "2023-01-01",
      data_fim: "2023-12-31"
    }
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'ATIVA': return 'success';
      case 'REVOGADA': return 'default';
      case 'PENDENTE': return 'warning';
      default: return 'default';
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" gutterBottom>
            Gestão de Legislação
          </Typography>
          <Button variant="contained" startIcon={<AddIcon />}>
            Nova Legislação
          </Button>
        </Box>

        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Título</TableCell>
                  <TableCell>Tipo</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Vigência</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {legislacoes.map((item) => (
                  <TableRow key={item.id}>
                    <TableCell>
                      <Typography variant="body2" fontWeight="medium">
                        {item.titulo}
                      </Typography>
                    </TableCell>
                    <TableCell>{item.tipo}</TableCell>
                    <TableCell>
                      <Chip 
                        label={item.status} 
                        color={getStatusColor(item.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {new Date(item.data_inicio).toLocaleDateString('pt-BR')}
                        {item.data_fim && ` - ${new Date(item.data_fim).toLocaleDateString('pt-BR')}`}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <IconButton size="small">
                        <ViewIcon />
                      </IconButton>
                      <IconButton size="small">
                        <EditIcon />
                      </IconButton>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </Paper>
      </Box>
    </Container>
  );
};

export default GestaoLegislacaoPage;