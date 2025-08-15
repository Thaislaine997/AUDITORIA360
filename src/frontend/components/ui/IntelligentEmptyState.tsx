import React, { useState } from 'react';
import {
  Box,
  Typography,
  Button,
  Card,
  CardContent,
  CardActions,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Chip,
  Avatar,
} from '@mui/material';
import {
  PlayArrow,
  Add,
  Lightbulb,
  CheckCircle,
  TrendingUp,
  PersonAdd,
  Settings,
  Description,
} from '@mui/icons-material';

interface EmptyStateGuide {
  title: string;
  description: string;
  videoUrl?: string;
  videoThumbnail?: string;
  actionButton: {
    text: string;
    action: () => void;
    icon?: React.ReactNode;
  };
  quickTips?: string[];
  estimatedTime?: string;
}

interface IntelligentEmptyStateProps {
  context: 'clients' | 'configurations' | 'documents' | 'reports';
  userProfile: 'gestor' | 'analista';
  onAction: () => void;
}

const IntelligentEmptyState: React.FC<IntelligentEmptyStateProps> = ({
  context,
  userProfile,
  onAction,
}) => {
  const [videoDialogOpen, setVideoDialogOpen] = useState(false);
  const [currentGuide, setCurrentGuide] = useState<EmptyStateGuide | null>(null);

  const getGuideByContext = (): EmptyStateGuide => {
    const guides: Record<string, Record<string, EmptyStateGuide>> = {
      clients: {
        gestor: {
          title: 'Cadastre seu primeiro cliente',
          description: 'Como gestor, comece cadastrando um cliente para sua equipe trabalhar. O sistema irá sugerir as melhores configurações baseadas no perfil da empresa.',
          videoUrl: '/videos/gestor-primeiro-cliente.mp4',
          videoThumbnail: '/images/thumbnails/gestor-cliente.jpg',
          actionButton: {
            text: 'Cadastrar primeiro cliente',
            action: onAction,
            icon: <PersonAdd />
          },
          quickTips: [
            'Use templates por segmento para acelerar a configuração',
            'Defina as permissões da equipe desde o início',
            'Configure os canais de comunicação (Email, WhatsApp)'
          ],
          estimatedTime: '5 minutos'
        },
        analista: {
          title: 'Adicione um novo cliente',
          description: 'Comece adicionando um cliente ao sistema. Você poderá configurar os documentos e canais de envio de acordo com as necessidades dele.',
          videoUrl: '/videos/analista-novo-cliente.mp4',
          videoThumbnail: '/images/thumbnails/analista-cliente.jpg',
          actionButton: {
            text: 'Adicionar cliente',
            action: onAction,
            icon: <Add />
          },
          quickTips: [
            'Tenha em mãos: CNPJ, email principal e telefone',
            'Identifique o regime tributário da empresa',
            'Prepare a lista de documentos necessários'
          ],
          estimatedTime: '3 minutos'
        }
      },
      configurations: {
        gestor: {
          title: 'Configure a automação inteligente',
          description: 'Defina regras de automação para que o sistema configure clientes automaticamente baseado no perfil da empresa.',
          videoUrl: '/videos/gestor-automacao.mp4',
          actionButton: {
            text: 'Criar automação',
            action: onAction,
            icon: <Settings />
          },
          quickTips: [
            'Use lógica condicional (SE-ENTÃO) para automação',
            'Templates por segmento aceleram o processo',
            'Monitore o desempenho das regras criadas'
          ],
          estimatedTime: '10 minutos'
        },
        analista: {
          title: 'Configure seu primeiro envio',
          description: 'Configure como e quais documentos serão enviados para o cliente. O sistema possui templates que facilitam essa configuração.',
          videoUrl: '/videos/analista-configuracao.mp4',
          actionButton: {
            text: 'Configurar envio',
            action: onAction,
            icon: <Settings />
          },
          quickTips: [
            'Escolha os documentos obrigatórios para o regime tributário',
            'Configure múltiplos destinatários se necessário',
            'Teste a configuração no modo simulação'
          ],
          estimatedTime: '5 minutos'
        }
      },
      documents: {
        gestor: {
          title: 'Centralize seus documentos',
          description: 'Organize todos os documentos em um local seguro e acessível para sua equipe. Configure templates e automações.',
          videoUrl: '/videos/gestor-documentos.mp4',
          actionButton: {
            text: 'Fazer upload de documentos',
            action: onAction,
            icon: <Description />
          },
          quickTips: [
            'Organize por cliente e período',
            'Use tags para facilitar a busca',
            'Configure backup automático'
          ],
          estimatedTime: '3 minutos'
        },
        analista: {
          title: 'Faça upload dos documentos',
          description: 'Comece enviando os documentos que precisam ser processados e enviados para os clientes.',
          videoUrl: '/videos/analista-upload.mp4',
          actionButton: {
            text: 'Enviar documentos',
            action: onAction,
            icon: <Add />
          },
          quickTips: [
            'Formatos aceitos: PDF, XML, XLS, XLSX',
            'Máximo 50MB por arquivo',
            'Organize os arquivos por cliente'
          ],
          estimatedTime: '2 minutos'
        }
      },
      reports: {
        gestor: {
          title: 'Crie relatórios executivos',
          description: 'Configure dashboards e relatórios personalizados para acompanhar o desempenho da sua operação.',
          videoUrl: '/videos/gestor-relatorios.mp4',
          actionButton: {
            text: 'Criar primeiro relatório',
            action: onAction,
            icon: <TrendingUp />
          },
          quickTips: [
            'Use templates por tipo de análise',
            'Configure alertas automáticos',
            'Compartilhe relatórios com a equipe'
          ],
          estimatedTime: '8 minutos'
        },
        analista: {
          title: 'Gere relatórios operacionais',
          description: 'Crie relatórios para acompanhar o status dos envios e identificar possíveis problemas.',
          videoUrl: '/videos/analista-relatorios.mp4',
          actionButton: {
            text: 'Gerar relatório',
            action: onAction,
            icon: <Description />
          },
          quickTips: [
            'Filtre por período e cliente',
            'Exporte em PDF ou Excel',
            'Agende relatórios recorrentes'
          ],
          estimatedTime: '3 minutos'
        }
      }
    };

    return guides[context][userProfile];
  };

  const guide = getGuideByContext();

  const openVideoGuide = () => {
    setCurrentGuide(guide);
    setVideoDialogOpen(true);
  };

  const getContextIcon = () => {
    switch (context) {
      case 'clients':
        return <PersonAdd sx={{ fontSize: 80, color: 'primary.main' }} />;
      case 'configurations':
        return <Settings sx={{ fontSize: 80, color: 'secondary.main' }} />;
      case 'documents':
        return <Description sx={{ fontSize: 80, color: 'success.main' }} />;
      case 'reports':
        return <TrendingUp sx={{ fontSize: 80, color: 'warning.main' }} />;
      default:
        return <Lightbulb sx={{ fontSize: 80, color: 'info.main' }} />;
    }
  };

  return (
    <Box
      sx={{
        display: 'flex',
        flexDirection: 'column',
        alignItems: 'center',
        justifyContent: 'center',
        minHeight: '60vh',
        textAlign: 'center',
        p: 4,
      }}
    >
      {/* Main Empty State Card */}
      <Card 
        sx={{ 
          maxWidth: 600, 
          width: '100%',
          boxShadow: 3,
          borderRadius: 2
        }}
      >
        <CardContent sx={{ p: 4 }}>
          {/* Icon */}
          <Box sx={{ mb: 3 }}>
            {getContextIcon()}
          </Box>

          {/* Title and Description */}
          <Typography variant="h4" component="h2" gutterBottom>
            {guide.title}
          </Typography>
          
          <Typography 
            variant="body1" 
            color="text.secondary" 
            paragraph
            sx={{ fontSize: '1.1rem', lineHeight: 1.6 }}
          >
            {guide.description}
          </Typography>

          {/* Time Estimate */}
          {guide.estimatedTime && (
            <Chip 
              icon={<CheckCircle />}
              label={`Tempo estimado: ${guide.estimatedTime}`}
              color="success"
              variant="outlined"
              sx={{ mb: 3 }}
            />
          )}

          {/* Quick Tips */}
          {guide.quickTips && guide.quickTips.length > 0 && (
            <Box sx={{ mb: 3, textAlign: 'left' }}>
              <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
                <Lightbulb sx={{ mr: 1, color: 'warning.main' }} />
                Dicas Rápidas:
              </Typography>
              <List dense>
                {guide.quickTips.map((tip, index) => (
                  <ListItem key={index} sx={{ py: 0.5 }}>
                    <ListItemIcon sx={{ minWidth: 32 }}>
                      <CheckCircle color="success" fontSize="small" />
                    </ListItemIcon>
                    <ListItemText 
                      primary={tip}
                      primaryTypographyProps={{ variant: 'body2' }}
                    />
                  </ListItem>
                ))}
              </List>
            </Box>
          )}
        </CardContent>

        <CardActions sx={{ justifyContent: 'center', pb: 3, pt: 0 }}>
          <Box sx={{ display: 'flex', gap: 2, flexWrap: 'wrap' }}>
            {/* Video Guide Button */}
            {guide.videoUrl && (
              <Button
                variant="outlined"
                startIcon={<PlayArrow />}
                onClick={openVideoGuide}
                size="large"
              >
                Ver guia em vídeo (2 min)
              </Button>
            )}

            {/* Main Action Button */}
            <Button
              variant="contained"
              size="large"
              startIcon={guide.actionButton.icon}
              onClick={guide.actionButton.action}
              sx={{ minWidth: 200 }}
            >
              {guide.actionButton.text}
            </Button>
          </Box>
        </CardActions>
      </Card>

      {/* Additional Help Section */}
      <Box sx={{ mt: 4, textAlign: 'center' }}>
        <Typography variant="body2" color="text.secondary">
          Precisa de ajuda? Acesse nossa{' '}
          <Button 
            variant="text" 
            size="small"
            onClick={() => window.open('/help', '_blank')}
          >
            documentação completa
          </Button>
          {' '}ou entre em contato com o suporte.
        </Typography>
      </Box>

      {/* Video Guide Dialog */}
      <Dialog
        open={videoDialogOpen}
        onClose={() => setVideoDialogOpen(false)}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Avatar sx={{ mr: 2, bgcolor: 'primary.main' }}>
              <PlayArrow />
            </Avatar>
            {currentGuide?.title}
          </Box>
        </DialogTitle>
        
        <DialogContent>
          {currentGuide?.videoUrl && (
            <Box sx={{ position: 'relative', paddingTop: '56.25%', mb: 2 }}>
              <video
                controls
                autoPlay
                style={{
                  position: 'absolute',
                  top: 0,
                  left: 0,
                  width: '100%',
                  height: '100%',
                  borderRadius: 8,
                }}
              >
                <source src={currentGuide.videoUrl} type="video/mp4" />
                Seu navegador não suporta o elemento de vídeo.
              </video>
            </Box>
          )}
          
          <Typography variant="body1" paragraph>
            {currentGuide?.description}
          </Typography>
        </DialogContent>
        
        <DialogActions>
          <Button onClick={() => setVideoDialogOpen(false)}>
            Fechar
          </Button>
          <Button 
            variant="contained" 
            onClick={() => {
              setVideoDialogOpen(false);
              currentGuide?.actionButton.action();
            }}
            startIcon={currentGuide?.actionButton.icon}
          >
            {currentGuide?.actionButton.text}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default IntelligentEmptyState;