from domain.entities.usuario import Usuario
from domain.repositories.usuario_repository import UsuarioRepository
from application.interfaces.hasheador_password import HasheadorPassword


class CrearUsuario:
    def __init__(self, usuario_repository: UsuarioRepository, hasheador: HasheadorPassword):
        self.usuario_repository = usuario_repository
        self.hasheador = hasheador

    def ejecutar(self, nombre_usuario, password):
        if not password:
            raise ValueError("La contraseña no puede estar vacía")
        password_hash = self.hasheador.hashear(password)
        usuario = Usuario(id=None, nombre_usuario=nombre_usuario, password_hash=password_hash)
        self.usuario_repository.guardar(usuario)
        return nombre_usuario