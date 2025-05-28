import base64




def decrypt_user_id(encrypted_id: str) -> int | None:
    try:
        encrypted_bytes = encrypted_id.encode('utf-8')
        user_id_bytes = base64.urlsafe_b64decode(encrypted_bytes)
        user_id_str = user_id_bytes.decode('utf-8')
        return int(user_id_str)
    except Exception:
        return None
