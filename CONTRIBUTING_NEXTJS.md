# Guia de Contribuição - AUDITORIA360

## 🚀 Começando

### Pré-requisitos

- Node.js >= 18.0.0
- npm ou yarn
- Git
- Conta no Supabase (para desenvolvimento)

### Configuração do Ambiente

1. **Clone o repositório**
```bash
git clone https://github.com/Thaislaine997/AUDITORIA360.git
cd AUDITORIA360
```

2. **Instale as dependências**
```bash
npm install
```

3. **Configure variáveis de ambiente**
```bash
cp .env.example .env.local
```
Edite `.env.local` com suas credenciais Supabase.

4. **Execute em desenvolvimento**
```bash
npm run dev
```

## 🏗️ Arquitetura

### Estrutura do Projeto

```
AUDITORIA360/
├── pages/                    # Páginas Next.js
│   ├── index.tsx            # Homepage institucional
│   ├── login.tsx            # Página de login
│   ├── dashboard.tsx        # Dashboard protegido
│   └── _app.tsx             # App wrapper
├── components/              # Componentes React
│   ├── ui/                  # Componentes base (Button, Loading, etc)
│   └── layout/              # Layouts (Header, Footer, etc)
├── lib/                     # Utilities e integrações
│   └── supabaseClient.ts    # Cliente Supabase
├── styles/                  # CSS e Tailwind
├── public/                  # Assets estáticos
└── .github/                 # GitHub Actions e templates
```

### Stack Tecnológica

- **Framework**: Next.js 14 (App Router)
- **Styling**: Tailwind CSS
- **Auth/DB**: Supabase
- **TypeScript**: Para type safety
- **Deploy**: GitHub Pages via Actions

## 📝 Padrões de Código

### TypeScript

- Use TypeScript em todos os arquivos `.ts` e `.tsx`
- Defina interfaces para props de componentes
- Use type safety sempre que possível

```typescript
interface ComponentProps {
  title: string
  isLoading?: boolean
  onSubmit: (data: FormData) => void
}
```

### Componentes React

- Componentes funcionais com hooks
- Props desestruturadas
- Export default para componentes principais

```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary'
  children: ReactNode
}

export default function Button({ variant = 'primary', children }: ButtonProps) {
  return <button className={`btn-${variant}`}>{children}</button>
}
```

### Styling com Tailwind

- Use classes utilitárias do Tailwind
- Evite CSS customizado quando possível
- Use a configuração de cores do tema

```typescript
<div className="bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700">
  Conteúdo
</div>
```

### Estrutura de Páginas Next.js

```typescript
import Head from 'next/head'
import Layout from '../components/layout/Layout'

export default function MyPage() {
  return (
    <>
      <Head>
        <title>Título da Página - AUDITORIA360</title>
        <meta name="description" content="Descrição da página" />
      </Head>
      <Layout>
        <div className="container mx-auto px-4">
          {/* Conteúdo da página */}
        </div>
      </Layout>
    </>
  )
}
```

## 🔐 Integração com Supabase

### Autenticação

```typescript
import { authHelpers } from '../lib/supabaseClient'

// Login
const { data, error } = await authHelpers.signIn(email, password)

// Logout  
await authHelpers.signOut()

// Verificar usuário atual
const user = await authHelpers.getCurrentUser()
```

### Rotas Protegidas

```typescript
useEffect(() => {
  const checkUser = async () => {
    const user = await authHelpers.getCurrentUser()
    if (!user) {
      router.push('/login')
    }
  }
  checkUser()
}, [router])
```

## 📋 Fluxo de Contribuição

### 1. Issues

- Verifique issues existentes antes de criar uma nova
- Use os templates de issue disponíveis
- Seja específico na descrição do problema ou feature

### 2. Branches

```bash
# Para bugs
git checkout -b fix/descricao-do-bug

# Para features
git checkout -b feature/nome-da-feature

# Para documentação
git checkout -b docs/atualizacao-documentacao
```

### 3. Commits

Use conventional commits:

```bash
git commit -m "feat: adiciona página de dashboard"
git commit -m "fix: corrige problema de autenticação"
git commit -m "docs: atualiza guia de instalação"
```

### 4. Pull Requests

- Use o template de PR
- Inclua screenshots para mudanças visuais
- Descreva o que foi implementado
- Marque reviewers relevantes

## 🧪 Testes

### Executar Testes

```bash
# Testes unitários
npm test

# Testes com coverage
npm run test:coverage

# Build de produção (teste de build)
npm run build
```

### Escrever Testes

```typescript
import { render, screen } from '@testing-library/react'
import Button from '../components/ui/Button'

describe('Button Component', () => {
  it('renders correctly', () => {
    render(<Button>Click me</Button>)
    expect(screen.getByText('Click me')).toBeInTheDocument()
  })
})
```

## 🚀 Deploy

### GitHub Pages

O deploy é automático via GitHub Actions:

1. Push para `main` ou `Principal`
2. GitHub Actions executa build
3. Deploy automático no GitHub Pages

### Configuração Local

```bash
# Build de produção
npm run build

# Testar build localmente
npm start
```

## 📚 Recursos Úteis

### Documentação

- [Next.js Docs](https://nextjs.org/docs)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [Supabase Docs](https://supabase.com/docs)
- [TypeScript Handbook](https://www.typescriptlang.org/docs/)

### Ferramentas de Desenvolvimento

- VS Code com extensões:
  - TypeScript
  - Tailwind CSS IntelliSense
  - ES7+ React/Redux/React-Native snippets

## 🤝 Comunidade

### Obtendo Ajuda

- 🐛 **Bugs**: Abra uma issue usando o template
- 💡 **Features**: Discuta primeiro em uma issue
- ❓ **Dúvidas**: Use as discussions do GitHub

### Code Review

- Seja construtivo nos comentários
- Explique o "porquê", não apenas o "o que"
- Sugira melhorias, não apenas critique

## ⚡ Comandos Rápidos

```bash
# Desenvolvimento
npm run dev          # Servidor de desenvolvimento
npm run build        # Build de produção
npm run lint         # Verificar código
npm run format       # Formatar código

# Testes
npm test            # Executar testes
npm run test:watch  # Testes em watch mode

# Deploy
git push origin main  # Trigger deploy automático
```

---

**Obrigado por contribuir com o AUDITORIA360! 🚀**