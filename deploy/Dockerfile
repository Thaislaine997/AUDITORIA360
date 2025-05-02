# Usar a imagem base do Python
FROM python:3.11

# Definir o diretório de trabalho dentro do container
WORKDIR /app

# Copiar os arquivos do projeto para o container
COPY . /app

# Instalar as dependências do projeto
RUN pip install --no-cache-dir -r requirements.txt

# Expor a porta usada pelo Streamlit
EXPOSE 8080

# Comando para iniciar a aplicação
CMD ["streamlit", "run", "src/main.py", "--server.port=8080", "--server.address=0.0.0.0"]