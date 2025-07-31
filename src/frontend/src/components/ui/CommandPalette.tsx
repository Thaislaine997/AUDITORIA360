import React, { useState, useEffect } from 'react';
import {
  Dialog,
  DialogContent,
  TextField,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  ListItemButton,
  Typography,
  Box,
  Chip,
  InputAdornment,
  Divider,
} from '@mui/material';
import {
  Search as SearchIcon,
  Dashboard as DashboardIcon,
  Payment as PaymentIcon,
  Description as DocumentIcon,
  Gavel as GavelIcon,
  Assessment as AuditIcon,
  Chat as ChatIcon,
  Assignment as ReportIcon,
  Person as PersonIcon,
  Settings as SettingsIcon,
  Keyboard,
} from '@mui/icons-material';
import { useNavigate } from 'react-router-dom';

interface Command {
  id: string;
  title: string;
  description?: string;
  category: 'navigation' | 'action' | 'settings';
  icon: React.ReactNode;
  action: (navigate?: (path: string) => void) => void;
  shortcut?: string;
  keywords: string[];
}

interface CommandPaletteProps {
  open: boolean;
  onClose: () => void;
}

const CommandPalette: React.FC<CommandPaletteProps> = ({ open, onClose }) => {
  let navigate: ((path: string) => void) | undefined;
  
  try {
    navigate = useNavigate();
  } catch (error) {
    // useNavigate is not available outside of Router context (e.g., in tests)
    navigate = undefined;
  }
  
  const [query, setQuery] = useState('');
  const [filteredCommands, setFilteredCommands] = useState<Command[]>([]);
  const [selectedIndex, setSelectedIndex] = useState(0);

  const commands: Command[] = [
    {
      id: 'nav_dashboard',
      title: 'Dashboard',
      description: 'Ir para a página principal',
      category: 'navigation',
      icon: <DashboardIcon />,
      action: (nav) => nav && nav('/dashboard'),
      shortcut: 'Ctrl+D',
      keywords: ['dashboard', 'inicio', 'principal', 'home'],
    },
    {
      id: 'nav_payroll',
      title: 'Folha de Pagamento',
      description: 'Gerenciar folha de pagamento',
      category: 'navigation',
      icon: <PaymentIcon />,
      action: (nav) => nav && nav('/payroll'),
      shortcut: 'Ctrl+P',
      keywords: ['folha', 'pagamento', 'salario', 'payroll'],
    },
    {
      id: 'nav_documents',
      title: 'Documentos',
      description: 'Visualizar e gerenciar documentos',
      category: 'navigation',
      icon: <DocumentIcon />,
      action: (nav) => nav && nav('/documents'),
      keywords: ['documentos', 'arquivos', 'documents'],
    },
    {
      id: 'nav_cct',
      title: 'CCT',
      description: 'Convenção Coletiva de Trabalho',
      category: 'navigation',
      icon: <GavelIcon />,
      action: (nav) => nav && nav('/cct'),
      keywords: ['cct', 'convencao', 'trabalho'],
    },
    {
      id: 'nav_audit',
      title: 'Auditoria',
      description: 'Ferramentas de auditoria',
      category: 'navigation',
      icon: <AuditIcon />,
      action: (nav) => nav && nav('/audit'),
      keywords: ['auditoria', 'audit', 'compliance'],
    },
    {
      id: 'nav_chatbot',
      title: 'Chatbot',
      description: 'Assistente virtual',
      category: 'navigation',
      icon: <ChatIcon />,
      action: (nav) => nav && nav('/chatbot'),
      keywords: ['chatbot', 'chat', 'assistente', 'ai'],
    },
    {
      id: 'nav_reports',
      title: 'Relatórios',
      description: 'Modelos de relatório',
      category: 'navigation',
      icon: <ReportIcon />,
      action: (nav) => nav && nav('/reports/templates'),
      keywords: ['relatorios', 'reports', 'modelos'],
    },
    {
      id: 'action_profile',
      title: 'Meu Perfil',
      description: 'Visualizar perfil do usuário',
      category: 'settings',
      icon: <PersonIcon />,
      action: (nav) => nav && nav('/profile'),
      keywords: ['perfil', 'profile', 'usuario'],
    },
    {
      id: 'action_settings',
      title: 'Configurações',
      description: 'Configurações do sistema',
      category: 'settings',
      icon: <SettingsIcon />,
      action: (nav) => nav && nav('/settings'),
      keywords: ['configuracoes', 'settings', 'opcoes'],
    },
  ];

  useEffect(() => {
    if (!query.trim()) {
      setFilteredCommands(commands);
    } else {
      const filtered = commands.filter(command =>
        command.title.toLowerCase().includes(query.toLowerCase()) ||
        command.description?.toLowerCase().includes(query.toLowerCase()) ||
        command.keywords.some(keyword => 
          keyword.toLowerCase().includes(query.toLowerCase())
        )
      );
      setFilteredCommands(filtered);
    }
    setSelectedIndex(0);
  }, [query]);

  useEffect(() => {
    const handleKeyDown = (event: KeyboardEvent) => {
      if (!open) return;

      switch (event.key) {
        case 'ArrowDown':
          event.preventDefault();
          setSelectedIndex(prev => 
            prev < filteredCommands.length - 1 ? prev + 1 : 0
          );
          break;
        case 'ArrowUp':
          event.preventDefault();
          setSelectedIndex(prev => 
            prev > 0 ? prev - 1 : filteredCommands.length - 1
          );
          break;
        case 'Enter':
          event.preventDefault();
          if (filteredCommands[selectedIndex]) {
            filteredCommands[selectedIndex].action(navigate);
            onClose();
            setQuery('');
          }
          break;
        case 'Escape':
          onClose();
          setQuery('');
          break;
      }
    };

    document.addEventListener('keydown', handleKeyDown);
    return () => document.removeEventListener('keydown', handleKeyDown);
  }, [open, filteredCommands, selectedIndex, onClose]);

  const handleCommandClick = (command: Command) => {
    command.action(navigate);
    onClose();
    setQuery('');
  };

  const getCategoryColor = (category: Command['category']) => {
    switch (category) {
      case 'navigation':
        return 'primary';
      case 'action':
        return 'secondary';
      case 'settings':
        return 'default';
      default:
        return 'default';
    }
  };

  const getCategoryLabel = (category: Command['category']) => {
    switch (category) {
      case 'navigation':
        return 'Navegação';
      case 'action':
        return 'Ação';
      case 'settings':
        return 'Configurações';
      default:
        return '';
    }
  };

  return (
    <Dialog
      open={open}
      onClose={onClose}
      maxWidth="md"
      fullWidth
      PaperProps={{
        sx: {
          borderRadius: 2,
          minHeight: '50vh',
          maxHeight: '80vh',
        },
      }}
    >
      <DialogContent sx={{ p: 0 }}>
        <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
          <TextField
            fullWidth
            placeholder="Digite para buscar comandos..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            autoFocus
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <SearchIcon />
                </InputAdornment>
              ),
              endAdornment: (
                <InputAdornment position="end">
                  <Box sx={{ display: 'flex', gap: 0.5 }}>
                    <Chip
                      size="small"
                      icon={<Keyboard />}
                      label="Ctrl+K"
                      variant="outlined"
                    />
                  </Box>
                </InputAdornment>
              ),
            }}
            sx={{
              '& .MuiOutlinedInput-root': {
                '& fieldset': {
                  border: 'none',
                },
              },
            }}
          />
        </Box>

        {filteredCommands.length === 0 ? (
          <Box sx={{ p: 4, textAlign: 'center' }}>
            <Typography variant="body2" color="text.secondary">
              Nenhum comando encontrado para "{query}"
            </Typography>
          </Box>
        ) : (
          <List sx={{ maxHeight: '50vh', overflow: 'auto', p: 1 }}>
            {filteredCommands.map((command, index) => (
              <ListItem key={command.id} disablePadding>
                <ListItemButton
                  selected={index === selectedIndex}
                  onClick={() => handleCommandClick(command)}
                  sx={{
                    borderRadius: 1,
                    mb: 0.5,
                    '&.Mui-selected': {
                      backgroundColor: 'primary.main',
                      color: 'primary.contrastText',
                      '&:hover': {
                        backgroundColor: 'primary.dark',
                      },
                    },
                  }}
                >
                  <ListItemIcon
                    sx={{
                      color: index === selectedIndex ? 'inherit' : 'text.secondary',
                    }}
                  >
                    {command.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={
                      <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                        <Typography variant="body1">{command.title}</Typography>
                        <Chip
                          size="small"
                          label={getCategoryLabel(command.category)}
                          color={getCategoryColor(command.category)}
                          variant="outlined"
                          sx={{ height: 20, fontSize: '0.7rem' }}
                        />
                      </Box>
                    }
                    secondary={command.description}
                    secondaryTypographyProps={{
                      sx: {
                        color: index === selectedIndex ? 'inherit' : 'text.secondary',
                        opacity: index === selectedIndex ? 0.8 : 1,
                      },
                    }}
                  />
                  {command.shortcut && (
                    <Box sx={{ ml: 2 }}>
                      <Chip
                        size="small"
                        label={command.shortcut}
                        variant="outlined"
                        sx={{ 
                          height: 24, 
                          fontSize: '0.7rem',
                          borderColor: index === selectedIndex ? 'currentColor' : 'text.secondary',
                          color: index === selectedIndex ? 'inherit' : 'text.secondary',
                        }}
                      />
                    </Box>
                  )}
                </ListItemButton>
              </ListItem>
            ))}
          </List>
        )}

        <Divider />
        <Box sx={{ p: 1, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <Typography variant="caption" color="text.secondary">
            Use ↑↓ para navegar, Enter para selecionar, Esc para fechar
          </Typography>
          <Typography variant="caption" color="text.secondary">
            {filteredCommands.length} comando(s) encontrado(s)
          </Typography>
        </Box>
      </DialogContent>
    </Dialog>
  );
};

export default CommandPalette;