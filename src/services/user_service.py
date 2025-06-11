"""
Serviço para interagir com as tabelas de usuários no BigQuery.
"""
from typing import Optional
from src.utils.bq_executor import BigQueryExecutor
from src.schemas.rbac_schemas import UserInDB

def get_user_by_email(email: str) -> Optional[UserInDB]:
    executor = BigQueryExecutor()
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
    params = [("email", "STRING", email)]
    results = executor.execute_query(query, params)
    if not results:
        return None
    user_data = dict(results[0])
    if not user_data.get("papeis"):
        user_data["papeis"] = []
    return UserInDB(**user_data)
