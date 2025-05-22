# Dockerfile

# Use a imagem base oficial do Python correspondente ao seu ambiente de execução
FROM python:3.10-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Crie um usuário e grupo não-root para executar a aplicação
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Copia o arquivo de dependências primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia o código da aplicação para o diretório de trabalho
# Ajuste se o seu código não estiver todo em 'src/' ou se precisar de outros arquivos da raiz
COPY src/ ./src/
# Se main.py e outros arquivos de nível superior forem necessários, copie-os também:
# COPY main.py . 
# COPY config.py . # Exemplo

# Mude a propriedade dos arquivos da aplicação para o usuário não-root
RUN chown -R appuser:appuser /app

# Mude para o usuário não-root
USER appuser

# Define a variável de ambiente PORT
ENV PORT 8080

# Expõe a porta que o contêiner estará ouvindo
EXPOSE 8080

# Comando para iniciar o servidor Gunicorn
# Garanta que src.main:app está correto e que 'app' é a instância Flask em src/main.py
CMD ["gunicorn", "--bind", "0.0.0.0:8080", "--workers", "1", "--threads", "8", "--timeout", "120", "src.main:app"]