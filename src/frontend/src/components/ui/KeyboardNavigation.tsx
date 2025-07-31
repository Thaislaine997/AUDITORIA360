import React, { useEffect, useCallback, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Tooltip,
  Snackbar,
  Alert,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Button,
  Box,
  Typography,
  List,
  ListItem,
  ListItemText,
  Chip,
  Accordion,
  AccordionSummary,
  AccordionDetails,
  TextField,
  ListItemButton,
  ListItemIcon,
  InputAdornment,
} from '@mui/material';
import {
  Keyboard,
  ExpandMore,
  Search,
  Dashboard,
  Business,
  People,
  Assignment,
  Psychology,
  AccountBalance,
  Assessment,
  Settings,
  AccountCircle,
  Description,
} from '@mui/icons-material';

interface KeyboardShortcut {
  key: string;
  description: string;
  action: () => void;
  section: string;
}

interface CommandPaletteItem {
  id: string;
  label: string;
  description?: string;
  path: string;
  icon: React.ReactNode;
  keywords: string[];
}

interface KeyboardNavigationProps {
  children: React.ReactNode;
}

const KeyboardNavigation: React.FC<KeyboardNavigationProps> = ({ children }) => {
  const navigate = useNavigate();
  const [shortcutTooltip, setShortcutTooltip] = useState<string>('');
  const [showShortcutHelp, setShowShortcutHelp] = useState(false);
  const [showCommandPalette, setShowCommandPalette] = useState(false);
  const [commandSearchQuery, setCommandSearchQuery] = useState('');

  // Command palette items for quick navigation
  const commandPaletteItems: CommandPaletteItem[] = [
    {
      id: 'dashboard',
      label: 'Dashboard',
      description: 'Visão geral do sistema',
      path: '/dashboard',
      icon: <Dashboard />,
      keywords: ['dashboard', 'inicio', 'home', 'principal'],
    },
    {
      id: 'demandas',
      label: 'Portal de Demandas',
      description: 'Gerencie solicitações e tickets',
      path: '/demandas',
      icon: <Assignment />,
      keywords: ['demandas', 'tickets', 'solicitações', 'portal'],
    },
    {
      id: 'consultor-riscos',
      label: 'Consultor de Riscos',
      description: 'IA para análise de riscos',
      path: '/consultor-riscos',
      icon: <Psychology />,
      keywords: ['riscos', 'consultor', 'ia', 'análise'],
    },
    {
      id: 'gestao-contabilidades',
      label: 'Gestão de Contabilidades',
      description: 'Gerenciar contabilidades',
      path: '/gestao/contabilidades',
      icon: <AccountBalance />,
      keywords: ['contabilidades', 'gestão', 'contábil'],
    },
    {
      id: 'gestao-clientes',
      label: 'Gestão de Clientes',
      description: 'Gerenciar clientes',
      path: '/gestao/clientes',
      icon: <Business />,
      keywords: ['clientes', 'gestão', 'empresas'],
    },
    {
      id: 'gestao-usuarios',
      label: 'Gerenciamento de Usuários',
      description: 'Gerenciar usuários do sistema',
      path: '/gestao/usuarios',
      icon: <People />,
      keywords: ['usuários', 'gestão', 'colaboradores', 'equipe'],
    },
    {
      id: 'relatorios-avancados',
      label: 'Relatórios Avançados',
      description: 'Relatórios e análises',
      path: '/relatorios/avancados',
      icon: <Assessment />,
      keywords: ['relatórios', 'análises', 'dados', 'gráficos'],
    },
    {
      id: 'minha-conta',
      label: 'Minha Conta',
      description: 'Configurações pessoais',
      path: '/configuracoes/minha-conta',
      icon: <AccountCircle />,
      keywords: ['conta', 'perfil', 'configurações', 'pessoal'],
    },
    {
      id: 'templates',
      label: 'Templates',
      description: 'Gerenciar templates',
      path: '/configuracoes/templates',
      icon: <Description />,
      keywords: ['templates', 'modelos', 'configurações'],
    },
  ];

  // Filter command palette items based on search query
  const filteredCommands = commandPaletteItems.filter(item => {
    if (!commandSearchQuery) return true;
    
    const query = commandSearchQuery.toLowerCase();
    return (
      item.label.toLowerCase().includes(query) ||
      item.description?.toLowerCase().includes(query) ||
      item.keywords.some(keyword => keyword.toLowerCase().includes(query))
    );
  });

  const shortcuts: KeyboardShortcut[] = [
    // Command palette
    {
      key: 'Ctrl+k',
      description: 'Abrir paleta de comandos',
      action: () => setShowCommandPalette(true),
      section: 'Sistema',
    },
    
    // Navigation shortcuts
    {
      key: 'g+d',
      description: 'Ir para Dashboard',
      action: () => navigate('/dashboard'),
      section: 'Navegação',
    },
    {
      key: 'g+c',
      description: 'Ir para Clientes',
      action: () => navigate('/gestao/clientes'),
      section: 'Navegação',
    },
    {
      key: 'g+u',
      description: 'Ir para Usuários',
      action: () => navigate('/gestao/usuarios'),
      section: 'Navegação',
    },
    {
      key: 'g+r',
      description: 'Ir para Relatórios',
      action: () => navigate('/relatorios/avancados'),
      section: 'Navegação',
    },
    {
      key: 'g+s',
      description: 'Ir para Configurações',
      action: () => navigate('/configuracoes/minha-conta'),
      section: 'Navegação',
    },

    // Action shortcuts
    {
      key: 'c',
      description: 'Criar novo (Cliente/Documento/etc)',
      action: () => {
        const currentPath = window.location.pathname;
        if (currentPath.includes('/clients')) {
          navigate('/clients/new');
        } else if (currentPath.includes('/documents')) {
          navigate('/documents/upload');
        } else if (currentPath.includes('/reports')) {
          navigate('/reports/new');
        } else {
          // Default to new client
          navigate('/clients/new');
        }
      },
      section: 'Ações',
    },
    {
      key: 's',
      description: 'Salvar (quando em formulário)',
      action: () => {
        const saveButton = document.querySelector('[data-testid="save-button"], button[type="submit"]') as HTMLButtonElement;
        if (saveButton && !saveButton.disabled) {
          saveButton.click();
        }
      },
      section: 'Ações',
    },
    {
      key: 'e',
      description: 'Editar item selecionado',
      action: () => {
        const editButton = document.querySelector('[data-action="edit"], [aria-label*="edit" i]') as HTMLButtonElement;
        if (editButton) {
          editButton.click();
        }
      },
      section: 'Ações',
    },
    {
      key: 'Delete',
      description: 'Excluir item selecionado',
      action: () => {
        const deleteButton = document.querySelector('[data-action="delete"], [aria-label*="delete" i], [aria-label*="excluir" i]') as HTMLButtonElement;
        if (deleteButton) {
          deleteButton.click();
        }
      },
      section: 'Ações',
    },

    // Search and filter
    {
      key: '/',
      description: 'Focar na busca',
      action: () => {
        const searchInput = document.querySelector('input[type="search"], input[placeholder*="buscar" i], input[placeholder*="pesquisar" i]') as HTMLInputElement;
        if (searchInput) {
          searchInput.focus();
          searchInput.select();
        }
      },
      section: 'Busca',
    },
    {
      key: 'f',
      description: 'Abrir filtros',
      action: () => {
        const filterButton = document.querySelector('[data-action="filter"], [aria-label*="filtro" i]') as HTMLButtonElement;
        if (filterButton) {
          filterButton.click();
        }
      },
      section: 'Busca',
    },

    // System shortcuts
    {
      key: '?',
      description: 'Mostrar atalhos do teclado',
      action: () => setShowShortcutHelp(true),
      section: 'Sistema',
    },
    {
      key: 'Escape',
      description: 'Fechar modais/cancelar',
      action: () => {
        const closeButton = document.querySelector('[data-action="close"], [aria-label*="close" i], [aria-label*="fechar" i]') as HTMLButtonElement;
        if (closeButton) {
          closeButton.click();
        }
      },
      section: 'Sistema',
    },

    // Navigation within lists/tables
    {
      key: 'ArrowDown',
      description: 'Próximo item na lista',
      action: () => {
        const currentSelected = document.querySelector('[data-selected="true"], .selected, [aria-selected="true"]');
        const nextItem = currentSelected?.nextElementSibling as HTMLElement;
        if (nextItem) {
          nextItem.click();
          nextItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      },
      section: 'Lista',
    },
    {
      key: 'ArrowUp',
      description: 'Item anterior na lista',
      action: () => {
        const currentSelected = document.querySelector('[data-selected="true"], .selected, [aria-selected="true"]');
        const prevItem = currentSelected?.previousElementSibling as HTMLElement;
        if (prevItem) {
          prevItem.click();
          prevItem.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
        }
      },
      section: 'Lista',
    },
    {
      key: 'Enter',
      description: 'Abrir/selecionar item',
      action: () => {
        const selectedItem = document.querySelector('[data-selected="true"], .selected, [aria-selected="true"]') as HTMLElement;
        if (selectedItem) {
          selectedItem.click();
        }
      },
      section: 'Lista',
    },

    // Tab navigation
    {
      key: 'Tab',
      description: 'Próximo elemento focável',
      action: () => {
        // Tab navigation is handled by the browser
      },
      section: 'Navegação por Abas',
    },
    {
      key: 'Shift+Tab',
      description: 'Elemento focável anterior',
      action: () => {
        // Shift+Tab navigation is handled by the browser
      },
      section: 'Navegação por Abas',
    },
  ];

  const handleKeyDown = useCallback((event: KeyboardEvent) => {
    // Don't handle shortcuts when typing in inputs
    if (
      event.target instanceof HTMLInputElement ||
      event.target instanceof HTMLTextAreaElement ||
      event.target instanceof HTMLSelectElement ||
      (event.target as Element)?.getAttribute('contenteditable') === 'true'
    ) {
      // Exception: Allow certain shortcuts even in inputs
      if (event.key === 'Escape') {
        (event.target as HTMLElement).blur();
        return;
      }
      return;
    }

    const key = event.key;
    const ctrlKey = event.ctrlKey || event.metaKey;
    const shiftKey = event.shiftKey;
    const altKey = event.altKey;

    // Build key combination string
    let keyCombo = '';
    if (ctrlKey) keyCombo += 'Ctrl+';
    if (altKey) keyCombo += 'Alt+';
    if (shiftKey) keyCombo += 'Shift+';
    keyCombo += key;

    // Handle Ctrl+K for command palette
    if ((ctrlKey || event.metaKey) && key === 'k') {
      event.preventDefault();
      setShowCommandPalette(true);
      return;
    }

    // Handle sequential shortcuts (like g+d)
    if (key === 'g') {
      event.preventDefault();
      setShortcutTooltip('g → Pressione a próxima tecla para navegar');
      
      const handleSecondKey = (secondEvent: KeyboardEvent) => {
        secondEvent.preventDefault();
        const secondKey = secondEvent.key;
        const fullShortcut = `g+${secondKey}`;
        
        const shortcut = shortcuts.find(s => s.key === fullShortcut);
        if (shortcut) {
          shortcut.action();
          setShortcutTooltip(`Navegando: ${shortcut.description}`);
          setTimeout(() => setShortcutTooltip(''), 2000);
        } else {
          setShortcutTooltip('Atalho não encontrado');
          setTimeout(() => setShortcutTooltip(''), 1000);
        }
        
        document.removeEventListener('keydown', handleSecondKey);
      };
      
      document.addEventListener('keydown', handleSecondKey);
      setTimeout(() => {
        document.removeEventListener('keydown', handleSecondKey);
        setShortcutTooltip('');
      }, 3000);
      
      return;
    }

    // Handle direct shortcuts
    const shortcut = shortcuts.find(s => s.key === key || s.key === keyCombo);
    if (shortcut) {
      event.preventDefault();
      shortcut.action();
      
      if (shortcut.key !== '?') { // Don't show tooltip for help shortcut
        setShortcutTooltip(shortcut.description);
        setTimeout(() => setShortcutTooltip(''), 1500);
      }
    }
  }, [navigate, shortcuts]);

  useEffect(() => {
    document.addEventListener('keydown', handleKeyDown);
    return () => {
      document.removeEventListener('keydown', handleKeyDown);
    };
  }, [handleKeyDown]);

  // Group shortcuts by section
  const groupedShortcuts = shortcuts.reduce((acc, shortcut) => {
    if (!acc[shortcut.section]) {
      acc[shortcut.section] = [];
    }
    acc[shortcut.section].push(shortcut);
    return acc;
  }, {} as Record<string, KeyboardShortcut[]>);

  return (
    <>
      {children}
      
      {/* Shortcut Tooltip */}
      <Snackbar
        open={!!shortcutTooltip}
        message={shortcutTooltip}
        anchorOrigin={{ vertical: 'top', horizontal: 'center' }}
        autoHideDuration={null}
        sx={{ 
          '& .MuiSnackbarContent-root': {
            backgroundColor: 'primary.main',
            color: 'white',
            fontWeight: 'bold',
          }
        }}
      />

      {/* Command Palette Dialog */}
      <Dialog
        open={showCommandPalette}
        onClose={() => {
          setShowCommandPalette(false);
          setCommandSearchQuery('');
        }}
        maxWidth="sm"
        fullWidth
        PaperProps={{
          sx: {
            position: 'absolute',
            top: '20%',
            m: 0,
          }
        }}
      >
        <DialogContent sx={{ p: 0 }}>
          <TextField
            autoFocus
            fullWidth
            placeholder="Digite para navegar ou procurar..."
            value={commandSearchQuery}
            onChange={(e) => setCommandSearchQuery(e.target.value)}
            variant="outlined"
            InputProps={{
              startAdornment: (
                <InputAdornment position="start">
                  <Search />
                </InputAdornment>
              ),
            }}
            sx={{
              '& .MuiOutlinedInput-root': {
                borderRadius: 0,
                borderBottom: '1px solid',
                borderBottomColor: 'divider',
                '& fieldset': {
                  border: 'none',
                },
              },
            }}
            onKeyDown={(e) => {
              if (e.key === 'ArrowDown') {
                e.preventDefault();
                const firstItem = document.querySelector('[data-command-item="0"]') as HTMLElement;
                firstItem?.focus();
              } else if (e.key === 'Escape') {
                setShowCommandPalette(false);
                setCommandSearchQuery('');
              }
            }}
          />
          
          <List sx={{ maxHeight: 400, overflow: 'auto', p: 1 }}>
            {filteredCommands.length === 0 ? (
              <ListItem>
                <ListItemText 
                  primary="Nenhum resultado encontrado"
                  secondary="Tente uma busca diferente"
                  sx={{ textAlign: 'center' }}
                />
              </ListItem>
            ) : (
              filteredCommands.map((item, index) => (
                <ListItemButton
                  key={item.id}
                  data-command-item={index}
                  onClick={() => {
                    navigate(item.path);
                    setShowCommandPalette(false);
                    setCommandSearchQuery('');
                  }}
                  onKeyDown={(e) => {
                    if (e.key === 'ArrowDown') {
                      e.preventDefault();
                      const nextItem = document.querySelector(`[data-command-item="${index + 1}"]`) as HTMLElement;
                      nextItem?.focus();
                    } else if (e.key === 'ArrowUp') {
                      e.preventDefault();
                      if (index === 0) {
                        const searchInput = document.querySelector('input[placeholder*="Digite para navegar"]') as HTMLElement;
                        searchInput?.focus();
                      } else {
                        const prevItem = document.querySelector(`[data-command-item="${index - 1}"]`) as HTMLElement;
                        prevItem?.focus();
                      }
                    } else if (e.key === 'Enter') {
                      navigate(item.path);
                      setShowCommandPalette(false);
                      setCommandSearchQuery('');
                    } else if (e.key === 'Escape') {
                      setShowCommandPalette(false);
                      setCommandSearchQuery('');
                    }
                  }}
                  sx={{
                    borderRadius: 1,
                    mb: 0.5,
                    '&:hover, &:focus': {
                      bgcolor: 'primary.main',
                      color: 'white',
                      '& .MuiListItemIcon-root': {
                        color: 'white',
                      },
                    },
                  }}
                >
                  <ListItemIcon>
                    {item.icon}
                  </ListItemIcon>
                  <ListItemText
                    primary={item.label}
                    secondary={item.description}
                  />
                </ListItemButton>
              ))
            )}
          </List>
        </DialogContent>
      </Dialog>

      {/* Keyboard Shortcuts Help Dialog */}
      <Dialog
        open={showShortcutHelp}
        onClose={() => setShowShortcutHelp(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Keyboard sx={{ mr: 1 }} />
            Atalhos do Teclado
          </Box>
        </DialogTitle>
        <DialogContent>
          <Alert severity="info" sx={{ mb: 3 }}>
            Use os atalhos abaixo para navegar mais rapidamente pelo sistema. 
            Os atalhos estão organizados por categoria para facilitar o aprendizado.
          </Alert>

          {Object.entries(groupedShortcuts).map(([section, sectionShortcuts]) => (
            <Accordion key={section} defaultExpanded={section === 'Navegação'}>
              <AccordionSummary expandIcon={<ExpandMore />}>
                <Typography variant="h6">{section}</Typography>
              </AccordionSummary>
              <AccordionDetails>
                <List>
                  {sectionShortcuts.map((shortcut, index) => (
                    <ListItem key={index}>
                      <ListItemText
                        primary={
                          <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                            <Typography variant="body1">
                              {shortcut.description}
                            </Typography>
                            <Chip
                              label={shortcut.key}
                              variant="outlined"
                              size="small"
                              sx={{ 
                                fontFamily: 'monospace',
                                fontWeight: 'bold'
                              }}
                            />
                          </Box>
                        }
                      />
                    </ListItem>
                  ))}
                </List>
              </AccordionDetails>
            </Accordion>
          ))}

          <Box sx={{ mt: 3, p: 2, bgcolor: 'background.paper', borderRadius: 1, border: 1, borderColor: 'divider' }}>
            <Typography variant="body2" color="text.secondary">
              <strong>Dica:</strong> Pressione <Chip label="?" size="small" sx={{ mx: 0.5 }} /> a qualquer momento para ver esta ajuda.
              Os atalhos que começam com <Chip label="g" size="small" sx={{ mx: 0.5 }} /> são sequenciais - pressione 'g' primeiro, depois a segunda tecla.
            </Typography>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setShowShortcutHelp(false)}>
            Fechar
          </Button>
        </DialogActions>
      </Dialog>
    </>
  );
};

export default KeyboardNavigation;