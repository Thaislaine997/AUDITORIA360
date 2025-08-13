import React from 'react';
import { TicketsList } from '../components/TicketsList';
import { NotificacoesList } from '../components/NotificacoesList';
import { EmpresasList, SindicatosList, CCTsList, TarefasList } from '../components/PortalDemandasDomainLists';
import { AuditoriasList, RelatoriosList, UploadsList } from '../components/PortalDemandasAuditoriaLists';
import IAChatAssistant from '../components/IAChatAssistant';
import { Box, Typography, Divider } from '@mui/material';
import { Notifications, ConfirmationNumber, Business, Groups, Gavel, TaskAlt, Assignment, Assessment, CloudUpload } from '@mui/icons-material';

const PortalDemandasDashboard: React.FC = () => {
  return (
    <Box maxWidth={1100} mx="auto" p={3} position="relative">
      <Typography variant="h4" fontWeight={800} mb={3} sx={{ letterSpacing: 1 }}>Portal Demandas <span style={{ fontWeight: 400, fontSize: 22, color: '#888' }}>Dashboard</span></Typography>

      <Box mb={4}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <Notifications color="primary" />
          <Typography variant="h5" fontWeight={700}>Notificações</Typography>
        </Box>
        <NotificacoesList />
      </Box>
      <Divider sx={{ my: 3 }} />

      <Box mb={4}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <ConfirmationNumber color="primary" />
          <Typography variant="h5" fontWeight={700}>Tickets</Typography>
        </Box>
        <TicketsList />
      </Box>
      <Divider sx={{ my: 3 }} />

      <Box mb={4}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <Business color="primary" />
          <Typography variant="h5" fontWeight={700}>Empresas</Typography>
        </Box>
        <EmpresasList />
      </Box>
      <Divider sx={{ my: 3 }} />

      <Box mb={4}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <Groups color="primary" />
          <Typography variant="h5" fontWeight={700}>Sindicatos</Typography>
        </Box>
        <SindicatosList />
      </Box>
      <Divider sx={{ my: 3 }} />

      <Box mb={4}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <Gavel color="primary" />
          <Typography variant="h5" fontWeight={700}>CCTs</Typography>
        </Box>
        <CCTsList />
      </Box>
      <Divider sx={{ my: 3 }} />

      <Box mb={4}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <TaskAlt color="primary" />
          <Typography variant="h5" fontWeight={700}>Tarefas</Typography>
        </Box>
        <TarefasList />
      </Box>
      <Divider sx={{ my: 3 }} />

      <Box mb={4}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <Assignment color="primary" />
          <Typography variant="h5" fontWeight={700}>Auditorias</Typography>
        </Box>
        <AuditoriasList />
      </Box>
      <Divider sx={{ my: 3 }} />

      <Box mb={4}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <Assessment color="primary" />
          <Typography variant="h5" fontWeight={700}>Relatórios</Typography>
        </Box>
        <RelatoriosList />
      </Box>
      <Divider sx={{ my: 3 }} />

      <Box mb={4}>
        <Box display="flex" alignItems="center" gap={1} mb={1}>
          <CloudUpload color="primary" />
          <Typography variant="h5" fontWeight={700}>Uploads</Typography>
        </Box>
        <UploadsList />
      </Box>
      <IAChatAssistant />
    </Box>
  );
};

export default PortalDemandasDashboard;
