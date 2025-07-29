import asyncio

from google.cloud import bigquery


# Mock do cliente BigQuery para propósitos de teste
class MockBigQueryClient:
    def query(self, query):
        print(f"Executando consulta: {query}")

        class Result:
            def __init__(self, rows):
                self.rows = rows

            def result(self):
                return iter(self.rows)

        return Result(
            [
                # Adicione aqui linhas de teste conforme necessário
            ]
        )


bq_client = MockBigQueryClient()


async def main():
    # 1. Buscar uma CCT com status 'PENDENTE_EXTRACAO'
    query = f"""
        SELECT id_cct_documento, gcs_uri_documento, id_cliente_principal_associado, data_inicio_vigencia
        FROM `seu-projeto-gcp.auditoria_folha_dataset.CCTsDocumentos`
        WHERE status_processamento_ia = 'PENDENTE_EXTRACAO'
        LIMIT 1
    """
    result = bq_client.query(query).result()
    row = next(result, None)
    if not row:
        print("Nenhuma CCT com status PENDENTE_EXTRACAO encontrada.")
        return
    id_cct = row.id_cct_documento
    gcs_uri_pdf = row.gcs_uri_documento
    id_cliente = row.id_cliente_principal_associado or "global"
    ano_vigencia = row.data_inicio_vigencia.year if row.data_inicio_vigencia else 2025
    print(f"Processando CCT: {id_cct}\nPDF: {gcs_uri_pdf}")
    # await processar_extracao_texto_cct(id_cct, gcs_uri_pdf, id_cliente, ano_vigencia)
    print("Processo concluído!")


if __name__ == "__main__":
    asyncio.run(main())
