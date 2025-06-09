"""
Controller para gerenciar o cadastro e autenticação de Contabilidades e seus usuários.
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
import uuid

from src.schemas_models import (
    RegistroContabilidadePayload,
    RegistroContabilidadeResponse,
    ContabilidadeResponse,
    UsuarioContabilidadeResponse,
    Token,
    TokenData,
    EmpresaClienteSimplificado
)
from configs.config import settings
from google.cloud import bigquery

# Configuração de Autenticação
SECRET_KEY = settings.SECRET_KEY_CONTABILIDADE
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = settings.ACCESS_TOKEN_EXPIRE_MINUTES_CONTABILIDADE

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/contabilidades/login/token")

TABLE_ID_CONTABILIDADES = f"{settings.BIGQUERY_PROJECT_ID}.{settings.BIGQUERY_DATASET_ID}.Contabilidades"
TABLE_ID_USUARIOS_CONTABILIDADE = f"{settings.BIGQUERY_PROJECT_ID}.{settings.BIGQUERY_DATASET_ID}.UsuariosContabilidade"
TABLE_ID_EMPRESAS_CLIENTES = f"{settings.BIGQUERY_PROJECT_ID}.{settings.BIGQUERY_DATASET_ID}.EmpresasClientes"
TABLE_ID_CONTABILIDADE_EMPRESA_CLIENTE_LINK = f"{settings.BIGQUERY_PROJECT_ID}.{settings.BIGQUERY_DATASET_ID}.ContabilidadeEmpresaClienteLink"

client = bigquery.Client()

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password):
    return pwd_context.hash(password)

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

async def get_current_user(token: str = Depends(oauth2_scheme)) -> TokenData:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar as credenciais",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email_from_payload = payload.get("sub")
        id_usuario_contabilidade_from_payload = payload.get("id_usuario_contabilidade")
        id_contabilidade_from_payload = payload.get("id_contabilidade")

        if not isinstance(email_from_payload, str) or \
           not isinstance(id_usuario_contabilidade_from_payload, str) or \
           not isinstance(id_contabilidade_from_payload, str):
            raise credentials_exception
            
        # Agora que sabemos que são strings, podemos usá-los diretamente.
        token_data = TokenData(
            email=email_from_payload, 
            id_usuario_contabilidade=id_usuario_contabilidade_from_payload, 
            id_contabilidade=id_contabilidade_from_payload
        )
        return token_data  # Adicionado o retorno aqui
    except JWTError:
        raise credentials_exception
    # Removido o 'return token_data' daqui para garantir que todos os caminhos retornem ou levantem exceção dentro do try/except

async def get_current_active_user(current_user: TokenData = Depends(get_current_user)) -> TokenData:
    # Consulta ao BigQuery para verificar se o usuário está ativo
    query = f"""SELECT ativo FROM `{TABLE_ID_USUARIOS_CONTABILIDADE}` 
                 WHERE id_usuario_contabilidade = @id_usuario_contabilidade AND ativo = TRUE"""
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_usuario_contabilidade", "STRING", current_user.id_usuario_contabilidade)
        ]
    )
    query_job = client.query(query, job_config=job_config)
    results = list(query_job.result())
    
    if not results:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Usuário inativo ou não encontrado")
    return current_user


def registrar_nova_contabilidade_e_usuario(
    payload: RegistroContabilidadePayload
) -> RegistroContabilidadeResponse:
    """Registra uma nova contabilidade e seu primeiro usuário administrador."""
    contabilidade_data = payload.contabilidade
    usuario_data = payload.usuario

    # 1. Verificar se o CNPJ já existe
    query_cnpj = f"""SELECT id_contabilidade FROM `{TABLE_ID_CONTABILIDADES}` WHERE cnpj = @cnpj"""
    job_config_cnpj = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("cnpj", "STRING", contabilidade_data.cnpj)]
    )
    query_job_cnpj = client.query(query_cnpj, job_config=job_config_cnpj)
    results_cnpj = list(query_job_cnpj.result())
    if results_cnpj:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"CNPJ {contabilidade_data.cnpj} já cadastrado.")

    # 2. Verificar se o email do usuário já existe
    query_email = f"""SELECT id_usuario_contabilidade FROM `{TABLE_ID_USUARIOS_CONTABILIDADE}` WHERE email = @email"""
    job_config_email = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("email", "STRING", usuario_data.email)]
    )
    query_job_email = client.query(query_email, job_config=job_config_email)
    results_email = list(query_job_email.result())
    if results_email:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"Email {usuario_data.email} já cadastrado para outro usuário.")

    # 3. Criar a Contabilidade
    id_contabilidade = str(uuid.uuid4())
    agora = datetime.now(timezone.utc)
    contabilidade_row = {
        "id_contabilidade": id_contabilidade,
        "cnpj": contabilidade_data.cnpj,
        "razao_social": contabilidade_data.razao_social,
        "nome_fantasia": contabilidade_data.nome_fantasia,
        "data_cadastro": agora.isoformat(),
        "data_atualizacao": agora.isoformat(),
        "ativo": True
    }
    errors_cont = client.insert_rows_json(TABLE_ID_CONTABILIDADES, [contabilidade_row])
    if errors_cont:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao inserir contabilidade no BigQuery: {errors_cont}")

    # 4. Criar o Usuário da Contabilidade
    id_usuario = str(uuid.uuid4())
    senha_hash = get_password_hash(usuario_data.senha)
    usuario_row = {
        "id_usuario_contabilidade": id_usuario,
        "id_contabilidade": id_contabilidade,
        "email": usuario_data.email,
        "senha_hash": senha_hash,
        "nome_usuario": usuario_data.nome_usuario,
        "cargo": usuario_data.cargo,
        "data_criacao": agora.isoformat(),
        "ativo": True
    }
    errors_user = client.insert_rows_json(TABLE_ID_USUARIOS_CONTABILIDADE, [usuario_row])
    if errors_user:
        # Idealmente, deveríamos ter uma transação ou lógica de rollback aqui
        # Por simplicidade, vamos apenas logar o erro e levantar a exceção
        print(f"Erro ao inserir usuário, mas contabilidade {id_contabilidade} foi criada.")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Erro ao inserir usuário no BigQuery: {errors_user}")

    # 5. Tentar vincular automaticamente a empresas clientes existentes
    try:
        vincular_contabilidade_a_clientes_por_cnpj(id_contabilidade, contabilidade_data.cnpj)
    except Exception as e:
        # Logar o erro mas não impedir o registro da contabilidade
        print(f"Alerta: Falha ao tentar vincular automaticamente a contabilidade {id_contabilidade} (CNPJ: {contabilidade_data.cnpj}) a empresas clientes: {str(e)}")


    return RegistroContabilidadeResponse(
        contabilidade=ContabilidadeResponse(
            id_contabilidade=id_contabilidade,
            cnpj=contabilidade_data.cnpj,
            razao_social=contabilidade_data.razao_social,
            nome_fantasia=contabilidade_data.nome_fantasia,
            data_cadastro=agora,
            data_atualizacao=agora,
            ativo=True
        ),
        usuario=UsuarioContabilidadeResponse(
            id_usuario_contabilidade=id_usuario,
            id_contabilidade=id_contabilidade,
            email=usuario_data.email,
            nome_usuario=usuario_data.nome_usuario,
            cargo=usuario_data.cargo,
            data_criacao=agora,
            ativo=True
        )
    )

def autenticar_usuario_contabilidade(email: str, senha_fornecida: str) -> UsuarioContabilidadeResponse | None:
    """Autentica um usuário da contabilidade e retorna seus dados se válido."""
    query = f"""SELECT id_usuario_contabilidade, id_contabilidade, email, senha_hash, nome_usuario, cargo, data_criacao, data_ultimo_login, ativo 
                 FROM `{TABLE_ID_USUARIOS_CONTABILIDADE}` 
                 WHERE email = @email""" # Removido `AND ativo = TRUE` para dar feedback sobre conta inativa
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("email", "STRING", email)]
    )
    query_job = client.query(query, job_config=job_config)
    
    results = list(query_job.result())
    if not results:
        return None # Usuário não encontrado
    
    user_row = results[0]

    if not user_row.ativo:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Conta de usuário inativa.")
    
    if not verify_password(senha_fornecida, user_row.senha_hash):
        return None # Senha incorreta
    
    # Atualizar data_ultimo_login
    agora_datetime = datetime.now(timezone.utc) # Usar datetime object
    agora_iso = agora_datetime.isoformat() # Converter para string ISO para o BigQuery

    update_query = f"""UPDATE `{TABLE_ID_USUARIOS_CONTABILIDADE}`
                       SET data_ultimo_login = @agora
                       WHERE id_usuario_contabilidade = @id_usuario"""
    update_job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("agora", "TIMESTAMP", agora_iso), # Usar string ISO
            bigquery.ScalarQueryParameter("id_usuario", "STRING", user_row.id_usuario_contabilidade)
        ]
    )
    client.query(update_query, job_config=update_job_config).result()

    return UsuarioContabilidadeResponse(
        id_usuario_contabilidade=user_row.id_usuario_contabilidade,
        id_contabilidade=user_row.id_contabilidade,
        email=user_row.email,
        nome_usuario=user_row.nome_usuario,
        cargo=user_row.cargo,
        data_criacao=user_row.data_criacao,
        data_ultimo_login=agora_datetime, # Usar o objeto datetime para o Pydantic model
        ativo=user_row.ativo
    )

def login_para_token_acesso(
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Token:
    """Processa o login e retorna um token JWT."""
    usuario = autenticar_usuario_contabilidade(email=form_data.username, senha_fornecida=form_data.password)
    if not usuario:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email ou senha incorretos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": usuario.email, "id_usuario_contabilidade": usuario.id_usuario_contabilidade, "id_contabilidade": usuario.id_contabilidade},
        expires_delta=access_token_expires
    )
    return Token(access_token=access_token, token_type="bearer")

def get_usuario_contabilidade_completo_por_id(id_usuario: str) -> UsuarioContabilidadeResponse | None:
    """Busca um usuário de contabilidade completo pelo seu ID."""
    query = f"""SELECT id_usuario_contabilidade, id_contabilidade, email, nome_usuario, cargo, data_criacao, data_ultimo_login, ativo 
                 FROM `{TABLE_ID_USUARIOS_CONTABILIDADE}` 
                 WHERE id_usuario_contabilidade = @id_usuario"""
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("id_usuario", "STRING", id_usuario)]
    )
    query_job = client.query(query, job_config=job_config)
    results = list(query_job.result())

    if not results:
        return None
    
    user_row = results[0]

    # O cliente BigQuery para Python geralmente retorna objetos datetime para campos TIMESTAMP.
    # Pydantic também tentará converter strings ISO para datetime automaticamente.
    # data_ultimo_login pode ser None se nunca houve login ou se o campo é NULL.
    return UsuarioContabilidadeResponse(
        id_usuario_contabilidade=user_row.id_usuario_contabilidade,
        id_contabilidade=user_row.id_contabilidade,
        email=user_row.email,
        nome_usuario=user_row.nome_usuario,
        cargo=user_row.cargo,
        data_criacao=user_row.data_criacao, # Deve ser datetime
        data_ultimo_login=user_row.data_ultimo_login, # Pode ser datetime ou None
        ativo=user_row.ativo
    )

def vincular_contabilidade_a_clientes_por_cnpj(id_contabilidade_nova: str, cnpj_contabilidade_nova: str):
    """
    Busca por empresas clientes que declararam o CNPJ da contabilidade recém-registrada
    e cria os vínculos na tabela ContabilidadeEmpresaClienteLink.
    """
    query_empresas_para_vincular = f"""
        SELECT ec.id_empresa_cliente
        FROM `{TABLE_ID_EMPRESAS_CLIENTES}` ec
        LEFT JOIN `{TABLE_ID_CONTABILIDADE_EMPRESA_CLIENTE_LINK}` link 
            ON ec.id_empresa_cliente = link.id_empresa_cliente AND link.id_contabilidade = @id_contabilidade_nova
        WHERE ec.cnpj_contabilidade_declarado = @cnpj_contabilidade_nova
          AND ec.ativo = TRUE
          AND link.id_link IS NULL -- Garante que o vínculo ainda não exista para esta contabilidade
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[
            bigquery.ScalarQueryParameter("id_contabilidade_nova", "STRING", id_contabilidade_nova),
            bigquery.ScalarQueryParameter("cnpj_contabilidade_nova", "STRING", cnpj_contabilidade_nova),
        ]
    )
    query_job = client.query(query_empresas_para_vincular, job_config=job_config)
    empresas_a_vincular = list(query_job.result())

    if not empresas_a_vincular:
        print(f"Nenhuma empresa cliente encontrada para vincular automaticamente à contabilidade CNPJ: {cnpj_contabilidade_nova}")
        return

    links_para_inserir = []
    agora = datetime.now(timezone.utc).isoformat()
    for empresa_row in empresas_a_vincular:
        id_link = str(uuid.uuid4())
        links_para_inserir.append({
            "id_link": id_link,
            "id_contabilidade": id_contabilidade_nova,
            "id_empresa_cliente": empresa_row.id_empresa_cliente,
            "data_vinculo": agora,
            "ativo": True,
            "origem_vinculo": "AUTOMATICO_REGISTRO_CONTABILIDADE"
        })
        print(f"Preparando para vincular contabilidade {id_contabilidade_nova} à empresa cliente {empresa_row.id_empresa_cliente}")

    if links_para_inserir:
        errors_link = client.insert_rows_json(TABLE_ID_CONTABILIDADE_EMPRESA_CLIENTE_LINK, links_para_inserir)
        if errors_link:
            # Logar o erro, mas não tratar como crítico para o registro da contabilidade
            print(f"Erro ao tentar inserir vínculos automáticos para contabilidade {id_contabilidade_nova} no BigQuery: {errors_link}")
        else:
            print(f"{len(links_para_inserir)} vínculos automáticos criados com sucesso para a contabilidade {id_contabilidade_nova}.")

def listar_clientes_vinculados_por_contabilidade(id_contabilidade: str) -> list[EmpresaClienteSimplificado]:
    """
    Retorna uma lista simplificada de empresas clientes vinculadas a uma contabilidade.
    """
    query = f"""
        SELECT ec.id_empresa_cliente, ec.cnpj_empresa, ec.razao_social, ec.nome_fantasia, ec.ativo
        FROM `{TABLE_ID_CONTABILIDADE_EMPRESA_CLIENTE_LINK}` link
        JOIN `{TABLE_ID_EMPRESAS_CLIENTES}` ec
          ON link.id_empresa_cliente = ec.id_empresa_cliente
        WHERE link.id_contabilidade = @id_contabilidade
          AND link.ativo = TRUE
          AND ec.ativo = TRUE
    """
    job_config = bigquery.QueryJobConfig(
        query_parameters=[bigquery.ScalarQueryParameter("id_contabilidade", "STRING", id_contabilidade)]
    )
    query_job = client.query(query, job_config=job_config)
    results = list(query_job.result())
    return [EmpresaClienteSimplificado(**dict(row)) for row in results]

