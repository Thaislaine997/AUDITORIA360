"""
Serviço para interagir com as tabelas de usuários no BigQuery.
"""
from typing import Optional
from src.utils.bq_executor import BQExecutor
from src.schemas.rbac_schemas import UserInDB
from google.cloud import bigquery

def get_user_by_email(email: str) -> Optional[UserInDB]:
    executor = BQExecutor(dataset_id="Clientes_dataset")
    query = f"""
        SELECT
            u.id_usuario,
            u.id_cliente,
            u.nome,
            u.email,
            u.hashed_password,
            u.ativo,
            ARRAY_AGG(IF(p.id_papel IS NULL, NULL, p.id_papel) IGNORE NULLS) as papeis
        FROM
            `auditoria-folha.Clientes_dataset.Usuarios` u
        LEFT JOIN
            `auditoria-folha.Clientes_dataset.Usuario_Papeis` up ON u.id_usuario = up.id_usuario
        LEFT JOIN
            `auditoria-folha.Clientes_dataset.Papeis` p ON up.id_papel = p.id_papel
        WHERE
            u.email = @email
        GROUP BY 1, 2, 3, 4, 5, 6
        LIMIT 1
    """
    params = [bigquery.ScalarQueryParameter("email", "STRING", email)]
    results_df = executor.execute_query_to_dataframe(query, params)
    if results_df.empty:
        return None
    row = results_df.iloc[0].to_dict()
    # Garante tipos corretos para o UserInDB
    user_data = {
        "id_usuario": str(row.get("id_usuario", "")),
        "id_cliente": str(row.get("id_cliente", "")),
        "nome": str(row.get("nome", "")),
        "email": str(row.get("email", "")),
        "hashed_password": str(row.get("hashed_password", "")),
        "ativo": bool(row.get("ativo", True)),
        "papeis": [str(p) for p in (row.get("papeis") or []) if p]
    }
    return UserInDB(**user_data)
