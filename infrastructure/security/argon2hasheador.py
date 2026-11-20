from argon2 import PasswordHasher
from argon2.exceptions import InvalidHashError, VerificationError

from application.interfaces.hasheador_password import HasheadorPassword


class Argon2Hasheador(HasheadorPassword):
    def __init__(self):
        self._hasher = PasswordHasher()

    def hashear(self, password: str) -> str:
        return self._hasher.hash(password)

    def verificar(self, password: str, password_hash: str) -> bool:
        try:
            return self._hasher.verify(password_hash, password)
        except (VerificationError, InvalidHashError):
            return False
        