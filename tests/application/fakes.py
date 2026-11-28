from application.interfaces.hasheador_password import HasheadorPassword


class HasheadorFalso(HasheadorPassword):
    def hashear(self, password):
        return f"hash-falso:{password}"

    def verificar(self, password, password_hash):
        return password_hash == self.hashear(password)
    