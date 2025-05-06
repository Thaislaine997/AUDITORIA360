# Dockerfile

# Use a imagem base oficial do Python correspondente ao seu ambiente de execução
FROM python:3.10-slim

# Define o diretório de trabalho no contêiner
WORKDIR /app

# Copia o arquivo de dependências primeiro (para aproveitar o cache do Docker)
COPY requirements.txt .

# Instala as dependências
RUN pip install --no-cache-dir -r requirements.txt

# Copia todo o conteúdo do diretório 'src' local para o diretório 'src' dentro de /app no contêiner
# Isso garante que seus módulos Python e config.json estejam disponíveis em /app/src/
COPY src/ ./src/

# Define a variável de ambiente PORT (o Functions Framework espera isso)
ENV PORT 8080

# Expõe a porta que o contêiner estará ouvindo
EXPOSE 8080

# Comando para iniciar o Functions Framework
# --source aponta para o arquivo de entrada DENTRO do diretório src no contêiner
# --target é o nome da sua função de ponto de entrada nesse arquivo
CMD ["functions-framework", "--source=src/docai_utils.py", "--target=cloud_function_entry_point", "--port=8080"]