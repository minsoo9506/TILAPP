import bcrypt


class Crypto:
    def __init__(self):
        pass

    def encrypt(self, secret: str) -> str:
        # bcrypt는 72바이트까지만 처리 가능하므로 잘라냄
        secret_bytes = secret.encode("utf-8")[:72]
        hashed = bcrypt.hashpw(secret_bytes, bcrypt.gensalt())
        return hashed.decode("utf-8")

    def verify(self, secret: str, hashed: str) -> bool:
        secret_bytes = secret.encode("utf-8")[:72]
        hashed_bytes = hashed.encode("utf-8")
        return bcrypt.checkpw(secret_bytes, hashed_bytes)


__all__ = ["Crypto"]
