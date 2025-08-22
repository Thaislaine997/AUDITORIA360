
import React from "react";
import { NextPage } from "next";
import Head from "next/head";
import Link from "next/link";
import {
  Box,
  Typography,
  Container,
  Grid,
  Button,
  Card,
  CardContent,
  CardActions,
  Divider,
  AppBar,
  Toolbar,
  IconButton,
  Drawer,
  List,
  ListItem,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  useMediaQuery,
  useTheme,
  Tooltip,
  Fade,
} from "@mui/material";
import MenuIcon from '@mui/icons-material/Menu';
import WhatsAppIcon from '@mui/icons-material/WhatsApp';
import InstagramIcon from '@mui/icons-material/Instagram';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import PhoneIcon from '@mui/icons-material/Phone';

const navigation = [
  { name: 'Quem Somos', href: '#quem-somos' },
  { name: 'Serviços', href: '#servicos' },
  { name: 'Planos', href: '#planos' },
  { name: 'FAQ', href: '#faq' },
  { name: 'Contato', href: '#contato' },
];

function scrollToSection(id: string) {
  if (typeof window !== 'undefined') {
    const el = document.querySelector(id);
    if (el) {
      const yOffset = -90; // compensa header fixo
      const y = el.getBoundingClientRect().top + window.pageYOffset + yOffset;
      window.scrollTo({ top: y, behavior: 'smooth' });
    }
  }
}
// Sobre a Empresa
const sobreEmpresa = [
  {
    icon: "https://cdn-icons-png.flaticon.com/512/1828/1828884.png",
    title: "Missão",
    color: "primary",
    desc: "Simplificar e potencializar a gestão de pessoas, promovendo eficiência, segurança e inovação para empresas de todos os portes.",
  },
  {
    icon: "https://cdn-icons-png.flaticon.com/512/1828/1828885.png",
    title: "Valores",
    color: "success.main",
    desc: "Ética, transparência, parceria, inovação, excelência e foco no cliente.",
  },
  {
    icon: "https://cdn-icons-png.flaticon.com/512/1828/1828886.png",
    title: "Princípios",
    color: "secondary",
    desc: (
      <>
        Atendimento humanizado.<br />Compromisso com resultados.<br />Segurança e conformidade em todos os processos.
      </>
    ),
  },
];

// Diferenciais reais DPEIXER
const diferenciais = [
  {
    icon: "https://cdn-icons-png.flaticon.com/512/3135/3135768.png",
    title: "Tecnologia Proprietária",
    desc: "Plataforma AUDITORIA360 exclusiva, com automação, relatórios inteligentes e integração total com eSocial.",
  },
  {
    icon: "https://cdn-icons-png.flaticon.com/512/3135/3135789.png",
    title: "Especialistas em BPO de RH",
    desc: "Equipe multidisciplinar com +20 anos de experiência em terceirização, folha, DP e projetos de RH sob medida.",
  },
  {
    icon: "https://cdn-icons-png.flaticon.com/512/3135/3135792.png",
    title: "Atendimento Consultivo",
    desc: "Suporte humanizado, multicanal e proativo, com SLA definido e acompanhamento estratégico.",
  },
  {
    icon: "https://cdn-icons-png.flaticon.com/512/3135/3135779.png",
    title: "Compliance e Segurança",
    desc: "Processos auditados, conformidade total com legislação e proteção de dados (LGPD).",
  },
  {
    icon: "https://cdn-icons-png.flaticon.com/512/3135/3135781.png",
    title: "Flexibilidade e Customização",
    desc: "Soluções adaptadas à realidade de cada cliente, com planos e integrações sob demanda.",
  },
];

// Planos de RH
const planosRH = [
  {
    name: "Plus RH",
    price: "39,90",
    description:
      "Todos os serviços de RH, exceto admissão, rescisão e documentos personalizados.",
    features: [
      "Gestão do ponto digital",
      "Portal do empregado",
      "Gestão de benefícios",
      "Gestão de férias",
      "Relatórios básicos",
      "Suporte por email",
    ],
    popular: false,
    icon: "https://cdn-icons-png.flaticon.com/512/3135/3135715.png",
  },
  {
    name: "Premium RH",
    price: "49,90",
    description: "Tudo do Plus + admissões e rescisões digitais.",
    features: [
      "Todos os recursos do Plus RH",
      "Admissões/rescisões digitais",
      "Homologações por videochamada",
      "Portal AUDITORIA360 básico",
      "Suporte prioritário",
    ],
    popular: true,
    icon: "https://cdn-icons-png.flaticon.com/512/3135/3135716.png",
  },
  {
    name: "Diamante RH",
    price: "69,90",
    description:
      "Premium + documentação personalizada, reuniões estratégicas, people analytics.",
    features: [
      "Todos os recursos do Premium RH",
      "Documentação personalizada",
      "Reuniões estratégicas mensais",
      "People Analytics avançado",
      "Portal AUDITORIA360 completo",
      "Suporte dedicado 24/7",
    ],
    popular: false,
    icon: "https://cdn-icons-png.flaticon.com/512/3135/3135717.png",
  },
];

const bannerOptions = [
  {
    label: 'Unsplash',
    file: '/hero-bg-unsplash.jpg',
    url: 'https://unsplash.com/photos/people-in-a-meeting-room-5QgIuuBxKwM',
  },
  {
    label: 'Pexels',
    file: '/hero-bg-pexels.jpg',
    url: 'https://www.pexels.com/photo/group-of-people-having-a-meeting-1181406/',
  },
  {
    label: 'Pixabay',
    file: '/hero-bg-pixabay.jpg',
    url: 'https://pixabay.com/photos/startup-meeting-brainstorming-594090/',
  },
];

const HomePage: NextPage = () => {
  const [bannerIdx, setBannerIdx] = React.useState(0);
  const [drawerOpen, setDrawerOpen] = React.useState(false);
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const banner = bannerOptions[bannerIdx];
  return (
    <>
      <Head>
        <title>DPEIXER | BPO de RH, Terceirização de Folha, Consultoria e Portal AUDITORIA360</title>
        <meta name="description" content="Especialistas em assessoria, terceirização de DP e RH, consultoria, treinamentos e serviços sob demanda. Portal AUDITORIA360: tecnologia, compliance e excelência para contabilidades e empresas." />
        <meta name="viewport" content="width=device-width, initial-scale=1" />
      </Head>
      {/* Header Institucional Moderno */}
      <AppBar position="fixed" color="default" elevation={4} sx={{ background: 'linear-gradient(90deg, #0d47a1 60%, #1976d2 100%)', color: 'white', boxShadow: '0 4px 24px #0002', zIndex: 1201 }}>
        <Toolbar sx={{ minHeight: 72, px: { xs: 1, md: 4 } }}>
          <Box sx={{ display: 'flex', alignItems: 'center', flexGrow: 1 }}>
            <img src="/logo.png" onError={(e) => { e.currentTarget.style.display = 'none'; }} alt="Logo DPEIXER" style={{ height: 44, marginRight: 16, filter: 'drop-shadow(0 2px 8px #0006)' }} />
            <Box>
              <Typography variant="h5" color="inherit" sx={{ fontWeight: 900, letterSpacing: 1, lineHeight: 1 }}>
                DPEIXER
              </Typography>
              <Typography variant="caption" sx={{ color: '#fff', opacity: 0.85, fontWeight: 500, letterSpacing: 1 }}>
                BPO de RH, Folha, Consultoria e Tecnologia
              </Typography>
            </Box>
          </Box>
          {/* Contatos e redes sociais desktop */}
          {!isMobile && (
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 2, mr: 3 }}>
              <Tooltip title="Fale conosco" arrow TransitionComponent={Fade}>
                <Button startIcon={<PhoneIcon />} href="tel:+5547933835427" sx={{ color: '#fff', fontWeight: 700, textTransform: 'none', fontSize: 16 }}>
                  (47) 93383-5427
                </Button>
              </Tooltip>
              <Tooltip title="WhatsApp" arrow TransitionComponent={Fade}>
                <IconButton href="https://wa.link/vbonkz" target="_blank" rel="noopener" sx={{ color: '#25d366' }}>
                  <WhatsAppIcon fontSize="medium" />
                </IconButton>
              </Tooltip>
              <Tooltip title="Instagram" arrow TransitionComponent={Fade}>
                <IconButton href="https://www.instagram.com/dpeixer_assessoria?igsh=MTF4dXRoODdseDJ0aw%3D%3D&utm_source=qr" target="_blank" rel="noopener" sx={{ color: '#fff' }}>
                  <InstagramIcon fontSize="medium" />
                </IconButton>
              </Tooltip>
              <Tooltip title="LinkedIn" arrow TransitionComponent={Fade}>
                <IconButton href="https://www.linkedin.com/company/dpeixer-assessoria-terceiriza%C3%A7%C3%A3o/about/?viewAsMember=true" target="_blank" rel="noopener" sx={{ color: '#fff' }}>
                  <LinkedInIcon fontSize="medium" />
                </IconButton>
              </Tooltip>
            </Box>
          )}
          {/* Navegação */}
          {!isMobile ? (
            <Box sx={{ display: 'flex', gap: 2, alignItems: 'center' }}>
              {navigation.map((item) => (
                <Button key={item.name} color="inherit" onClick={() => scrollToSection(item.href)} sx={{ fontWeight: 700, letterSpacing: 1, px: 2, py: 1, borderRadius: 2, transition: 'background .2s', '&:hover': { background: '#1565c0' } }}>{item.name}</Button>
              ))}
              <Link href="/login" passHref legacyBehavior>
                <Button variant="contained" color="secondary" sx={{ fontWeight: 800, boxShadow: 3, borderRadius: 2, px: 3, py: 1.2, ml: 1, fontSize: 16 }}>
                  Portal AUDITORIA360
                </Button>
              </Link>
            </Box>
          ) : (
            <>
              <IconButton edge="end" color="inherit" onClick={() => setDrawerOpen(true)} aria-label="menu" sx={{ ml: 1 }}>
                <MenuIcon fontSize="large" />
              </IconButton>
              <Drawer anchor="right" open={drawerOpen} onClose={() => setDrawerOpen(false)} PaperProps={{ sx: { width: 260, background: 'linear-gradient(120deg, #1976d2 60%, #90caf9 100%)', color: '#fff' } }}>
                <Box sx={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
                  <Box sx={{ display: 'flex', alignItems: 'center', p: 2, pb: 1 }}>
                    <img src="/logo.png" alt="Logo DPEIXER" style={{ height: 36, marginRight: 10 }} />
                    <Typography variant="h6" fontWeight={900}>DPEIXER</Typography>
                  </Box>
                  <List>
                    {navigation.map((item) => (
                      <ListItem key={item.name} disablePadding>
                        <ListItemButton onClick={() => { scrollToSection(item.href); setDrawerOpen(false); }}>
                          <ListItemText primary={item.name} primaryTypographyProps={{ fontWeight: 700, fontSize: 17 }} />
                        </ListItemButton>
                      </ListItem>
                    ))}
                    <ListItem disablePadding>
                      <Link href="/login" passHref legacyBehavior>
                        <ListItemButton component="a">
                          <ListItemText primary="Portal AUDITORIA360" primaryTypographyProps={{ fontWeight: 800, fontSize: 17 }} />
                        </ListItemButton>
                      </Link>
                    </ListItem>
                  </List>
                  <Box sx={{ flexGrow: 1 }} />
                  <Box sx={{ display: 'flex', justifyContent: 'center', gap: 1.5, pb: 2 }}>
                    <Tooltip title="WhatsApp" arrow TransitionComponent={Fade}>
                      <IconButton href="https://wa.link/vbonkz" target="_blank" rel="noopener" sx={{ color: '#25d366' }}>
                        <WhatsAppIcon fontSize="medium" />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="Instagram" arrow TransitionComponent={Fade}>
                      <IconButton href="https://www.instagram.com/dpeixer_assessoria?igsh=MTF4dXRoODdseDJ0aw%3D%3D&utm_source=qr" target="_blank" rel="noopener" sx={{ color: '#fff' }}>
                        <InstagramIcon fontSize="medium" />
                      </IconButton>
                    </Tooltip>
                    <Tooltip title="LinkedIn" arrow TransitionComponent={Fade}>
                      <IconButton href="https://www.linkedin.com/company/dpeixer-assessoria-terceiriza%C3%A7%C3%A3o/about/?viewAsMember=true" target="_blank" rel="noopener" sx={{ color: '#fff' }}>
                        <LinkedInIcon fontSize="medium" />
                      </IconButton>
                    </Tooltip>
                  </Box>
                  <Box sx={{ textAlign: 'center', pb: 2, color: '#fff', opacity: 0.7, fontSize: 13 }}>
                    <PhoneIcon fontSize="small" sx={{ verticalAlign: 'middle', mr: 0.5 }} /> (47) 93383-5427
                  </Box>
                </Box>
              </Drawer>
            </>
          )}
        </Toolbar>
      </AppBar>

      {/* Banner/Hero comercial, institucional, com selos e CTA */}
      <Box id="quem-somos" sx={{
        background: `linear-gradient(120deg, #0d47a1ee 80%, #1976d2cc 100%), url('${banner.file}') center/cover`,
        color: "white",
        py: { xs: 10, md: 16 },
        textAlign: "center",
        minHeight: 420,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: 8,
        position: 'relative',
        transition: 'background-image 0.5s',
        overflow: 'hidden',
      }}>
        <Container maxWidth="md" sx={{ position: 'relative', zIndex: 2 }}>
          {/* Slogan institucional */}
          <Typography variant="h2" fontWeight={900} gutterBottom sx={{ letterSpacing: 1, textShadow: '0 2px 16px #000a', fontSize: { xs: 32, md: 48 } }}>
            RH Inteligente, Seguro e Humano para sua Empresa
          </Typography>
          <Typography variant="h5" sx={{ mb: 3, opacity: 0.97, textShadow: '0 1px 8px #0008', fontWeight: 600 }}>
            +20 anos de experiência nacional em BPO de RH, Folha e Consultoria. <br />
            <span style={{ color: '#ffe082', fontWeight: 900 }}>Atendimento em todo o Brasil.</span>
          </Typography>
          {/* Destaques animados */}
          <Grid container spacing={2} justifyContent="center" sx={{ mb: 2 }}>
            <Grid item xs={12} sm={4}>
              <Box sx={{
                bgcolor: 'rgba(25, 118, 210, 0.85)',
                borderRadius: 3,
                px: 2.5,
                py: 1.5,
                boxShadow: 6,
                mb: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 1.5,
                animation: 'fadeInUp 1s',
                minHeight: 56,
              }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135789.png" alt="Especialistas" style={{ height: 32, marginRight: 8 }} />
                <Typography variant="h6" fontWeight={800} sx={{ color: '#fff', textShadow: '0 1px 6px #0006', fontSize: { xs: 16, md: 18 } }}>Especialistas em RH</Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Box sx={{
                bgcolor: 'rgba(25, 118, 210, 0.85)',
                borderRadius: 3,
                px: 2.5,
                py: 1.5,
                boxShadow: 6,
                mb: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 1.5,
                animation: 'fadeInUp 1.2s',
                minHeight: 56,
              }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135768.png" alt="Tecnologia" style={{ height: 32, marginRight: 8 }} />
                <Typography variant="h6" fontWeight={800} sx={{ color: '#fff', textShadow: '0 1px 6px #0006', fontSize: { xs: 16, md: 18 } }}>Tecnologia exclusiva</Typography>
              </Box>
            </Grid>
            <Grid item xs={12} sm={4}>
              <Box sx={{
                bgcolor: 'rgba(25, 118, 210, 0.85)',
                borderRadius: 3,
                px: 2.5,
                py: 1.5,
                boxShadow: 6,
                mb: 1,
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: 1.5,
                animation: 'fadeInUp 1.4s',
                minHeight: 56,
              }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135781.png" alt="Foco no cliente" style={{ height: 32, marginRight: 8 }} />
                <Typography variant="h6" fontWeight={800} sx={{ color: '#fff', textShadow: '0 1px 6px #0006', fontSize: { xs: 16, md: 18 } }}>Foco no cliente</Typography>
              </Box>
            </Grid>
          </Grid>
          {/* Selos de confiança */}
          <Box sx={{ display: 'flex', justifyContent: 'center', gap: 3, mb: 2, flexWrap: 'wrap' }}>
            <Box sx={{ bgcolor: '#fff', color: 'primary.main', borderRadius: 3, px: 2.5, py: 1, boxShadow: 4, fontWeight: 900, fontSize: 18, display: 'flex', alignItems: 'center', gap: 1, minWidth: 170 }}>
              <img src="https://cdn-icons-png.flaticon.com/512/3135/3135789.png" alt="20 anos" style={{ height: 28, marginRight: 8 }} />
              +20 anos de experiência
            </Box>
            <Box sx={{ bgcolor: '#fff', color: 'primary.main', borderRadius: 3, px: 2.5, py: 1, boxShadow: 4, fontWeight: 900, fontSize: 18, display: 'flex', alignItems: 'center', gap: 1, minWidth: 170 }}>
              <img src="https://cdn-icons-png.flaticon.com/512/3135/3135792.png" alt="Atendimento nacional" style={{ height: 28, marginRight: 8 }} />
              Atendimento nacional
            </Box>
            <Box sx={{ bgcolor: '#fff', color: 'primary.main', borderRadius: 3, px: 2.5, py: 1, boxShadow: 4, fontWeight: 900, fontSize: 18, display: 'flex', alignItems: 'center', gap: 1, minWidth: 170 }}>
              <img src="https://cdn-icons-png.flaticon.com/512/3135/3135779.png" alt="Clientes satisfeitos" style={{ height: 28, marginRight: 8 }} />
              Clientes satisfeitos
            </Box>
          </Box>
          {/* CTA principal e secundário */}
          <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, justifyContent: 'center', gap: 2, mt: 3 }}>
            <Link href="#planos" passHref legacyBehavior>
              <Button variant="contained" color="secondary" size="large" sx={{ px: 7, py: 2.5, fontWeight: 800, fontSize: 20, borderRadius: 3, boxShadow: 4 }}>
                Solicite uma demonstração
              </Button>
            </Link>
            <Link href="#contato" passHref legacyBehavior>
              <Button variant="outlined" color="inherit" size="large" sx={{ px: 5, py: 2.5, fontWeight: 800, fontSize: 18, borderRadius: 3, boxShadow: 2, border: '2px solid #fff', color: '#fff', '&:hover': { bgcolor: '#fff', color: 'primary.main' } }}>
                Fale com um especialista
              </Button>
            </Link>
          </Box>
        </Container>
        {/* Animação sutil de fundo */}
        <Box sx={{
          position: 'absolute',
          top: 0,
          left: 0,
          width: '100%',
          height: '100%',
          pointerEvents: 'none',
          zIndex: 1,
        }}>
          <Box sx={{
            position: 'absolute',
            top: { xs: 30, md: 60 },
            left: { xs: 10, md: 60 },
            width: 80,
            height: 80,
            bgcolor: 'secondary.light',
            opacity: 0.13,
            borderRadius: '50%',
            filter: 'blur(2px)',
            animation: 'floatY 5s ease-in-out infinite',
          }} />
          <Box sx={{
            position: 'absolute',
            bottom: { xs: 20, md: 60 },
            right: { xs: 10, md: 60 },
            width: 100,
            height: 100,
            bgcolor: 'primary.light',
            opacity: 0.11,
            borderRadius: '50%',
            filter: 'blur(2px)',
            animation: 'floatY 7s ease-in-out infinite reverse',
          }} />
        </Box>
        <style jsx global>{`
          @keyframes fadeInUp {
            from { opacity: 0; transform: translateY(30px); }
            to { opacity: 1; transform: translateY(0); }
          }
          @keyframes floatY {
            0% { transform: translateY(0); }
            50% { transform: translateY(-18px); }
            100% { transform: translateY(0); }
          }
        `}</style>
        <Box sx={{ position: 'absolute', bottom: 0, left: 0, width: '100%', height: 40, background: 'linear-gradient(0deg, #fff 0%, transparent 100%)', zIndex: 3 }} />
      </Box>

  {/* ...existing code... */}
      <Box sx={{ background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', py: 10 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" fontWeight={900} color="primary" align="center" sx={{ mb: 5, letterSpacing: 1 }}>
            Por que escolher a DPEIXER?
          </Typography>
          <Grid container spacing={4} justifyContent="center">
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 3 }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135768.png" alt="Tecnologia" style={{ height: 44, marginRight: 16 }} />
                <Box>
                  <Typography variant="h6" fontWeight={800} color="primary" gutterBottom>Tecnologia Proprietária</Typography>
                  <Typography variant="body2">Plataforma AUDITORIA360 exclusiva, automação, relatórios inteligentes e integração total com eSocial.</Typography>
                </Box>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 3 }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135789.png" alt="Especialistas" style={{ height: 44, marginRight: 16 }} />
                <Box>
                  <Typography variant="h6" fontWeight={800} color="primary" gutterBottom>Especialistas em BPO de RH</Typography>
                  <Typography variant="body2">+20 anos de experiência em terceirização, folha, DP e projetos de RH sob medida.</Typography>
                </Box>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 3 }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135792.png" alt="Atendimento" style={{ height: 44, marginRight: 16 }} />
                <Box>
                  <Typography variant="h6" fontWeight={800} color="primary" gutterBottom>Atendimento Consultivo</Typography>
                  <Typography variant="body2">Suporte humanizado, multicanal, com SLA definido e acompanhamento estratégico.</Typography>
                </Box>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 3 }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135779.png" alt="Compliance" style={{ height: 44, marginRight: 16 }} />
                <Box>
                  <Typography variant="h6" fontWeight={800} color="primary" gutterBottom>Compliance e Segurança</Typography>
                  <Typography variant="body2">Processos auditados, conformidade total com legislação e proteção de dados (LGPD).</Typography>
                </Box>
              </Box>
            </Grid>
            <Grid item xs={12} md={4}>
              <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 3 }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135781.png" alt="Flexibilidade" style={{ height: 44, marginRight: 16 }} />
                <Box>
                  <Typography variant="h6" fontWeight={800} color="primary" gutterBottom>Flexibilidade e Customização</Typography>
                  <Typography variant="body2">Soluções adaptadas à realidade de cada cliente, com planos e integrações sob demanda.</Typography>
                </Box>
              </Box>
              <Box sx={{ display: 'flex', alignItems: 'flex-start', mb: 3 }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135767.png" alt="Foco no cliente" style={{ height: 44, marginRight: 16 }} />
                <Box>
                  <Typography variant="h6" fontWeight={800} color="primary" gutterBottom>Foco no seu negócio</Typography>
                  <Typography variant="body2">Você dedica energia ao crescimento, enquanto cuidamos de toda a rotina trabalhista, previdenciária e de RH.</Typography>
                </Box>
              </Box>
            </Grid>
          </Grid>
        </Container>
      </Box>







      {/* Como funciona na prática? (único bloco de etapas) */}
      <Box sx={{ background: 'linear-gradient(120deg, #e3f2fd 60%, #fff 100%)', py: 8 }}>
        <Container maxWidth="lg">
          <Typography variant="h4" fontWeight={900} color="primary" align="center" sx={{ mb: 6, letterSpacing: 1 }}>
            Como funciona na prática?
          </Typography>
          <Grid container spacing={4} justifyContent="center">
            <Grid item xs={12} md={3}>
              <Card sx={{ p: 3, borderRadius: 4, boxShadow: 4, background: '#fff', minHeight: 180, textAlign: 'center' }}>
                <Typography variant="h3" color="primary" fontWeight={900}>1</Typography>
                <Typography variant="h6" fontWeight={700} gutterBottom>Diagnóstico</Typography>
                <Typography variant="body2">Análise dos processos atuais, necessidades e oportunidades.</Typography>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card sx={{ p: 3, borderRadius: 4, boxShadow: 4, background: '#fff', minHeight: 180, textAlign: 'center' }}>
                <Typography variant="h3" color="primary" fontWeight={900}>2</Typography>
                <Typography variant="h6" fontWeight={700} gutterBottom>Implantação</Typography>
                <Typography variant="body2">Migração de dados, parametrização, treinamento.</Typography>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card sx={{ p: 3, borderRadius: 4, boxShadow: 4, background: '#fff', minHeight: 180, textAlign: 'center' }}>
                <Typography variant="h3" color="primary" fontWeight={900}>3</Typography>
                <Typography variant="h6" fontWeight={700} gutterBottom>Gestão mensal</Typography>
                <Typography variant="body2">Processamento da folha, obrigações e suporte contínuo.</Typography>
              </Card>
            </Grid>
            <Grid item xs={12} md={3}>
              <Card sx={{ p: 3, borderRadius: 4, boxShadow: 4, background: '#fff', minHeight: 180, textAlign: 'center' }}>
                <Typography variant="h3" color="primary" fontWeight={900}>4</Typography>
                <Typography variant="h6" fontWeight={700} gutterBottom>Auditoria e evolução</Typography>
                <Typography variant="body2">Acompanhamento de indicadores e melhorias contínuas.</Typography>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Perguntas Frequentes */}
      <Box id="faq" sx={{ background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', py: 8 }}>
        <Container maxWidth="md">
          <Typography variant="h4" fontWeight={900} color="primary" align="center" sx={{ mb: 6, letterSpacing: 1 }}>
            Perguntas Frequentes
          </Typography>
          <Box sx={{ background: '#fff', borderRadius: 4, boxShadow: 4, p: 4 }}>
            <Typography variant="subtitle1" fontWeight={700} color="secondary" gutterBottom>
              O que está incluso na terceirização da folha?
            </Typography>
            <Typography variant="body2" sx={{ mb: 3 }}>
              Processamento completo da folha, encargos, obrigações acessórias, admissão, rescisão, férias, relatórios, atendimento e acesso à plataforma AUDITORIA360.
            </Typography>
            <Typography variant="subtitle1" fontWeight={700} color="secondary" gutterBottom>
              Como é feito o atendimento?
            </Typography>
            <Typography variant="body2" sx={{ mb: 3 }}>
              Atendimento consultivo, humanizado e multicanal (telefone, e-mail, portal e WhatsApp), com SLA definido e especialistas dedicados.
            </Typography>
            <Typography variant="subtitle1" fontWeight={700} color="secondary" gutterBottom>
              A DPEIXER atende empresas de qualquer porte?
            </Typography>
            <Typography variant="body2">
              Sim! Atendemos desde pequenas empresas até grandes grupos, inclusive contabilidades e escritórios de BPO.
            </Typography>
          </Box>
        </Container>
      </Box>

      {/* CTA Final */}
      <Box sx={{ background: 'linear-gradient(90deg, #1976d2 60%, #90caf9 100%)', color: 'white', py: 8, textAlign: 'center', boxShadow: 8 }}>
        <Container maxWidth="md">
          <Typography variant="h4" fontWeight={900} sx={{ mb: 2, letterSpacing: 1 }}>
            Pronto para transformar o RH da sua empresa?
          </Typography>
          <Typography variant="h6" sx={{ mb: 4, opacity: 0.95 }}>
            Fale com nossos especialistas e descubra como a DPEIXER pode revolucionar sua gestão de pessoas.
          </Typography>
          <Link href="/login" passHref legacyBehavior>
            <Button variant="contained" color="secondary" size="large" sx={{ px: 7, py: 2.5, fontWeight: 800, fontSize: 20, borderRadius: 3, boxShadow: 4 }}>
              Solicitar contato
            </Button>
          </Link>
        </Container>
      </Box>

      {/* Sobre a DPEIXER (institucional, sem repetir diferenciais/valores) */}
      <Box id="sobre" sx={{ background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', py: 8, position: 'relative', overflow: 'hidden' }}>
        <Container maxWidth="lg">
          <Typography variant="h4" fontWeight={900} color="primary" align="center" sx={{ mb: 6, letterSpacing: 1 }}>
            Sobre a DPEIXER
          </Typography>
          <Typography variant="body1" align="center" sx={{ maxWidth: 700, mx: 'auto', mb: 4 }}>
            A DPEIXER nasceu para transformar a gestão de pessoas no Brasil, unindo tecnologia, experiência e atendimento humano. Somos referência em soluções de RH, folha e consultoria para empresas de todos os portes, com atuação nacional e foco em inovação e segurança.
          </Typography>
          <Grid container spacing={4} justifyContent="center">
            {sobreEmpresa.map((item) => (
              <Grid item xs={12} md={4} key={item.title}>
                <Card sx={{
                  p: 4,
                  borderRadius: 5,
                  boxShadow: 8,
                  textAlign: 'center',
                  background: `linear-gradient(120deg, #fff 60%, #e3f2fd 100%)`,
                  border: '2px solid #1976d2',
                  transition: 'transform .25s, box-shadow .25s',
                  '&:hover': {
                    transform: 'translateY(-8px) scale(1.03)',
                    boxShadow: 16,
                    background: 'linear-gradient(120deg, #e3f2fd 60%, #fff 100%)',
                  },
                }}>
                  <Box sx={{ mb: 2 }}>
                    <img src={item.icon} alt={item.title} style={{ height: 56, filter: 'drop-shadow(0 2px 8px #1976d2aa)' }} />
                  </Box>
                  <Typography variant="h5" fontWeight={900} color={item.color} gutterBottom sx={{ letterSpacing: 1 }}>{item.title}</Typography>
                  <Typography variant="body1" color="text.secondary">{item.desc}</Typography>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
      </Box>

  {/* Removido bloco de diferenciais para evitar repetição, já incluso no bloco Por que escolher a DPEIXER? */}

      {/* Serviços detalhados */}
      <Divider id="servicos" sx={{ mb: 6, borderColor: '#1976d2', borderWidth: 2 }} />
      <Box id="servicos" sx={{ mb: 8, background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', py: 8, position: 'relative', overflow: 'hidden' }}>
        <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
          <Typography variant="h4" fontWeight={900} color="primary" align="center" gutterBottom sx={{ letterSpacing: 1, textShadow: '0 2px 8px #90caf9' }}>
            Serviços Especializados
          </Typography>
          <Grid container spacing={4} justifyContent="center">
            <Grid item xs={12} md={4}>
              <Card sx={{ p: 4, borderRadius: 4, boxShadow: 8, background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', border: '2px solid #1976d2', minHeight: 320, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start' }}>
                <Typography variant="h6" fontWeight={900} color="primary" gutterBottom>BPO de RH</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  O BPO de RH (Business Process Outsourcing) é a terceirização completa dos processos de RH, desde a admissão até o desligamento, incluindo gestão de benefícios, ponto, férias, folha, obrigações legais e atendimento ao colaborador. Permite que sua empresa foque no core business, ganhe eficiência, reduza custos e tenha acesso a especialistas e tecnologia de ponta.
                </Typography>
                <ul style={{ paddingLeft: 20, margin: 0, fontSize: 15 }}>
                  <li>Gestão de admissões, férias, rescisões e movimentações</li>
                  <li>Gestão de benefícios (VT, VR, saúde, etc.)</li>
                  <li>Gestão do ponto digital e banco de horas</li>
                  <li>Atendimento ao colaborador e gestores</li>
                  <li>Relatórios gerenciais e people analytics</li>
                  <li>Compliance e atualização legal</li>
                </ul>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ p: 4, borderRadius: 4, boxShadow: 8, background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', border: '2px solid #1976d2', minHeight: 320, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start' }}>
                <Typography variant="h6" fontWeight={900} color="primary" gutterBottom>Terceirização de Folha de Pagamento</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  Cuidamos de todo o processamento da folha de pagamento, encargos, obrigações acessórias, eSocial, cálculos, relatórios e suporte. Reduza riscos trabalhistas, evite multas e tenha total conformidade com a legislação.
                </Typography>
                <ul style={{ paddingLeft: 20, margin: 0, fontSize: 15 }}>
                  <li>Processamento mensal da folha e encargos</li>
                  <li>Geração de guias, relatórios e obrigações acessórias</li>
                  <li>Gestão de admissões, rescisões e férias</li>
                  <li>Entrega e validação do eSocial</li>
                  <li>Suporte técnico e consultivo</li>
                  <li>Auditoria e compliance contínuo</li>
                </ul>
              </Card>
            </Grid>
            <Grid item xs={12} md={4}>
              <Card sx={{ p: 4, borderRadius: 4, boxShadow: 8, background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', border: '2px solid #1976d2', minHeight: 320, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start' }}>
                <Typography variant="h6" fontWeight={900} color="primary" gutterBottom>Consultoria e Treinamentos</Typography>
                <Typography variant="body2" sx={{ mb: 2 }}>
                  Consultoria trabalhista, auditoria de processos, adequação à legislação, treinamentos práticos e workshops para equipes e gestores. Soluções sob medida para cada desafio do seu RH.
                </Typography>
                <ul style={{ paddingLeft: 20, margin: 0, fontSize: 15 }}>
                  <li>Consultoria em DP, RH e legislação</li>
                  <li>Auditoria de processos e compliance</li>
                  <li>Treinamentos presenciais e online</li>
                  <li>Workshops temáticos e capacitação</li>
                  <li>Projetos especiais sob demanda</li>
                </ul>
              </Card>
            </Grid>
          </Grid>
        </Container>
      </Box>

      {/* Planos */}
      <Divider id="planos" sx={{ mb: 6, borderColor: '#1976d2', borderWidth: 2 }} />
      <Box id="planos" sx={{ mb: 8, background: 'linear-gradient(120deg, #e3f2fd 60%, #fff 100%)', py: 8, position: 'relative', overflow: 'hidden' }}>
        <Box sx={{
          position: 'absolute',
          top: -40,
          left: -40,
          width: 120,
          height: 120,
          bgcolor: 'primary.light',
          opacity: 0.12,
          borderRadius: '50%',
          zIndex: 0,
        }} />
        <Typography
          variant="h4"
          fontWeight={900}
          gutterBottom
          align="center"
          color="primary"
          sx={{ letterSpacing: 1, textShadow: '0 2px 8px #90caf9' }}
        >
          Planos e Valores
        </Typography>
        <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
          <Grid container spacing={4} justifyContent="center">
            {planosRH.map((plan) => (
              <Grid item xs={12} md={4} key={plan.name}>
                <Card
                  variant="outlined"
                  sx={{
                    borderRadius: 4,
                    borderColor: plan.popular ? "secondary.main" : "grey.300",
                    boxShadow: plan.popular ? 10 : 4,
                    background: plan.popular
                      ? "linear-gradient(120deg, #1976d2 60%, #90caf9 100%)"
                      : "#fff",
                    color: plan.popular ? "#fff" : "inherit",
                    position: 'relative',
                    overflow: 'visible',
                    transition: "all .3s cubic-bezier(.4,2,.6,1)",
                    '&:hover': {
                      transform: 'translateY(-8px) scale(1.045)',
                      boxShadow: 20,
                      background: plan.popular
                        ? 'linear-gradient(120deg, #1565c0 60%, #90caf9 100%)'
                        : 'linear-gradient(120deg, #e3f2fd 60%, #fff 100%)',
                    },
                  }}
                >
                  {plan.popular && (
                    <Box sx={{
                      position: 'absolute',
                      top: -22,
                      left: '50%',
                      transform: 'translateX(-50%)',
                      bgcolor: 'secondary.main',
                      color: 'white',
                      px: 3,
                      py: 0.7,
                      borderRadius: 3,
                      fontWeight: 900,
                      fontSize: 18,
                      zIndex: 2,
                      boxShadow: 4,
                      border: '2.5px solid #fff',
                      letterSpacing: 1,
                    }}>
                      Mais Popular
                    </Box>
                  )}
                  <CardContent>
                    <Box sx={{ display: "flex", alignItems: "center", mb: 1 }}>
                      <img
                        src={plan.icon}
                        alt="icon"
                        style={{ height: 36, marginRight: 10, opacity: 0.9 }}
                      />
                      <Typography variant="h6" fontWeight={900} gutterBottom>
                        {plan.name}
                      </Typography>
                    </Box>
                    <Typography
                      variant="h4"
                      color={plan.popular ? "#fff" : "primary"}
                      fontWeight={900}
                    >
                      R$ {plan.price}
                      <Typography
                        variant="body2"
                        component="span"
                        color={plan.popular ? "#e3f2fd" : "text.secondary"}
                      >
                        /mês por vida
                      </Typography>
                    </Typography>
                    <Typography
                      variant="body2"
                      color={plan.popular ? "#e3f2fd" : "text.secondary"}
                      sx={{ mb: 2, mt: 1 }}
                    >
                      {plan.description}
                    </Typography>
                    <ul
                      style={{
                        paddingLeft: 20,
                        margin: 0,
                        color: plan.popular ? "#e3f2fd" : undefined,
                        fontWeight: 500,
                        fontSize: 16,
                      }}
                    >
                      {plan.features.map((f, i) => (
                        <li key={i}>{f}</li>
                      ))}
                    </ul>
                  </CardContent>
                  <CardActions>
                    <Button
                      fullWidth
                      variant={plan.popular ? "contained" : "outlined"}
                      color={plan.popular ? "secondary" : "primary"}
                      sx={{ fontWeight: 800, fontSize: 18, py: 1.5, borderRadius: 2 }}
                    >
                      Contratar Plano
                    </Button>
                  </CardActions>
                </Card>
              </Grid>
            ))}
          </Grid>
        </Container>
        <Box sx={{
          position: 'absolute',
          bottom: -40,
          right: -40,
          width: 120,
          height: 120,
          bgcolor: 'secondary.light',
          opacity: 0.12,
          borderRadius: '50%',
          zIndex: 0,
        }} />
      </Box>

      {/* Footer */}
      <Box component="footer" sx={{
        bgcolor: 'grey.900',
        color: 'grey.100',
        py: 8,
        mt: 10,
        boxShadow: 12,
        borderTopLeftRadius: { xs: 16, md: 40 },
        borderTopRightRadius: { xs: 16, md: 40 },
        position: 'relative',
        overflow: 'hidden',
      }}>
        <Box sx={{
          position: 'absolute',
          top: -60,
          left: -60,
          width: 180,
          height: 180,
          bgcolor: 'primary.main',
          opacity: 0.08,
          borderRadius: '50%',
          zIndex: 0,
        }} />
        <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
          <Grid container spacing={6} alignItems="flex-start">
            <Grid item xs={12} md={4} sx={{ mb: { xs: 4, md: 0 } }}>
              <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
                <img src="/logo.png" alt="Logo DPEIXER" style={{ height: 36, marginRight: 10, filter: 'drop-shadow(0 2px 8px #0006)' }} />
                <Typography variant="h6" fontWeight={900} color="inherit" sx={{ letterSpacing: 1 }}>
                  DPEIXER
                </Typography>
              </Box>
              <Typography variant="body2" color="grey.300" sx={{ mb: 2 }}>
                BPO de RH, Terceirização de Folha, Consultoria e Portal AUDITORIA360.
              </Typography>
              <Divider sx={{ bgcolor: 'grey.800', my: 2 }} />
              <Typography variant="caption" color="grey.600">
                &copy; {new Date().getFullYear()} DPEIXER. Todos os direitos reservados.
              </Typography>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" fontWeight={900} gutterBottom color="inherit" sx={{ letterSpacing: 1 }}>
                Serviços
              </Typography>
              <ul style={{ paddingLeft: 20, margin: 0, color: "#e3f2fd", fontWeight: 500, fontSize: 16, lineHeight: 2 }}>
                <li>Terceirização de Folha</li>
                <li>Consultoria Trabalhista</li>
                <li>Treinamentos</li>
                <li>Portal AUDITORIA360</li>
              </ul>
            </Grid>
            <Grid item xs={12} md={4}>
              <Typography variant="h6" fontWeight={900} gutterBottom color="inherit" sx={{ letterSpacing: 1 }}>
                Portal
              </Typography>
              <Link href="/login" passHref legacyBehavior>
                <Button color="secondary" variant="contained" sx={{ color: "#fff", fontWeight: 700, boxShadow: 2, mt: 1, borderRadius: 2, px: 4 }}>
                  Acessar AUDITORIA360
                </Button>
              </Link>
              <Typography variant="body2" color="grey.300" sx={{ mt: 3 }}>
                Gestão completa e auditoria inteligente
              </Typography>
              <Divider sx={{ bgcolor: 'grey.800', my: 2 }} />
              <Box sx={{ display: 'flex', gap: 2, mt: 2 }}>
                <a href="mailto:contato@dpeixer.com.br" style={{ color: '#90caf9', textDecoration: 'none', fontWeight: 700 }}>contato@dpeixer.com.br</a>
                <span style={{ color: '#90caf9' }}>|</span>
                <a href="https://www.linkedin.com/company/dpeixer" target="_blank" rel="noopener noreferrer" style={{ color: '#90caf9', textDecoration: 'none', fontWeight: 700 }}>LinkedIn</a>
              </Box>
            </Grid>
          </Grid>
        </Container>
        <Box sx={{
          position: 'absolute',
          bottom: -60,
          right: -60,
          width: 180,
          height: 180,
          bgcolor: 'secondary.main',
          opacity: 0.08,
          borderRadius: '50%',
          zIndex: 0,
        }} />
      </Box>
    </>
  );
};

export default HomePage;
