# Habilitação de HTTPS para AUDITORIA360

## 🎯 Objetivo

Implementar HTTPS no domínio `dpeixerassessoria.com.br` para garantir comunicação segura entre usuários e a aplicação AUDITORIA360.

## 🔐 Opções de Certificado SSL

### 1. 🆓 Let's Encrypt (Recomendado)

**Vantagens:**
- Gratuito
- Renovação automática
- Amplamente confiável
- Processo automatizado

**Implementação com Certbot:**

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install certbot python3-certbot-nginx

# Gerar certificado para Nginx
sudo certbot --nginx -d dpeixerassessoria.com.br

# Para Apache
sudo apt install certbot python3-certbot-apache
sudo certbot --apache -d dpeixerassessoria.com.br
```

### 2. 💰 Certificado Comercial

**Opções:**
- Comodo SSL
- DigiCert
- GlobalSign
- GoDaddy SSL

**Processo:**
1. Gerar CSR (Certificate Signing Request)
2. Enviar CSR para a CA
3. Validar domínio/organização
4. Instalar certificado no servidor

## ⚙️ Configuração por Servidor Web

### 🌐 Nginx Configuration

Arquivo: `/etc/nginx/sites-available/auditoria360`

```nginx
# Redirect HTTP to HTTPS
server {
    listen 80;
    server_name dpeixerassessoria.com.br www.dpeixerassessoria.com.br;
    return 301 https://dpeixerassessoria.com.br$request_uri;
}

# HTTPS Server Block
server {
    listen 443 ssl http2;
    server_name dpeixerassessoria.com.br;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/dpeixerassessoria.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dpeixerassessoria.com.br/privkey.pem;
    
    # Modern SSL Configuration
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384:ECDHE-RSA-CHACHA20-POLY1305;
    ssl_prefer_server_ciphers off;
    
    # SSL Optimization
    ssl_session_cache shared:SSL:10m;
    ssl_session_timeout 10m;
    ssl_session_tickets off;
    
    # OCSP Stapling
    ssl_stapling on;
    ssl_stapling_verify on;
    ssl_trusted_certificate /etc/letsencrypt/live/dpeixerassessoria.com.br/chain.pem;
    
    # Security Headers
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;
    add_header X-Frame-Options DENY always;
    add_header X-Content-Type-Options nosniff always;
    add_header X-XSS-Protection "1; mode=block" always;
    add_header Referrer-Policy "strict-origin-when-cross-origin" always;

    # Rest of your configuration...
    root /var/www/html/auditoria360;
    index index.html;

    # SPA Configuration
    location / {
        try_files $uri $uri/ /index.html;
    }

    # API Proxy
    location /api/ {
        proxy_pass http://backend:8000;
        proxy_ssl_verify off;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}

# Redirect www to non-www
server {
    listen 443 ssl http2;
    server_name www.dpeixerassessoria.com.br;
    
    ssl_certificate /etc/letsencrypt/live/dpeixerassessoria.com.br/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/dpeixerassessoria.com.br/privkey.pem;
    
    return 301 https://dpeixerassessoria.com.br$request_uri;
}
```

### 🕸️ Apache Configuration

Arquivo: `/etc/apache2/sites-available/auditoria360-ssl.conf`

```apache
<VirtualHost *:80>
    ServerName dpeixerassessoria.com.br
    ServerAlias www.dpeixerassessoria.com.br
    Redirect permanent / https://dpeixerassessoria.com.br/
</VirtualHost>

<VirtualHost *:443>
    ServerName dpeixerassessoria.com.br
    DocumentRoot /var/www/html/auditoria360

    # SSL Configuration
    SSLEngine on
    SSLCertificateFile /etc/letsencrypt/live/dpeixerassessoria.com.br/cert.pem
    SSLCertificateKeyFile /etc/letsencrypt/live/dpeixerassessoria.com.br/privkey.pem
    SSLCertificateChainFile /etc/letsencrypt/live/dpeixerassessoria.com.br/chain.pem

    # Modern SSL Configuration
    SSLProtocol all -SSLv3 -TLSv1 -TLSv1.1
    SSLCipherSuite ECDHE-RSA-AES128-GCM-SHA256:ECDHE-RSA-AES256-GCM-SHA384
    SSLHonorCipherOrder off
    SSLCompression off
    SSLSessionTickets off

    # Security Headers
    Header always set Strict-Transport-Security "max-age=31536000; includeSubDomains; preload"
    Header always set X-Frame-Options DENY
    Header always set X-Content-Type-Options nosniff
    Header always set X-XSS-Protection "1; mode=block"

    # SPA Configuration
    <Directory "/var/www/html/auditoria360">
        RewriteEngine On
        RewriteBase /
        RewriteRule ^index\.html$ - [L]
        RewriteCond %{REQUEST_FILENAME} !-f
        RewriteCond %{REQUEST_FILENAME} !-d
        RewriteRule . /index.html [L]
    </Directory>

    # API Proxy
    ProxyPreserveHost On
    ProxyPass /api/ http://backend:8000/api/
    ProxyPassReverse /api/ http://backend:8000/api/
</VirtualHost>
```

## 🚀 Implementação Passo a Passo

### 1. 📋 Preparação

```bash
# Backup da configuração atual
sudo cp /etc/nginx/sites-available/default /etc/nginx/sites-available/default.backup

# ou para Apache
sudo cp /etc/apache2/sites-available/000-default.conf /etc/apache2/sites-available/000-default.conf.backup
```

### 2. 🔧 Instalação do Certbot

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install snapd
sudo snap install core; sudo snap refresh core
sudo snap install --classic certbot

# Link do certbot
sudo ln -s /snap/bin/certbot /usr/bin/certbot
```

### 3. 🎯 Geração do Certificado

```bash
# Para Nginx
sudo certbot --nginx -d dpeixerassessoria.com.br -d www.dpeixerassessoria.com.br

# Para Apache
sudo certbot --apache -d dpeixerassessoria.com.br -d www.dpeixerassessoria.com.br

# Apenas certificado (configuração manual)
sudo certbot certonly --webroot -w /var/www/html/auditoria360 -d dpeixerassessoria.com.br
```

### 4. ✅ Validação

```bash
# Testar configuração do Nginx
sudo nginx -t
sudo systemctl reload nginx

# Testar configuração do Apache
sudo apache2ctl configtest
sudo systemctl reload apache2

# Verificar SSL
curl -I https://dpeixerassessoria.com.br
openssl s_client -connect dpeixerassessoria.com.br:443 -servername dpeixerassessoria.com.br
```

## 🔄 Renovação Automática

### 📅 Cron Job para Renovação

```bash
# Editar crontab
sudo crontab -e

# Adicionar linha para renovação automática (às 3h da manhã, todo dia 1º do mês)
0 3 1 * * /usr/bin/certbot renew --quiet && systemctl reload nginx

# ou para Apache
0 3 1 * * /usr/bin/certbot renew --quiet && systemctl reload apache2
```

### 🧪 Teste de Renovação

```bash
# Teste seco (dry run)
sudo certbot renew --dry-run

# Forçar renovação para teste
sudo certbot renew --force-renewal
```

## 🔍 Validações Pós-Implementação

### 1. 🌐 Testes de Acesso

- [ ] `http://dpeixerassessoria.com.br` → redireciona para HTTPS
- [ ] `https://dpeixerassessoria.com.br` → carrega corretamente
- [ ] `https://www.dpeixerassessoria.com.br` → redireciona para versão sem www
- [ ] Todas as sub-rotas funcionando via HTTPS

### 2. 🛡️ Verificação de Segurança

```bash
# Teste SSL Labs (online)
# https://www.ssllabs.com/ssltest/analyze.html?d=dpeixerassessoria.com.br

# Teste local
nmap --script ssl-enum-ciphers -p 443 dpeixerassessoria.com.br
```

### 3. 📊 Ferramentas de Validação

- **SSL Labs Test**: https://www.ssllabs.com/ssltest/
- **Security Headers**: https://securityheaders.com/
- **HSTS Preload**: https://hstspreload.org/
- **Certificate Transparency**: https://crt.sh/

## 🆘 Troubleshooting

### ❌ Problemas Comuns

1. **Erro "Connection not secure"**
   - Verificar se certificado foi instalado corretamente
   - Confirmar que não há mixed content (HTTP em página HTTPS)

2. **Erro de renovação automática**
   - Verificar logs: `sudo journalctl -u certbot.timer`
   - Testar manualmente: `sudo certbot renew --dry-run`

3. **Assets não carregam**
   - Verificar se todos os recursos estão com URL HTTPS
   - Atualizar referências no `index.html`

### 📞 Contatos de Suporte

- **Equipe DevOps**: devops@auditoria360.com.br
- **Documentação Let's Encrypt**: https://letsencrypt.org/docs/
- **Suporte 24h**: +55 (11) 99999-9999

---

> **🔒 IMPORTANTE**: Após implementar HTTPS, validar que todos os recursos carregam sem bloqueios de mixed content e que todas as funcionalidades da aplicação continuam operacionais.