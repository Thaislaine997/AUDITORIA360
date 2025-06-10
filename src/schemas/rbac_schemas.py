"""
Schemas Pydantic para o sistema de Role-Based Access Control (RBAC).
Estes modelos são usados para validação de dados na API, serialização
e para fornecer uma estrutura de dados clara e tipada no código.
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional

# ================== TOKEN SCHEMAS ==================

class Token(BaseModel):
    """Schema para a resposta do endpoint de login."""
    access_token: str
    token_type: str

class TokenData(BaseModel):
    """
    Schema para os dados que são codificados dentro do JWT.
    'sub' é o nome padrão para o 'subject' do token (nosso id_usuario).
    """
    sub: str
    id_cliente: Optional[str] = None
    roles: List[str] = []


# ================== USER SCHEMAS ==================

class UserBase(BaseModel):
    """Campos base compartilhados por todos os schemas de usuário."""
    email: EmailStr
    nome: str

class UserCreate(UserBase):
    """Schema para criar um novo usuário. Recebe a senha em texto plano."""
    password: str
    id_cliente: Optional[str] = None # Opcional, para criar usuários Dpeixer
    papeis: List[str] # Ex: ["CLIENTE_ADMIN"]

class UserInDB(UserBase):
    """
    Schema para representar um usuário completo, como ele vem do banco de dados.
    Inclui campos sensíveis e de sistema.
    """
    id_usuario: str
    id_cliente: Optional[str] = None
    hashed_password: str
    ativo: bool
    papeis: List[str] = []

    class Config:
        # Permite que o Pydantic leia dados de objetos, não apenas de dicts.
        # Útil ao converter resultados de ORMs ou queries.
        orm_mode = True

class UserPublic(UserBase):
    """
    Schema para exibir dados públicos de um usuário.
    NUNCA exponha a senha ou outros dados sensíveis.
    """
    id_usuario: str
    id_cliente: Optional[str] = None
    ativo: bool
    papeis: List[str] = []

    class Config:
        orm_mode = True

# ================== CLIENT SCHEMAS ==================

class Client(BaseModel):
    """Schema para representar um cliente."""
    id_cliente: str
    nome_empresa: str
    status: str

    class Config:
        orm_mode = True
