import os
from services.storage_utils import upload_arquivo, download_arquivo

# Exemplo de upload para o R2
print('Enviando arquivo de exemplo para o R2...')
# Crie um arquivo de teste
with open('arquivo_teste.txt', 'w') as f:
    f.write('Conteúdo de teste para upload no R2!')

upload_arquivo('arquivo_teste.txt', 'arquivo_teste.txt')
print('Upload concluído!')

# Exemplo de download do R2
print('Baixando arquivo de exemplo do R2...')
download_arquivo('arquivo_teste.txt', 'arquivo_teste_baixado.txt')
print('Download concluído!')

# Verifica conteúdo
with open('arquivo_teste_baixado.txt') as f:
    print('Conteúdo baixado:', f.read())
