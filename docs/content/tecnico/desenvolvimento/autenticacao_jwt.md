# Fluxo de Autenticação JWT (RBAC) - AUDITORIA360

## 1. Login e Obtenção do Token

- **Endpoint:** `POST /api/auth/token`
- **Body:** `application/x-www-form-urlencoded`
  - `username`: e-mail do usuário
  - `password`: senha do usuário

**Exemplo de requisição:**

```bash
curl -X POST "http://localhost:8000/api/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@empresa.com&password=suasenha"
```

**Resposta:**

```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

---

## 2. Acesso a Endpoints Protegidos

- **Inclua o token JWT no header Authorization:**
  ```
  Authorization: Bearer <access_token>
  ```

**Exemplo de requisição:**

```bash
curl -H "Authorization: Bearer <access_token>" \
  http://localhost:8000/api/auth/users/me/
```

---

## 3. Estrutura do Token JWT

O token contém:

- `sub`: id do usuário
- `id_cliente`: id do cliente
- `roles`: lista de papéis do usuário

---

## 4. Isolamento e Permissões

- Endpoints protegidos usam:
  ```python
  current_user: TokenData = Depends(get_current_user)
  ```
- O backend filtra dados por `id_cliente` e verifica permissões em `roles`.
- Exemplo de proteção:
  ```python
  if "CLIENTE_VISUALIZADOR" not in current_user.roles and "DPEIXER_ADMIN" not in current_user.roles:
      raise HTTPException(status_code=403, detail="Permissão negada.")
  ```

---

## 5. Fluxo de Logout

- O logout é feito apenas no frontend: basta descartar o token JWT.

---

## 6. Erros comuns

- **401 Unauthorized:** Token ausente, inválido ou expirado.
- **403 Forbidden:** Usuário não tem permissão para acessar o recurso.
