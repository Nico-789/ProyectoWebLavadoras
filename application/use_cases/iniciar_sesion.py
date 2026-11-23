from domain.repositories.usuario_repository import UsuarioRepository
from application.interfaces.hasheador_password import HasheadorPassword
from domain.entities.usuario import Usuario
from application.exceptions import CredencialesInvalidas

class IniciarSesion:
    def __init__(self, usuario_repository: UsuarioRepository,hasheador:HasheadorPassword):
        self.usuario_repository = usuario_repository
        self.hasheador=hasheador

    def ejecutar(self, nombre_usuario, password):
        usuario=self.usuario_repository.obtener_por_nombre(nombre_usuario)
        if not usuario or not self.hasheador.verificar(password,usuario.password_hash):
            raise CredencialesInvalidas()
        return nombre_usuario
