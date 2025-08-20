#!/bin/bash
# Script para preparar ambiente Node.js e PM2 no servidor

# Instalar Node.js (caso não esteja instalado)
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt-get install -y nodejs

# Instalar PM2 globalmente
sudo npm install -g pm2

# Criar diretório do app (ajuste o caminho se necessário)
mkdir -p /home/dpeixera6e7dea56/auditoria360
chown $USER:$USER /home/dpeixera6e7dea56/auditoria360

# Exemplo de comando para rodar o app (depois do deploy):
# cd /home/dpeixera6e7dea56/auditoria360
# pm2 start npm --name auditoria360 -- run start
