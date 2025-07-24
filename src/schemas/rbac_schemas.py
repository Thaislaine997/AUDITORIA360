"""
Schemas Pydantic para Role-Based Access Control (RBAC).
"""
from pydantic import BaseModel, EmailStr
from typing import List, Optional

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    sub: str
    id_cliente: Optional[str] = None
    roles: List[str] = []
    email: Optional[str] = None
    id_usuario_contabilidade: Optional[str] = None
    id_contabilidade: Optional[str] = None

class UserBase(BaseModel):
    email: EmailStr
    nome: str

class UserCreate(UserBase):
    password: str
    id_cliente: Optional[str] = None
    papeis: List[str]

class UserInDB(UserBase):
    id_usuario: str
    id_cliente: Optional[str] = None
    hashed_password: str
    ativo: bool
    papeis: List[str] = []
    class Config:
        orm_mode = True

class UserPublic(UserBase):
    id_usuario: str
    id_cliente: Optional[str] = None
    ativo: bool
    papeis: List[str] = []
    class Config:
        orm_mode = True

class Client(BaseModel):
    id_cliente: str
    nome_empresa: str
    status: str
    class Config:
        orm_mode = True
