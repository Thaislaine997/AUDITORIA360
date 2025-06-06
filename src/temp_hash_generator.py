from auth_utils import get_password_hash

password_to_hash = "41283407.Dp"
hashed_password = get_password_hash(password_to_hash)
print(hashed_password)
