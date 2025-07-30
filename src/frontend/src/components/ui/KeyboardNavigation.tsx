import React, { useEffect, useCallback } from 'react';
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
} from '@mui/material';
import {
  Keyboard,
  ExpandMore,
} from '@mui/icons-material';

interface KeyboardShortcut {
  key: string;
  description: string;
  action: () => void;
  section: string;
}

interface KeyboardNavigationProps {
  children: React.ReactNode;
}

const KeyboardNavigation: React.FC<KeyboardNavigationProps> = ({ children }) => {
  const navigate = useNavigate();
  const [shortcutTooltip, setShortcutTooltip] = React.useState<string>('');
  const [showShortcutHelp, setShowShortcutHelp] = React.useState(false);

  const shortcuts: KeyboardShortcut[] = [
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
      action: () => navigate('/clients'),
      section: 'Navegação',
    },
    {
      key: 'g+p',
      description: 'Ir para Folha de Pagamento',
      action: () => navigate('/payroll'),
      section: 'Navegação',
    },
    {
      key: 'g+f',
      description: 'Ir para Documentos',
      action: () => navigate('/documents'),
      section: 'Navegação',
    },
    {
      key: 'g+r',
      description: 'Ir para Relatórios',
      action: () => navigate('/reports'),
      section: 'Navegação',
    },
    {
      key: 'g+a',
      description: 'Ir para Auditoria',
      action: () => navigate('/audit'),
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