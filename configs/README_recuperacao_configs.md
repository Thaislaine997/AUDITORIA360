# Procedimento de recuperação/descriptografia de arquivos protegidos

1. Certifique-se de ter o arquivo `configs.key` gerado na criptografia e a senha utilizada.
2. Execute o script `decrypt_configs.py` na pasta `configs`:

```bash
python3 configs/decrypt_configs.py
```

3. Informe a senha utilizada na criptografia quando solicitado.
4. Os arquivos `.enc` serão restaurados para o formato original.

**Atenção:**

- Nunca compartilhe a senha ou o arquivo `configs.key` fora do ambiente seguro.
- Após a recuperação, reexecute o script de criptografia se precisar proteger novamente.
