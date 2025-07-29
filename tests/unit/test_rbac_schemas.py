from src.schemas.rbac_schemas import (
    Client,
    Token,
    TokenData,
    UserBase,
    UserCreate,
    UserInDB,
    UserPublic,
)


def test_token():
    obj = Token(access_token="abc", token_type="bearer")
    assert obj.token_type == "bearer"


def test_token_data():
    obj = TokenData(sub="user1", id_cliente="cli1", roles=["admin"])
    assert obj.sub == "user1"
    assert "admin" in obj.roles


def test_user_base():
    obj = UserBase(email="a@b.com", nome="Ana")
    assert obj.nome == "Ana"


def test_user_create():
    obj = UserCreate(email="a@b.com", nome="Ana", password="123", papeis=["admin"])
    assert obj.password == "123"


def test_user_in_db():
    obj = UserInDB(
        email="a@b.com",
        nome="Ana",
        id_usuario="1",
        hashed_password="hash",
        ativo=True,
        papeis=["admin"],
    )
    assert obj.ativo is True


def test_user_public():
    obj = UserPublic(
        email="a@b.com", nome="Ana", id_usuario="1", ativo=True, papeis=["admin"]
    )
    assert obj.ativo is True


def test_client():
    obj = Client(id_cliente="cli1", nome_empresa="Empresa", status="ativo")
    assert obj.status == "ativo"
