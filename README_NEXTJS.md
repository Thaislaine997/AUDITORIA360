# AUDITORIA360 - Plataforma Moderna de Terceirização de Departamento Pessoal

[![Deploy to GitHub Pages](https://github.com/Thaislaine997/AUDITORIA360/actions/workflows/deploy.yml/badge.svg)](https://github.com/Thaislaine997/AUDITORIA360/actions/workflows/deploy.yml)
![System Status](https://img.shields.io/badge/system-healthy-brightgreen) ![Health](https://img.shields.io/badge/health-100%25-brightgreen)

## 🚀 Visão Geral

AUDITORIA360 é uma plataforma moderna e escalável para terceirização de Departamento Pessoal, desenvolvida com **Next.js** (React) e integração **Supabase** para autenticação e banco de dados. A plataforma oferece deploy automático no **GitHub Pages** e área de login protegida para o portal AUDITORIA360.

### 🏢 DPEIXER - Assessoria & Terceirização

A DPEIXER oferece soluções completas em Departamento Pessoal e Recursos Humanos, voltadas para contabilidades e empresas que buscam:

- ✅ **Precisão** e segurança jurídica
- ✅ **Eficiência operacional**  
- ✅ **Compliance** trabalhista
- ✅ **Processos 100% digitais**

## 🏗️ Arquitetura Moderna

```
AUDITORIA360/
├── 📁 pages/                 # Páginas Next.js (SSG/SSR)
├── 📁 components/            # Componentes React reutilizáveis  
├── 📁 lib/                   # Integrações (Supabase, APIs)
├── 📁 styles/                # CSS global e Tailwind
├── 📁 public/                # Assets estáticos
├── 📁 .github/               # GitHub Actions e templates
│   ├── workflows/            # CI/CD workflows
│   └── ISSUE_TEMPLATE/       # Templates de issues
├── 📄 next.config.js         # Configuração Next.js
├── 📄 tailwind.config.js     # Configuração Tailwind CSS
└── 📄 .env.example           # Variáveis de ambiente
```

### 🔧 Stack Tecnológica

| Componente | Tecnologia | Função |
|------------|------------|---------|
| **Frontend** | Next.js + React + TypeScript | Interface moderna e responsiva |
| **Styling** | Tailwind CSS | Design system e componentes |
| **Auth/DB** | Supabase | Autenticação e banco de dados |
| **Deploy** | GitHub Pages | Hospedagem estática automatizada |
| **CI/CD** | GitHub Actions | Deploy e integração contínua |

## 🚀 Instalação e Desenvolvimento

### Pré-requisitos

- Node.js >= 18.0.0
- npm ou yarn
- Conta Supabase (para auth/DB)

### 1. Clone e Instale

```bash
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360
npm install
```

### 2. Configure Variáveis de Ambiente

```bash
cp .env.example .env.local
```

Edite `.env.local` com suas credenciais Supabase:

```env
NEXT_PUBLIC_SUPABASE_URL=your_supabase_project_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

### 3. Execute em Desenvolvimento

```bash
npm run dev
```

Acesse: `http://localhost:3000`

### 4. Build para Produção

```bash
npm run build
```

## 🔐 Configuração do Supabase

### 1. Criar Projeto

1. Acesse [supabase.com](https://supabase.com)
2. Crie um novo projeto
3. Anote a URL e chave pública (anon key)

### 2. Configurar Autenticação

No painel Supabase:
- Vá em **Authentication > Settings**
- Configure **Site URL**: `https://thaislaine997.github.io`
- Adicione **Redirect URLs**:
  - `http://localhost:3000` (desenvolvimento)
  - `https://thaislaine997.github.io/AUDITORIA360` (produção)

## 🌐 Deploy Automatizado

### GitHub Pages com Actions

O deploy é **100% automatizado** via GitHub Actions:

1. **Push para branch `main` ou `Principal`**
2. **GitHub Actions** executa:
   - Instala dependências
   - Executa build Next.js
   - Gera páginas estáticas
   - Deploy no GitHub Pages

### Configuração de Secrets

No repositório GitHub, configure em **Settings > Secrets**:

```
NEXT_PUBLIC_SUPABASE_URL=your_supabase_url
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
```

## 🎯 Funcionalidades Principais

### 🏠 Site Institucional
- **Hero section** com proposta de valor
- **Sobre a empresa** com diferenciais
- **Serviços detalhados** e técnicos
- **Planos e preços** transparentes
- **Design responsivo** e moderno

### 🔒 Portal AUDITORIA360 (Área Protegida)
- **Login/Registro** com Supabase Auth
- **Dashboard** com métricas e KPIs
- **Módulos integrados**:
  - Controle da Folha Mensal
  - Portal de Demandas
  - Portal de Auditoria
  - Tabelas Oficiais (INSS, FGTS, etc.)
  - Portal CCT
  - Gestão e Relatórios

## 💰 Planos e Valores

| Plano | Valor/Mês | Inclui |
|-------|-----------|---------|
| **Plus** | R$ 39,90 | Folha mensal, eSocial, relatórios básicos |
| **Premium** | R$ 49,90 | Plus + admissões/rescisões + portal básico |
| **Diamante** | R$ 69,90 | Premium + docs personalizados + analytics |

### Diferenciais Inclusos
- 📍 Ponto digital com geolocalização
- 🎫 Gestão automatizada de benefícios (VR/VA/VT)
- ✍️ Assinatura eletrônica integrada
- 🔒 Processos 100% digitais e auditáveis

## 🤝 Contribuição

### Como Contribuir

1. Fork do repositório
2. Criar branch: `git checkout -b feature/nova-funcionalidade`
3. Commit: `git commit -am 'Adiciona nova funcionalidade'`
4. Push: `git push origin feature/nova-funcionalidade`
5. Abrir Pull Request

### Padrões de Código

- ✅ Usar **TypeScript** para type safety
- ✅ Seguir **ESLint** e **Prettier**
- ✅ Componentes funcionais com **hooks**
- ✅ **Tailwind CSS** para estilos
- ✅ Documentar funções públicas

## 📞 Suporte e Contato

- 🌐 **Website**: [thaislaine997.github.io/AUDITORIA360](https://thaislaine997.github.io/AUDITORIA360)
- 📧 **Email**: contato@dpeixer.com.br  
- 📱 **Portal**: Acesse via `/login` para clientes
- 🐛 **Issues**: [GitHub Issues](https://github.com/Thaislaine997/AUDITORIA360/issues)

---

## 📋 Migração Legacy

Esta versão modernizada mantém compatibilidade com o sistema anterior. Os módulos legados estão disponíveis em:

- `src/frontend/` - Interface React/Vite original
- `src/api/` - APIs FastAPI existentes
- `portal_demandas/` - Sistema de gestão de tickets
- `supabase/` - Configurações Supabase existentes

**AUDITORIA360** - Plataforma Moderna de Terceirização de Departamento Pessoal  
*Desenvolvido com ❤️ usando Next.js + Supabase*