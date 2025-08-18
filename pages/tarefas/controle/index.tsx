// Migrated from src/frontend/pages/tarefas/TarefasControlePage.tsx
import React, { useState } from "react";
import {
  Container,
  Typography,
  Box,
  Paper,
  Button,
  Chip,
  IconButton,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
} from "@mui/material";
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  PlayArrow as StartIcon,
  Pause as PauseIcon,
} from "@mui/icons-material";

interface Tarefa {
  id: number;
  titulo: string;
  descricao: string;
  status: 'PENDENTE' | 'EM_ANDAMENTO' | 'CONCLUIDA' | 'CANCELADA';
  prioridade: 'BAIXA' | 'MEDIA' | 'ALTA';
  responsavel: string;
  data_criacao: string;
  data_vencimento: string;
}

const TarefasControlePage: React.FC = () => {
  const [tarefas] = useState<Tarefa[]>([
    {
      id: 1,
      titulo: "Auditoria Empresa ABC",
      descricao: "Realizar auditoria mensal da folha de pagamento",
      status: "EM_ANDAMENTO",
      prioridade: "ALTA",
      responsavel: "João Silva",
      data_criacao: "2024-01-15",
      data_vencimento: "2024-01-25"
    },
    {
      id: 2,
      titulo: "Análise CCT Comerciários",
      descricao: "Revisar nova convenção coletiva",
      status: "PENDENTE",
      prioridade: "MEDIA",
      responsavel: "Maria Santos",
      data_criacao: "2024-01-16",
      data_vencimento: "2024-01-30"
    },
    {
      id: 3,
      titulo: "Relatório Divergências Q4",
      descricao: "Compilar relatório trimestral de divergências",
      status: "CONCLUIDA",
      prioridade: "BAIXA",
      responsavel: "Pedro Costa",
      data_criacao: "2024-01-10",
      data_vencimento: "2024-01-20"
    }
  ]);

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'PENDENTE': return 'warning';
      case 'EM_ANDAMENTO': return 'info';
      case 'CONCLUIDA': return 'success';
      case 'CANCELADA': return 'error';
      default: return 'default';
    }
  };

  const getPrioridadeColor = (prioridade: string) => {
    switch (prioridade) {
      case 'ALTA': return 'error';
      case 'MEDIA': return 'warning';
      case 'BAIXA': return 'info';
      default: return 'default';
    }
  };

  return (
    <Container maxWidth="lg">
      <Box sx={{ py: 4 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 4 }}>
          <Typography variant="h4" gutterBottom>
            Controle de Tarefas
          </Typography>
          <Button variant="contained" startIcon={<AddIcon />}>
            Nova Tarefa
          </Button>
        </Box>

        <Paper>
          <TableContainer>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Tarefa</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Prioridade</TableCell>
                  <TableCell>Responsável</TableCell>
                  <TableCell>Vencimento</TableCell>
                  <TableCell>Ações</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {tarefas.map((tarefa) => (
                  <TableRow key={tarefa.id}>
                    <TableCell>
                      <Typography variant="body2" fontWeight="medium">
                        {tarefa.titulo}
                      </Typography>
                      <Typography variant="caption" color="text.secondary">
                        {tarefa.descricao}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={tarefa.status.replace('_', ' ')} 
                        color={getStatusColor(tarefa.status) as any}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      <Chip 
                        label={tarefa.prioridade} 
                        color={getPrioridadeColor(tarefa.prioridade) as any}
                        size="small"
                        variant="outlined"
                      />
                    </TableCell>
                    <TableCell>{tarefa.responsavel}</TableCell>
                    <TableCell>
                      <Typography variant="body2">
                        {new Date(tarefa.data_vencimento).toLocaleDateString('pt-BR')}
                      </Typography>
                    </TableCell>
                    <TableCell>
                      <IconButton size="small">
                        {tarefa.status === 'EM_ANDAMENTO' ? <PauseIcon /> : <StartIcon />}
                      </IconButton>
                      <IconButton size="small">
                        <EditIcon />
                      </IconButton>
                      <IconButton size="small">
                        <DeleteIcon />
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

export default TarefasControlePage;