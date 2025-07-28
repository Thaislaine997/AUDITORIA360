# GUIA DO DESIGN SYSTEM AUDITORIA360 v3.0

## 📋 Visão Geral
Este documento apresenta o novo Design System do AUDITORIA360, com componentes modernos, responsivos e acessíveis.

## 🎨 Paleta de Cores

### Cores Primárias
- `--primary-color: #00D4FF` - Ciano vibrante (cor principal da logo)
- `--secondary-color: #0ea5e9` - Azul complementar
- `--accent-color: #22d3ee` - Cor de destaque

### Cores de Fundo
- `--background-color: #0A0D1F` - Fundo principal (azul escuro)
- `--secondary-background-color: #1E2242` - Fundo secundário (cards)
- `--surface-color: #2a2f54` - Superfícies elevadas

### Cores de Estado
- `--success-color: #22c55e` - Verde (sucesso)
- `--warning-color: #facc15` - Amarelo (aviso)
- `--danger-color: #ef4444` - Vermelho (erro)
- `--info-color: #22d3ee` - Azul (informação)

## 🧩 Componentes Disponíveis

### 1. Cards
```html
<!-- Card Básico -->
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Título do Card</h3>
        <p class="card-subtitle">Subtítulo opcional</p>
    </div>
    <div class="card-body">
        <p>Conteúdo do card...</p>
    </div>
</div>

<!-- Card com Efeito Glass -->
<div class="card card-glass">
    <div class="card-body">
        <p>Card com efeito vidro moderno</p>
    </div>
</div>
```

### 2. Botões
```html
<!-- Botões com diferentes estilos -->
<button class="button button-primary">Primário</button>
<button class="button button-secondary">Secundário</button>
<button class="button button-outline">Outline</button>
<button class="button button-success">Sucesso</button>
<button class="button button-warning">Aviso</button>
<button class="button button-danger">Perigo</button>

<!-- Tamanhos -->
<button class="button button-primary button-sm">Pequeno</button>
<button class="button button-primary">Normal</button>
<button class="button button-primary button-lg">Grande</button>
```

### 3. Badges
```html
<span class="badge badge-primary">Primary</span>
<span class="badge badge-success">Success</span>
<span class="badge badge-warning">Warning</span>
<span class="badge badge-danger">Danger</span>
<span class="badge badge-info">Info</span>
```

### 4. Alertas
```html
<div class="alert alert-success">Operação realizada com sucesso!</div>
<div class="alert alert-warning">Atenção: verifique os dados.</div>
<div class="alert alert-danger">Erro: falha na operação.</div>
<div class="alert alert-info">Informação importante.</div>
```

### 5. Layout e Containers
```html
<!-- Container principal -->
<div class="container">
    <div class="section">
        <!-- Seção com espaçamento -->
    </div>
</div>

<!-- Grid responsivo -->
<div class="grid grid-2">
    <div>Item 1</div>
    <div>Item 2</div>
</div>

<div class="grid grid-3">
    <div>Item 1</div>
    <div>Item 2</div>
    <div>Item 3</div>
</div>

<!-- Flexbox -->
<div class="flex items-center justify-between gap-md">
    <div>Esquerda</div>
    <div>Direita</div>
</div>
```

### 6. Formulários
```html
<div class="form-group">
    <label class="form-label">Label do Campo</label>
    <input type="text" class="form-input" placeholder="Digite aqui...">
</div>

<div class="form-group">
    <label class="form-label">Seleção</label>
    <select class="form-input form-select">
        <option>Opção 1</option>
        <option>Opção 2</option>
    </select>
</div>
```

## 🔧 Como Usar no Streamlit

### Carregamento do CSS
```python
import streamlit as st
import os

def load_css():
    css_path = os.path.join("assets", "style.css")
    if os.path.exists(css_path):
        with open(css_path) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# Chamar no início da página
load_css()
```

### Logo no Header
```python
def load_logo():
    logo_path = "assets/logo.png"
    if os.path.exists(logo_path):
        import base64
        with open(logo_path, "rb") as img_file:
            b64_img = base64.b64encode(img_file.read()).decode()
        st.markdown(f'''
            <div class="header">
                <img src="data:image/png;base64,{b64_img}" 
                     alt="Logo AUDITORIA360" class="logo"/>
                <h1 class="header-title">AUDITORIA360</h1>
            </div>
        ''', unsafe_allow_html=True)
```

### Usando Componentes
```python
# Card personalizado
st.markdown('''
<div class="card">
    <div class="card-header">
        <h3 class="card-title">Métricas Importantes</h3>
    </div>
    <div class="card-body">
        <p>Conteúdo das métricas...</p>
    </div>
</div>
''', unsafe_allow_html=True)

# Botões personalizados
st.markdown('''
<div class="flex gap-md">
    <button class="button button-primary">Salvar</button>
    <button class="button button-secondary">Cancelar</button>
</div>
''', unsafe_allow_html=True)
```

## 📱 Responsividade

O design system é totalmente responsivo e se adapta automaticamente a diferentes tamanhos de tela:

- **Desktop**: Layout completo com todos os elementos
- **Tablet**: Grid se adapta para 2 colunas
- **Mobile**: Layout em coluna única, botões em largura total

## 🌙 Modo Escuro

O tema escuro está ativo por padrão e se adapta às preferências do sistema operacional do usuário.

## ♿ Acessibilidade

- Contraste mínimo de 4.5:1 entre texto e fundo
- Focus outline visível para navegação por teclado
- Suporte a leitores de tela
- Suporte a modo de alto contraste

## 🚀 Animações

Todas as animações respeitam as preferências de movimento reduzido do usuário:

```css
.animate-fade-in { animation: fadeIn 0.6s ease-out; }
.animate-slide-in { animation: slideIn 0.5s ease-out; }
.animate-pulse { animation: pulse 2s infinite; }
```

## 📝 Classes Utilitárias

```html
<!-- Espaçamento -->
<div class="mt-1 mb-2 ml-1 mr-1">Margens</div>
<div class="pt-1 pb-2 pl-1 pr-1">Padding</div>

<!-- Texto -->
<div class="text-center">Centralizado</div>
<div class="text-muted">Texto secundário</div>
<div class="text-small">Texto pequeno</div>

<!-- Layout -->
<div class="w-full">Largura total</div>
<div class="hidden">Oculto</div>
<div class="visible">Visível</div>
```

## ✅ Checklist de Implementação

Para usar o design system em uma nova página:

1. ✅ Carregar o CSS com `load_css()`
2. ✅ Adicionar o logo com `load_logo()`
3. ✅ Usar containers `.container` e `.section`
4. ✅ Aplicar classes de componentes apropriadas
5. ✅ Testar em diferentes dispositivos
6. ✅ Verificar acessibilidade e contraste
7. ✅ Validar animações e transições

## 🔗 Recursos Adicionais

- **Documentação CSS**: Ver comentários em `assets/style.css`
- **Exemplo Visual**: Executar `/tmp/test_visual_components.py`
- **Suporte**: Abrir issue no repositório para dúvidas

---

**AUDITORIA360 Design System v3.0** - Moderno, Acessível e Profissional 🚀