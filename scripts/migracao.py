# /scripts/migracao.py
import pdfplumber
import pandas as pd
from supabase import create_client, Client
import os
from dotenv import load_dotenv

# Carrega as variáveis do ficheiro .env para o ambiente
load_dotenv()

# Função para conectar de forma segura ao Supabase
def conectar_supabase() -> Client:
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_SERVICE_KEY")
    if not url or not key:
        raise ValueError("As variáveis de ambiente SUPABASE_URL e SUPABASE_SERVICE_KEY são obrigatórias.")
    return create_client(url, key)

# Função para obter o ID da contabilidade pelo nome ou CNPJ
def obter_id_contabilidade(supabase: Client, cnpj: str) -> int:
    """Busca o ID de uma contabilidade na base de dados a partir do CNPJ."""
    try:
        response = supabase.table('Contabilidades').select('id').eq('cnpj', cnpj).single().execute()
        return response.data['id']
    except Exception as e:
        print(f"Erro ao buscar contabilidade com CNPJ {cnpj}: {e}")
        raise

def extrair_dados_pdf(caminho_pdf: str) -> pd.DataFrame:
    """
    Função principal de extração de dados de um PDF.
    Esta é a parte que você precisa personalizar.
    """
    print(f"A processar o ficheiro: {caminho_pdf}...")
    # --- INÍCIO DA LÓGICA PERSONALIZÁVEL ---
    # Exemplo: Tenta extrair a primeira tabela da primeira página.
    # Você terá que inspecionar os seus PDFs e ajustar esta lógica.
    # pdfplumber é muito poderoso para encontrar tabelas e texto por coordenadas.
    with pdfplumber.open(caminho_pdf) as pdf:
        primeira_pagina = pdf.pages[0]
        tabelas = primeira_pagina.extract_tables()
        if not tabelas:
            print("AVISO: Nenhuma tabela encontrada neste PDF com a lógica atual.")
            return pd.DataFrame()
        
        # Assume que a primeira tabela tem os dados e a primeira linha é o cabeçalho
        df = pd.DataFrame(tabelas[0][1:], columns=tabelas[0][0])
    # --- FIM DA LÓGICA PERSONALIZÁVEL ---
    
    print(f"Extraídas {len(df)} linhas do PDF.")
    return df

def migrar_para_supabase(supabase: Client, df_clientes: pd.DataFrame, id_contabilidade: int):
    """Insere os dados do DataFrame na tabela Empresas do Supabase."""
    if df_clientes.empty:
        print("DataFrame vazio. A saltar a migração para esta contabilidade.")
        return

    print(f"A iniciar a migração de {len(df_clientes)} clientes para a contabilidade ID {id_contabilidade}...")
    
    # Renomeie as colunas do seu DataFrame para corresponderem às da tabela Supabase
    # Exemplo: df_clientes = df_clientes.rename(columns={'NOME DA EMPRESA': 'nome'})
    
    registos_para_inserir = []
    for _, row in df_clientes.iterrows():
        # Verifique se a coluna 'NOME DA EMPRESA' existe no seu DataFrame
        if 'NOME DA EMPRESA' not in row or not row['NOME DA EMPRESA']:
            print(f"AVISO: Linha ignorada por não ter nome de empresa: {row}")
            continue

        registos_para_inserir.append({
            "nome": row['NOME DA EMPRESA'],  # Ajuste o nome da coluna aqui
            "contabilidade_id": id_contabilidade,
            "detalhes_personalizados": {
                # Adicione outros campos do PDF aqui em formato JSON
                "movimentacao_inicial": row.get('MOVIMENTAÇÃO'), # Exemplo
                "origem_pdf": os.path.basename(row.name) if hasattr(row, 'name') else 'N/A'
            }
        })

    if not registos_para_inserir:
        print("Nenhum registo válido para inserir.")
        return

    try:
        data, count = supabase.table('Empresas').insert(registos_para_inserir).execute()
        print(f"Sucesso! {len(data.data)} registos inseridos.")
    except Exception as e:
        print(f"ERRO GERAL ao inserir o lote de dados: {e}")

if __name__ == "__main__":
    supabase_client = conectar_supabase()

    # --- Processo para a DELANE ---
    print("\n----- A PROCESSAR DELANE -----")
    cnpj_delane = '21.391.377/0001-99' # CNPJ da Elaine Cristina
    id_delane = obter_id_contabilidade(supabase_client, cnpj_delane)
    caminho_pdf_delane = 'caminho/para/seu/DELANE_CONTROLE.pdf' # Ajuste o caminho
    df_delane = extrair_dados_pdf(caminho_pdf_delane)
    migrar_para_supabase(supabase_client, df_delane, id_delane)

    # --- Processo para a CKONT ---
    print("\n----- A PROCESSAR CKONT -----")
    cnpj_ckont = '50.215.504/0001-05'
    id_ckont = obter_id_contabilidade(supabase_client, cnpj_ckont)
    caminho_pdf_ckont = 'caminho/para/seu/CKONT_CONTROLE.pdf' # Ajuste o caminho
    df_ckont = extrair_dados_pdf(caminho_pdf_ckont)
    migrar_para_supabase(supabase_client, df_ckont, id_ckont)

    print("\nMigração concluída!")