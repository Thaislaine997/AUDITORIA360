
import React from "react";
import { motion } from "framer-motion";
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

      {/* HERO INSTITUCIONAL E COMERCIAL REORGANIZADO */}
      <Box id="quem-somos" sx={{
        background: `linear-gradient(120deg, #0d47a1ee 80%, #1976d2cc 100%), url('${banner.file}') center/cover`,
        color: "white",
        py: { xs: 10, md: 14 },
        textAlign: "center",
        minHeight: 480,
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        boxShadow: 8,
        position: 'relative',
        transition: 'background-image 0.5s',
        overflow: 'hidden',
      }}>
        <Container maxWidth="md" sx={{ position: 'relative', zIndex: 2 }}>
          <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.5 }} transition={{ duration: 0.7 }}>
            <Typography variant="h2" fontWeight={900} gutterBottom sx={{ letterSpacing: 1, textShadow: '0 2px 16px #000a', fontSize: { xs: 28, md: 42 } }}>
              <span style={{ color: '#ffe082', fontWeight: 900 }}>DPEIXER</span> – Assessoria & Terceirização
            </Typography>
            <Typography variant="h5" sx={{ mb: 2, opacity: 0.97, textShadow: '0 1px 8px #0008', fontWeight: 600 }}>
              Soluções Integradas em RH, DP e Auditoria Inteligente
            </Typography>
            <Typography variant="body1" sx={{ mb: 3, fontSize: 18, opacity: 0.95, maxWidth: 700, mx: 'auto', textShadow: '0 1px 8px #0008' }}>
              A DPEIXER é especialista em Gestão de Recursos Humanos (BPO), Departamento Pessoal Terceirizado, Consultoria Trabalhista e Plataforma de Auditoria Digital.<br />
              Nosso propósito é simplificar processos, reduzir custos, garantir conformidade legal e entregar inteligência estratégica para empresas de todos os portes e escritórios contábeis.
            </Typography>
            <Grid container spacing={2} justifyContent="center" sx={{ mb: 2 }}>
              <Grid item xs={12} sm={4}>
                <Box sx={{ bgcolor: 'rgba(25, 118, 210, 0.85)', borderRadius: 3, px: 2.5, py: 1.5, boxShadow: 6, mb: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1.5, minHeight: 56 }}>
                  <img src="https://cdn-icons-png.flaticon.com/512/3135/3135789.png" alt="Especialistas" style={{ height: 32, marginRight: 8 }} />
                  <Typography variant="h6" fontWeight={800} sx={{ color: '#fff', fontSize: { xs: 16, md: 18 } }}>+20 anos de experiência</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box sx={{ bgcolor: 'rgba(25, 118, 210, 0.85)', borderRadius: 3, px: 2.5, py: 1.5, boxShadow: 6, mb: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1.5, minHeight: 56 }}>
                  <img src="https://cdn-icons-png.flaticon.com/512/3135/3135768.png" alt="Tecnologia" style={{ height: 32, marginRight: 8 }} />
                  <Typography variant="h6" fontWeight={800} sx={{ color: '#fff', fontSize: { xs: 16, md: 18 } }}>Plataforma própria</Typography>
                </Box>
              </Grid>
              <Grid item xs={12} sm={4}>
                <Box sx={{ bgcolor: 'rgba(25, 118, 210, 0.85)', borderRadius: 3, px: 2.5, py: 1.5, boxShadow: 6, mb: 1, display: 'flex', alignItems: 'center', justifyContent: 'center', gap: 1.5, minHeight: 56 }}>
                  <img src="https://cdn-icons-png.flaticon.com/512/3135/3135781.png" alt="Foco no cliente" style={{ height: 32, marginRight: 8 }} />
                  <Typography variant="h6" fontWeight={800} sx={{ color: '#fff', fontSize: { xs: 16, md: 18 } }}>Atendimento humanizado</Typography>
                </Box>
              </Grid>
            </Grid>
            <Box sx={{ display: 'flex', flexDirection: { xs: 'column', sm: 'row' }, justifyContent: 'center', gap: 2, mt: 3 }}>
              <Link href="#planos" passHref legacyBehavior>
                <Button variant="contained" color="secondary" size="large" sx={{ px: 7, py: 2.5, fontWeight: 800, fontSize: 20, borderRadius: 3, boxShadow: 4 }}>
                  Veja planos e valores
                </Button>
              </Link>
              <Link href="#plataforma" passHref legacyBehavior>
                <Button variant="outlined" color="inherit" size="large" sx={{ px: 5, py: 2.5, fontWeight: 800, fontSize: 18, borderRadius: 3, boxShadow: 2, border: '2px solid #fff', color: '#fff', '&:hover': { bgcolor: '#fff', color: 'primary.main' } }}>
                  Conheça a Plataforma
                </Button>
              </Link>
            </Box>
          </motion.div>
        </Container>
      </Box>

  {/* ...existing code... */}

      {/* PLATAFORMA EXCLUSIVA DE AUDITORIA E GESTÃO */}
      <Box id="plataforma" sx={{ background: 'linear-gradient(120deg, #1976d2 60%, #0d47a1 100%)', color: 'white', py: 10, boxShadow: 8 }}>
        <Container maxWidth="lg">
          <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.5 }} transition={{ duration: 0.7 }}>
            <Typography variant="h4" fontWeight={900} align="center" sx={{ mb: 3, letterSpacing: 1, textShadow: '0 2px 12px #000a' }}>
              💎 Plataforma <span style={{ color: '#ffe082' }}>AUDITORIA360</span> – Nosso Diferencial
            </Typography>
            <Typography variant="h6" align="center" sx={{ mb: 4, opacity: 0.95, fontWeight: 500 }}>
              A AUDITORIA360 é uma plataforma exclusiva da DPEIXER que une auditoria digital, gestão inteligente e compliance automatizado.
            </Typography>
            <Grid container spacing={4} justifyContent="center">
              <Grid item xs={12} md={6}>
                <ul style={{ fontSize: 18, lineHeight: 1.7, color: '#fff', marginBottom: 0 }}>
                  <li>📊 Dashboards em tempo real com indicadores de folha e RH</li>
                  <li>✅ Alertas automáticos de conformidade (obrigações, prazos e riscos)</li>
                  <li>🔒 Segurança e LGPD garantida com protocolos avançados de proteção</li>
                  <li>🤝 Integração com sistemas contábeis e folha de pagamento</li>
                  <li>📥 Upload seguro de documentos e histórico digital organizado</li>
                  <li>⚡ Economia de tempo com tarefas repetitivas automatizadas</li>
                </ul>
              </Grid>
              <Grid item xs={12} md={6} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <img src="/logo.png" alt="Plataforma AUDITORIA360" style={{ maxHeight: 120, maxWidth: '100%', filter: 'drop-shadow(0 2px 12px #000a)' }} />
              </Grid>
            </Grid>
            <Box sx={{ textAlign: 'center', mt: 4 }}>
              <Link href="/plataforma" passHref legacyBehavior>
                <Button variant="contained" color="secondary" size="large" sx={{ px: 7, py: 2.5, fontWeight: 800, fontSize: 20, borderRadius: 3, boxShadow: 4 }}>
                  Conheça a Plataforma
                </Button>
              </Link>
            </Box>
          </motion.div>
        </Container>
      </Box>

      {/* DIFERENCIAIS DPEIXER */}
      <Box sx={{ background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', py: 8 }}>
        <Container maxWidth="lg">
          <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.5 }} transition={{ duration: 0.7 }}>
            <Typography variant="h4" fontWeight={900} color="primary" align="center" sx={{ mb: 5, letterSpacing: 1 }}>
              ⚖️ Diferenciais DPEIXER
            </Typography>
            <Grid container spacing={4} justifyContent="center">
              <Grid item xs={12} md={6}>
                <ul style={{ fontSize: 17, lineHeight: 1.7, color: '#1976d2', marginBottom: 0 }}>
                  <li>SLA de atendimento garantido em até 48 horas úteis</li>
                  <li>Conformidade 100% com legislação trabalhista e LGPD</li>
                  <li>Plataforma AUDITORIA360 exclusiva</li>
                  <li>Redução de custos operacionais com terceirização especializada</li>
                  <li>Transparência total nos processos e relatórios detalhados</li>
                  <li>Atendimento humanizado + suporte digital</li>
                  <li>Descontos progressivos para grandes volumes</li>
                </ul>
              </Grid>
              <Grid item xs={12} md={6} sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                <img src="https://cdn-icons-png.flaticon.com/512/3135/3135789.png" alt="Diferenciais" style={{ maxHeight: 120, maxWidth: '100%' }} />
              </Grid>
            </Grid>
          </motion.div>
        </Container>
      </Box>







      {/* Como funciona na prática? (único bloco de etapas) */}
      <Box sx={{ background: 'linear-gradient(120deg, #e3f2fd 60%, #fff 100%)', py: 8 }}>
        <Container maxWidth="lg">
          <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.5 }} transition={{ duration: 0.7 }}>
            <Typography variant="h4" fontWeight={900} color="primary" align="center" sx={{ mb: 6, letterSpacing: 1 }}>
              🚀 Como funciona na prática?
            </Typography>
            <Grid container spacing={4} justifyContent="center">
              {[
                { n: 1, title: 'Diagnóstico', desc: 'Análise dos processos atuais, necessidades e oportunidades.' },
                { n: 2, title: 'Implantação', desc: 'Migração de dados, parametrização, treinamento.' },
                { n: 3, title: 'Gestão mensal', desc: 'Processamento da folha, obrigações e suporte contínuo.' },
                { n: 4, title: 'Auditoria e evolução', desc: 'Acompanhamento de indicadores e melhorias contínuas.' },
              ].map((etapa, idx) => (
                <Grid item xs={12} md={3} key={etapa.n}>
                  <motion.div
                    initial={{ opacity: 0, y: 40 }}
                    whileInView={{ opacity: 1, y: 0 }}
                    viewport={{ once: true, amount: 0.4 }}
                    transition={{ duration: 0.6, delay: idx * 0.15 }}
                  >
                    <Card sx={{ p: 3, borderRadius: 4, boxShadow: 4, background: '#fff', minHeight: 180, textAlign: 'center' }}>
                      <Typography variant="h3" color="primary" fontWeight={900}>{etapa.n}</Typography>
                      <Typography variant="h6" fontWeight={700} gutterBottom>{etapa.title}</Typography>
                      <Typography variant="body2">{etapa.desc}</Typography>
                    </Card>
                  </motion.div>
                </Grid>
              ))}
            </Grid>
          </motion.div>
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
          <motion.div initial={{ opacity: 0, y: 40 }} whileInView={{ opacity: 1, y: 0 }} viewport={{ once: true, amount: 0.5 }} transition={{ duration: 0.7 }}>
            <Typography variant="h4" fontWeight={900} color="primary" align="center" gutterBottom sx={{ letterSpacing: 1, textShadow: '0 2px 8px #90caf9' }}>
              🛠️ Nossos Serviços
            </Typography>
            <Typography variant="h6" color="secondary" align="center" sx={{ mt: 2, mb: 4, fontWeight: 700 }}>
              Soluções completas para empresas de todos os portes e escritórios contábeis
            </Typography>
            <Grid container spacing={4} justifyContent="center">
              {/* BPO de RH */}
              <Grid item xs={12} md={6} lg={3}>
                <Card sx={{ p: 0, borderRadius: 4, boxShadow: 8, background: 'linear-gradient(120deg, #e3f2fd 60%, #fff 100%)', border: '2px solid #1976d2', minHeight: 380, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', overflow: 'hidden' }}>
                  <Box sx={{ height: 120, width: '100%', overflow: 'hidden', mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#fff' }}>
                    <img src="/workspaces/AUDITORIA360/public/pexels-olly-3771836.jpg" alt="BPO de RH" style={{ height: 80 }} />
                  </Box>
                  <Box sx={{ p: 3 }}>
                    <Typography variant="h6" fontWeight={900} color="primary" gutterBottom>BPO de Recursos Humanos</Typography>
                    <ul style={{ paddingLeft: 20, margin: 0, fontSize: 15 }}>
                      <li>Admissões e rescisões digitais (100% online e com assinatura eletrônica)</li>
                      <li>Gestão completa do ponto eletrônico e controle de jornada</li>
                      <li>Administração de benefícios (vale-transporte, alimentação, saúde, etc.)</li>
                      <li>Gestão de férias e afastamentos</li>
                      <li>Homologações por videoconferência</li>
                      <li>Portal do empregado com autoatendimento e relatórios gerenciais</li>
                      <li>Relatórios estratégicos e indicadores de desempenho (People Analytics)</li>
                    </ul>
                  </Box>
                </Card>
              </Grid>
              {/* DP Terceirizado */}
              <Grid item xs={12} md={6} lg={3}>
                <Card sx={{ p: 0, borderRadius: 4, boxShadow: 8, background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', border: '2px solid #1976d2', minHeight: 380, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', overflow: 'hidden' }}>
                  <Box sx={{ height: 120, width: '100%', overflow: 'hidden', mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#fff' }}>
                    <img src="/workspaces/AUDITORIA360/public/pexels-campaign-creators-1181406.jpg" alt="DP Terceirizado" style={{ height: 80 }} />
                  </Box>
                  <Box sx={{ p: 3 }}>
                    <Typography variant="h6" fontWeight={900} color="primary" gutterBottom>Departamento Pessoal Terceirizado</Typography>
                    <ul style={{ paddingLeft: 20, margin: 0, fontSize: 15 }}>
                      <li>Cálculo e processamento da folha de pagamento</li>
                      <li>Emissão de guias de encargos (INSS, FGTS, IRRF etc.)</li>
                      <li>Integração completa com o eSocial</li>
                      <li>Administração de férias, 13º salário e rescisões contratuais</li>
                      <li>Entrega de obrigações acessórias trabalhistas</li>
                      <li>Cumprimento rigoroso da LGPD (proteção de dados)</li>
                      <li>Suporte completo e seguro para o RH interno ou escritório contábil</li>
                    </ul>
                  </Box>
                </Card>
              </Grid>
              {/* Consultoria e Assessoria */}
              <Grid item xs={12} md={6} lg={3}>
                <Card sx={{ p: 0, borderRadius: 4, boxShadow: 8, background: 'linear-gradient(120deg, #e3f2fd 60%, #fff 100%)', border: '2px solid #1976d2', minHeight: 380, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', overflow: 'hidden' }}>
                  <Box sx={{ height: 120, width: '100%', overflow: 'hidden', mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#fff' }}>
                    <img src="/workspaces/AUDITORIA360/public/pexels-rio-lecatompessy-3033831.jpg" alt="Consultoria e Assessoria" style={{ height: 80 }} />
                  </Box>
                  <Box sx={{ p: 3 }}>
                    <Typography variant="h6" fontWeight={900} color="primary" gutterBottom>Consultoria e Assessoria Trabalhista</Typography>
                    <ul style={{ paddingLeft: 20, margin: 0, fontSize: 15 }}>
                      <li>Auditoria completa de processos de RH e DP</li>
                      <li>Diagnóstico de passivos trabalhistas e previdenciários</li>
                      <li>Adequação à legislação vigente e normas do eSocial</li>
                      <li>Consultoria estratégica para escritórios contábeis e empresas</li>
                      <li>Treinamentos personalizados para equipes de RH e gestores</li>
                      <li>Planejamento e implementação de melhorias de processos</li>
                    </ul>
                  </Box>
                </Card>
              </Grid>
              {/* Serviços Sob Demanda */}
              <Grid item xs={12} md={6} lg={3}>
                <Card sx={{ p: 0, borderRadius: 4, boxShadow: 8, background: 'linear-gradient(120deg, #fff 60%, #e3f2fd 100%)', border: '2px solid #1976d2', minHeight: 380, display: 'flex', flexDirection: 'column', justifyContent: 'flex-start', overflow: 'hidden' }}>
                  <Box sx={{ height: 120, width: '100%', overflow: 'hidden', mb: 2, display: 'flex', alignItems: 'center', justifyContent: 'center', bgcolor: '#fff' }}>
                    <img src="/logo.png" alt="Serviços Sob Demanda" style={{ height: 80 }} />
                  </Box>
                  <Box sx={{ p: 3 }}>
                    <Typography variant="h6" fontWeight={900} color="primary" gutterBottom>Serviços Sob Demanda</Typography>
                    <ul style={{ paddingLeft: 20, margin: 0, fontSize: 15 }}>
                      <li>Regularizações específicas (CAGED, RAIS, DIRF etc.)</li>
                      <li>Apoio em fiscalizações e autos de infração</li>
                      <li>Elaboração e revisão de contratos e documentos trabalhistas</li>
                      <li>Recrutamento e Seleção sob demanda</li>
                      <li>Projetos de transformação digital em RH e DP</li>
                    </ul>
                  </Box>
                </Card>
              </Grid>
            </Grid>
            <Typography variant="caption" color="text.secondary" align="center" display="block" sx={{ mt: 3 }}>
              *Valores base para empresas até 10 colaboradores. Consulte condições para outros portes e serviços personalizados.
            </Typography>
          </motion.div>
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
          <Typography variant="h5" color="secondary" align="center" sx={{ mb: 4, fontWeight: 700 }}>
            BPO de RH
          </Typography>
          <Box sx={{ overflowX: 'auto', mb: 4 }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: 8, boxShadow: '0 2px 12px #90caf933', marginBottom: 24 }}>
              <thead>
                <tr style={{ background: '#e3f2fd' }}>
                  <th style={{ padding: 16, fontWeight: 900, fontSize: 18, color: '#1976d2', borderBottom: '2px solid #1976d2' }}>Plano</th>
                  <th style={{ padding: 16, fontWeight: 900, fontSize: 18, color: '#1976d2', borderBottom: '2px solid #1976d2' }}>Valor</th>
                  <th style={{ padding: 16, fontWeight: 900, fontSize: 18, color: '#1976d2', borderBottom: '2px solid #1976d2' }}>Principais Recursos</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style={{ padding: 14, fontWeight: 700 }}>Plus RH</td>
                  <td style={{ padding: 14 }}>R$ 39,90/vida</td>
                  <td style={{ padding: 14 }}>Gestão de ponto, férias, benefícios, portal do empregado.</td>
                </tr>
                <tr style={{ background: '#f5faff' }}>
                  <td style={{ padding: 14, fontWeight: 700 }}>Premium RH</td>
                  <td style={{ padding: 14 }}>R$ 49,90/vida</td>
                  <td style={{ padding: 14 }}>Tudo do Plus + admissões e rescisões digitais.</td>
                </tr>
                <tr>
                  <td style={{ padding: 14, fontWeight: 700 }}>Diamante RH</td>
                  <td style={{ padding: 14 }}>R$ 69,90/vida</td>
                  <td style={{ padding: 14 }}>Tudo do Premium + documentação personalizada, reuniões estratégicas, people analytics.</td>
                </tr>
                <tr style={{ background: '#f5faff' }}>
                  <td colSpan={3} style={{ padding: 14, fontWeight: 600, color: '#1976d2', textAlign: 'center' }}>
                    Valores progressivos: descontos de até 6% por volume de colaboradores.
                  </td>
                </tr>
              </tbody>
            </table>
          </Box>
          <Typography variant="h5" color="secondary" align="center" sx={{ mb: 4, fontWeight: 700 }}>
            Terceirização de DP
          </Typography>
          <Box sx={{ overflowX: 'auto', mb: 2 }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', background: '#fff', borderRadius: 8, boxShadow: '0 2px 12px #90caf933', marginBottom: 24 }}>
              <thead>
                <tr style={{ background: '#e3f2fd' }}>
                  <th style={{ padding: 16, fontWeight: 900, fontSize: 18, color: '#1976d2', borderBottom: '2px solid #1976d2' }}>Categoria</th>
                  <th style={{ padding: 16, fontWeight: 900, fontSize: 18, color: '#1976d2', borderBottom: '2px solid #1976d2' }}>Valor</th>
                  <th style={{ padding: 16, fontWeight: 900, fontSize: 18, color: '#1976d2', borderBottom: '2px solid #1976d2' }}>Observações</th>
                </tr>
              </thead>
              <tbody>
                <tr>
                  <td style={{ padding: 14, fontWeight: 700 }}>Funcionários (Simples Nacional)</td>
                  <td style={{ padding: 14 }}>R$ 23,00/vida</td>
                  <td style={{ padding: 14 }}>Folha, encargos, obrigações, eSocial, atendimento.</td>
                </tr>
                <tr style={{ background: '#f5faff' }}>
                  <td style={{ padding: 14, fontWeight: 700 }}>Professores / alocação de custos</td>
                  <td style={{ padding: 14 }}>R$ 25,00/vida</td>
                  <td style={{ padding: 14 }}>Gestão diferenciada, múltiplos vínculos.</td>
                </tr>
                <tr>
                  <td style={{ padding: 14, fontWeight: 700 }}>Pró-labore</td>
                  <td style={{ padding: 14 }}>R$ 18,00/vida</td>
                  <td style={{ padding: 14 }}>Processamento mensal, obrigações acessórias.</td>
                </tr>
                <tr style={{ background: '#f5faff' }}>
                  <td style={{ padding: 14, fontWeight: 700 }}>Admissão/rescisão extra</td>
                  <td style={{ padding: 14 }}>R$ 10,00</td>
                  <td style={{ padding: 14 }}>Por evento adicional ao pacote.</td>
                </tr>
                <tr>
                  <td style={{ padding: 14, fontWeight: 700 }}>Recálculo de guias</td>
                  <td style={{ padding: 14 }}>a partir de R$ 15,00</td>
                  <td style={{ padding: 14 }}>Por demanda, conforme complexidade.</td>
                </tr>
                <tr style={{ background: '#f5faff' }}>
                  <td colSpan={3} style={{ padding: 14, fontWeight: 600, color: '#1976d2', textAlign: 'center' }}>
                    Consultoria mensal gratuita até 100 vidas.
                  </td>
                </tr>
              </tbody>
            </table>
          </Box>
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

      {/* Footer institucional escuro */}
      <Box component="footer" sx={{ background: 'linear-gradient(90deg, #0d47a1 60%, #1976d2 100%)', color: '#fff', py: 6, mt: 0, boxShadow: 8 }}>
        <Container maxWidth="lg" sx={{ display: 'flex', flexDirection: { xs: 'column', md: 'row' }, alignItems: { xs: 'flex-start', md: 'center' }, justifyContent: 'space-between', gap: 4 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: { xs: 2, md: 0 } }}>
            <img src="/logo.png" alt="Logo DPEIXER" style={{ height: 48, marginRight: 16, filter: 'drop-shadow(0 2px 8px #0006)' }} />
            <Box>
              <Typography variant="h6" fontWeight={900} sx={{ letterSpacing: 1 }}>DPEIXER</Typography>
              <Typography variant="caption" sx={{ color: '#fff', opacity: 0.85, fontWeight: 500, letterSpacing: 1 }}>
                BPO de RH, Folha, Consultoria e Tecnologia
              </Typography>
            </Box>
          </Box>
          <Box sx={{ display: 'flex', flexDirection: 'column', gap: 1 }}>
            <Typography variant="body2" sx={{ fontWeight: 700 }}>Contato</Typography>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <PhoneIcon fontSize="small" sx={{ mr: 0.5 }} />
              <a href="tel:+5547933835427" style={{ color: '#fff', textDecoration: 'none', fontWeight: 700 }}>(47) 93383-5427</a>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <WhatsAppIcon fontSize="small" sx={{ color: '#25d366' }} />
              <a href="https://wa.link/vbonkz" target="_blank" rel="noopener" style={{ color: '#fff', textDecoration: 'none', fontWeight: 700 }}>WhatsApp</a>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <InstagramIcon fontSize="small" />
              <a href="https://www.instagram.com/dpeixer_assessoria?igsh=MTF4dXRoODdseDJ0aw%3D%3D&utm_source=qr" target="_blank" rel="noopener" style={{ color: '#fff', textDecoration: 'none', fontWeight: 700 }}>Instagram</a>
            </Box>
            <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <LinkedInIcon fontSize="small" />
              <a href="https://www.linkedin.com/company/dpeixer-assessoria-terceiriza%C3%A7%C3%A3o/about/?viewAsMember=true" target="_blank" rel="noopener" style={{ color: '#fff', textDecoration: 'none', fontWeight: 700 }}>LinkedIn</a>
            </Box>
          </Box>
          <Box sx={{ textAlign: { xs: 'left', md: 'right' }, mt: { xs: 3, md: 0 } }}>
            <Typography variant="body2" sx={{ fontWeight: 700, mb: 1 }}>Endereço</Typography>
            <Typography variant="body2">Atendimento nacional remoto<br />Base: Joinville/SC</Typography>
            <Typography variant="caption" sx={{ color: '#fff', opacity: 0.7, mt: 1, display: 'block' }}>
              &copy; {new Date().getFullYear()} DPEIXER. Todos os direitos reservados.
            </Typography>
          </Box>
        </Container>
      </Box>
    </>
  );
};

export default HomePage;
